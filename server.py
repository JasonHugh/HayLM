from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import FileResponse, StreamingResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import HTMLResponse
# from asr.sense_voice import get_asr_text, load_asr_model
from util.prompt import get_system_prompt
from asr.paraformer_dashscope import get_asr_text
from tts import sambert_dashscope
import os, yaml, re, json, time, emoji
from util import chat
from util.db import SQLiteTool
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from util.data_model import User, Session
from pydantic import ValidationError
from pydub import AudioSegment
from service.user_service import UserService
from service.content_service import ContentService
from service.game_service import GameService
from db.models import AIRole, History, UserConfig, Game
from util.schemas import *
from db.database import DatabaseUtil
from util import utils

app = FastAPI(title='Child Friend')

user_dir = "user_data"

# sqlite init
db_dir = user_dir + "/sqlite"
if not os.path.exists(db_dir):
    os.makedirs(db_dir)
sqlite_tool = SQLiteTool(db_dir + '/chat.db')
sqlite_tool.connect()

# auth
JWT_SECRET_KEY = "haylm"
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_DAYS = 90

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# asr tts model load
# tts_model = sambert.load_tts_model()
# asr_model = load_asr_model()

# audio dir init
input_audio_dir = user_dir + "/input_audio"
if not os.path.exists(input_audio_dir):
    os.makedirs(input_audio_dir)
output_audio_dir = user_dir + "/output_audio"
if not os.path.exists(output_audio_dir):
    os.makedirs(output_audio_dir)

with open("secrets/cfg.yaml", "r", encoding='utf-8') as file:
    conf = yaml.safe_load(file)

OPENAI_MODEL_NAME = "glm-4-flash"


##########################################################

# 跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://118.89.73.252:4173", "https://192.168.1.101:5173", "https://192.168.1.102:5173","https://192.168.1.100:5173","https://192.168.1.103:5173"],  # 允许所有域，也可以指定特定域
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)
 
app.mount("/static", StaticFiles(directory="static"), name="static")
# 静态文件代理
class RedirectToIndexMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 排除静态文件
        if not request.url.path.endswith((".js", ".css", ".png", ".ico")) and not request.url.path.startswith("/api") and not request.url.path.startswith("/docs"):
            # 只拦截指定前缀
            if request.url.path.startswith("/") or request.url.path == "/":
                return HTMLResponse(content=request.app.index_html, status_code=200)
        response = await call_next(request)
        return response
# 添加中间件
app.add_middleware(RedirectToIndexMiddleware)
 
 
# 读取index.html
with open("static/dist/index.html", encoding='utf-8') as f:
    app.index_html = f.read()

# 自定义JS文件的MIME类型为application/javascript
@app.middleware("http")
async def override_static_file_mimetype(request, call_next):
    response = await call_next(request)
    if request.url.path.endswith((".js")):
        response.headers["content-type"] = "application/javascript"
    return response

##########################################################
 

@app.post("/api/v1/register")
def register(userRequest: UserRequest):
    success, user = UserService().register(userRequest)
    if not success:
        return {"success": False, "message": user}
    
    # generate jwt token
    access_token = __create_access_token(
        data={"user_id":user.id,"name":user.name,"SN":user.SN}, expires_delta=timedelta(days=JWT_EXPIRE_DAYS)
    )
    return {"success": True, "access_token": access_token}

@app.post("/api/v1/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user: User = __authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = __create_access_token(
        data={"user_id":user.id,"name":user.name,"SN":user.SN}, expires_delta=timedelta(days=JWT_EXPIRE_DAYS)
    )
    return {"success": True, "access_token": access_token}

def __create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(days=JWT_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def __authenticate_user(username, password):
    user = sqlite_tool.get_user(username)
    if user and pwd_context.verify(password, user.password):
        return user
    else:
        return None
        
async def __get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("name")
        if not username:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = sqlite_tool.get_user(username=username)
    if not user:
        raise credentials_exception
    return user


@app.get("/api/v1/chat/response")
async def get_response(user_input: str, user: User = Depends(__get_current_user)):
    print(f"start chat {datetime.now()}")
        
    if not user_input:
        return {"success": False, "message": "user input or wav file can't be null"}
    
    userService = UserService()
    # get user active session
    session: Session = userService.get_active_session(user.id)

    user_history = History(user_id=user.id, session_id=session.id,content=user_input, create_time=datetime.now())

    print("User: "+user_input)
    print(f"time {datetime.now()}")

    userConfig = userService.get_user_config(user.id)
    if userConfig.styled_role_id:
        ai_role = userService.get_ai_role(userConfig.styled_role_id)
        userConfig.ai_name = ai_role.ai_name
        userConfig.ai_role = ai_role.context + "里的" + ai_role.role_name
        userConfig.ai_profile = ai_role.profile
        userConfig.ai_timbre = ai_role.timbre
        userConfig.ai_tts_model = ai_role.tts_model
        DatabaseUtil.get_session().expire_all()

    # generate prompt
    if session.name == "MAIN":
        sys_prompt = get_system_prompt(userConfig, session)
    elif session.name.startswith("GAME:"):
        # get game prompt
        game_id = session.name.split(":")[1]
        gameService = GameService()
        game: Game = gameService.find_by_id(game_id)
        sys_prompt = game.prompt

    # get user history
    currentDate = datetime.now().strftime("%Y-%m-%d")
    histories: list[History] = sqlite_tool.get_history(user.id, session.id, date=currentDate, is_important=None,batchSize=100)
    # generate messages
    messages = [{"role": "system", "content": sys_prompt},{"role": "assistant", "content": "现在时间是："+utils.get_current_time_str_zh()}]
    if histories:
        for h in histories:
            messages.append({"role": h.role, "content": h.content})
    messages.append({"role": "user", "content": user_input})

    print(messages)
    print(f"time {datetime.now()}")
    # get response from llm
    responses = chat.get_streaming_response(messages, OPENAI_MODEL_NAME)

    return StreamingResponse(generateLLMResponse(responses=responses,userConfig=userConfig,user=user,session=session,user_history=user_history), media_type="text/event-stream")

def generateLLMResponse(responses: list, userConfig: UserConfig, user: User, session: Session, user_history: History):
    response_time = ""
    total_response_text = ""
    output_audio_paths = []
    sentence = ""
    delimiter = "[,，.。?？!！？?]"
    first = True
    event = ""
    for response in responses:
        print("字符："+response["text"])
        sentence += response["text"]
        total_response_text += response["text"]
        if first:
            event = "start"
            first = False
            response_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            yield f"event: {event}\ndata: " + json.dumps({"role":"user", "content":user_history.content, "create_time":user_history.create_time.strftime("%Y-%m-%d %H:%M:%S")}) + "\n\n"
        else:
            match = re.match(delimiter, response["text"])
            current_setence = ""
            if match:
                splits = sentence.split(match.group(0))
                current_setence = splits[0] + match.group(0)
                if len(current_setence) < 6:
                    continue
                if len(splits) > 1:
                    sentence = sentence.split(match.group(0))[1]
                else:
                    sentence = ""
            elif not response["isStop"]:
                continue

            event = "message"
            
            # if no more content, add history
            if response["isStop"]:
                event = "end"
                # add history
                contentService = ContentService()
                contentService.addUserHistory(user_history)
                contentService.addAIHistory(History(user_id=user.id, session_id=session.id,content=total_response_text, create_time=datetime.now()))

                if sentence == "":
                    print(f"{datetime.now()}")
                    yield f"event: {event}\ndata: " + json.dumps({
                        "role":"assistant", 
                        "content":"", 
                        "create_time":response_time,
                        "audio_path": ""
                    }) + "\n\n"
                    break
                else:
                    current_setence = sentence
            
            print("AI: "+current_setence)

            output_audio_path = ""
            # tts
            if(userConfig.ai_tts_model == "sambert"):
                #sambert-zhiying-v1 16K 童声
                #sambert-zhistella-v1  16K 知性女声
                #sambert-zhiming-v1  16K 诙谐男声
                #sambert-zhiwei-v1  16K 萝莉女声
                #sambert-zhishuo-v1  16K
                #sambert-zhimiao-emo-v1  16K
                output_audio_path = sambert_dashscope.get_tts_audio(current_setence, userConfig.ai_timbre)
                print("output audio path: "+ output_audio_path)
            if output_audio_path:
                output_audio_paths.append(output_audio_path)
            
            print(f"{event}: {datetime.now()}")
            # time.sleep(5)
            yield f"event: {event}\ndata: " + json.dumps({
                "role":"assistant", 
                "content":current_setence, 
                "create_time":response_time,
                "audio_path": output_audio_path
            }) + "\n\n"


@app.post("/api/v1/asr")
async def get_asr(user: User = Depends(__get_current_user), wav: UploadFile = File(...)):
    print(f"start asr {datetime.now()}")
    
    input_audio_path = "{}/{}.wav".format(input_audio_dir, datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
    # save audio with 16k
    audio = AudioSegment.from_file(wav.file)
    audio.set_frame_rate(16000).set_sample_width(2).export(input_audio_path, format="wav")
    print(os.path.abspath(input_audio_path))
    user_input = get_asr_text(os.path.abspath(input_audio_path))
    os.remove(input_audio_path)

    print(f"end asr {datetime.now()}")
        
    if not user_input:
        return {"success": False, "message": "没有检测到语音"}

    return {"success": True, "data": {"text": user_input}}

@app.get("/api/v1/chat/audio")
async def get_chat_audio(audio_path: str = None):
    return FileResponse(audio_path, media_type="audio/wav")

@app.get("/api/v1/chat/history")
async def get_history(session_id: int, date: str, user: User = Depends(__get_current_user)):
    match = re.match("\d{4}-\d{2}-\d{2}", date)
    if not match:
        return {"success": False, "message":"please format date to yyyy-mm-dd"}
    histories: list[History] = sqlite_tool.get_history(user_id=user.id, session_id=session_id, date=date, batchSize=30)
    return {"success": True, "data":{ "history": histories}}

@app.delete("/api/v1/chat/history/delete")
async def delete_history(history_id_list: list[int], user: User = Depends(__get_current_user)):
    for history_id in history_id_list:
        sqlite_tool.delete_history(history_id=history_id)
    return {"success": True}

@app.get("/api/v1/airoles")
async def find_all_airoles(user: User = Depends(__get_current_user)):
    userService = UserService()
    ai_roles: list[AIRole] = userService.find_all_airoles()
    return {"success": True, "data":{ "ai_roles": ai_roles}}

@app.get("/api/v1/user/getConfig")
def get_user_config(user: User = Depends(__get_current_user)):
    userService = UserService()
    user_config = userService.get_user_config(user.id)

    if not user_config:
        return {"success": False, "message": "user config not found"}
    
    if user_config.styled_role_id:
        styled_role = userService.get_ai_role(user_config.styled_role_id)
    else:
        styled_role = None

    return {"success": True, "data":{ "config": user_config, "styled_role": styled_role}}

@app.get("/api/v1/image/{img:path}")
async def get_image(img: str):
    return FileResponse("static/image/" + img, media_type="image/jpeg")

@app.get("/api/v1/audio/{audio}")
async def get_audio(audio: str):
    return FileResponse("static/audio/" + audio, media_type="audio/wav")

@app.post("/api/v1/user/updateStyledRole")
def config(styled_role_id: int, user: User = Depends(__get_current_user)):
    userService = UserService()
    success, message = userService.update_user_styled_role(user_id=user.id, styled_role_id=styled_role_id)
    
    if success:
        return {"success": True}
    else:
        return {"success": False, "message": message}
    

@app.post("/api/v1/user/updateCustomAIRole")
def config(custom_ai: CustomAIRequest, user: User = Depends(__get_current_user)):
    userService = UserService()
    success, message = userService.update_custom_ai_role(user_id=user.id, custom_ai=custom_ai)
    
    if success:
        return {"success": True}
    else:
        return {"success": False, "message": message}

@app.get("/api/v1/games")
def game(user: User = Depends(__get_current_user)):
    gameService = GameService()
    games: list[Game] = gameService.get_game_list()
    return {"success": True, "data":{ "games": games}}

@app.post("/api/v1/user/enable_game/{game_id}")
def game(game_id:int, user: User = Depends(__get_current_user)):
    userService = UserService()
    success, message = userService.enable_game(user.id, game_id)
    if success:
        return {"success": True}
    else:
        return {"success": False, "message": message}

@app.post("/api/v1/user/disable_game")
def game(user: User = Depends(__get_current_user)):
    userService = UserService()
    success, message = userService.disable_game(user.id)
    if success:
        return {"success": True}
    else:
        return {"success": False, "message": message}

