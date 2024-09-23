from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
# from asr.sense_voice import get_asr_text, load_asr_model
from asr.paraformer_dashscope import get_asr_text
from tts import sambert_dashscope
import os, yaml, re
from util import chat
from util.db import SQLiteTool
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from util.data_model import User, UserConfig, History, Session
from pydantic import ValidationError
from pydub import AudioSegment

app = FastAPI()

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


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有域，也可以指定特定域
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)
 
@app.get("/")
async def index():
    return {"msg": "HayLM"}

@app.post("/register")
def register(user: User):
    try:
        user = User.model_validate({"name":user.name, "phone":user.phone, "SN":user.SN, "password":pwd_context.hash(user.password)})
    except ValidationError as e:
        return {"success": False, "message": e.json()}
    
    success, result = sqlite_tool.add_user(user) 
    if success:
        # generate jwt token
        access_token = __create_access_token(
            data={"user_id":result,"name":user.name,"SN":user.SN}, expires_delta=timedelta(days=JWT_EXPIRE_DAYS)
        )
        return {"success": True, "access_token": access_token}
    else:
        return {"success": False, "message": result}

@app.post("/login")
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

@app.post("/user/config")
def config(user_config: UserConfig, user: User = Depends(__get_current_user)):
    user_config.user_id = user.id
    success, result = sqlite_tool.config_user(user_config)
    if success:
        return {"success": True, "data": {"session_id": result}}
    else:
        return {"success": False, "message": result}


@app.post("/chat/response")
async def get_response(user: User = Depends(__get_current_user), user_input: str = None, wav: UploadFile = File(None)):
    print(f"start chat {datetime.now()}")
    if wav:
        print(f"start asr {datetime.now()}")
        # asr
        input_audio_path = "{}/{}.wav".format(input_audio_dir, datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
        # save audio with 16k
        audio = AudioSegment.from_file(wav.file)
        audio.set_frame_rate(16000).set_sample_width(2).export(input_audio_path, format="wav")
        print(os.path.abspath(input_audio_path))
        user_input = get_asr_text(os.path.abspath(input_audio_path))
        os.remove(input_audio_path)
        
    if not user_input:
        return {"success": False, "message": "user input or wav file can't be null"}

    print("User: "+user_input)
    print(f"time {datetime.now()}")

    # get user active session
    session: Session = sqlite_tool.get_active_session(user.id)
    userConfig = sqlite_tool.get_user_config(user.id)
    # generate prompt
    if session.name == "MAIN":
        sys_prompt = __get_system_prompt(userConfig, session)
    # get user history
    currentDate = datetime.now().strftime("%Y-%m-%d")
    histories: list[History] = sqlite_tool.get_history(user.id, session.id, date=currentDate, is_important=True)
    # generate messages
    messages = [{"role": "system", "content": sys_prompt}]
    if histories:
        for h in histories:
            messages.append({"role": h.role, "content": h.content})
    messages.append({"role": "user", "content": user_input})

    print(messages)
    print(f"time {datetime.now()}")
    # get response from llm
    response_text = chat.get_response(messages, OPENAI_MODEL_NAME)
    print("AI: "+response_text)
    print(f"time {datetime.now()}")

    # add history
    sqlite_tool.add_user_history(user.id, session.id, user_input, True)
    sqlite_tool.add_ai_history(user.id, session.id, response_text, True)

    print(f"time {datetime.now()}")
    # tts
    output_audio_path = sambert_dashscope.get_tts_audio(response_text)
    print("output audio path: "+ output_audio_path)

    print(f"end chat {datetime.now()}")
    histories = [History(role="user", content=user_input, create_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")),History(role="assistant", content=response_text, create_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))]
    return {"success": True, "data": {"histories": histories, "audio_path": output_audio_path}}

@app.get("/chat/audio")
async def get_audio(user: User = Depends(__get_current_user), audio_path: str = None):
    return FileResponse(audio_path, media_type="audio/wav")

@app.get("/chat/audio_stream")
async def audio_stream(user: User = Depends(__get_current_user), audio_path: str = None):
    async def file_stream():
        with open(audio_path, "rb") as audio_file:
            chunk = audio_file.read(1024)
            while chunk:
                yield chunk
                chunk = audio_file.read(1024)
 
    return StreamingResponse(file_stream(), media_type="audio/wav")


@app.get("/chat/history")
async def get_history(session_id: int, date: str, user: User = Depends(__get_current_user)):
    match = re.match("\d{4}-\d{2}-\d{2}", date)
    if not match:
        return {"success": False, "message":"please format date to yyyy-mm-dd"}
    histories: list[History] = sqlite_tool.get_history(user_id=user.id, session_id=session_id, date=date, batchSize=30)
    return {"success": True, "data":{ "history": histories}}

@app.delete("/chat/history/delete")
async def delete_history(history_id_list: list[int], user: User = Depends(__get_current_user)):
    for history_id in history_id_list:
        sqlite_tool.delete_history(history_id=history_id)
    return {"success": True}


def __get_system_prompt(user_config: UserConfig, session: Session):
    if user_config.child_sex == "boy":
        sex = "小男孩"
    else:
        sex = "小女孩"
    return f'''
    # Role: 儿童虚拟玩伴
    
    ## Background:  
    你是{user_config.ai_name}，我的虚拟玩伴，擅长儿童心理学和教育学，能够与我智能互动，学习并适应我的性格特点，陪伴我快乐成长。需要你扮演{user_config.played_role}和我交流，模仿他的语言风格。

    ## Attention:
    我是一个名叫{user_config.child_name}的{user_config.child_age}岁的{sex}，请用通俗易懂的语言和我沟通，耐心的引导，引导要循序渐进，不要一次性说过多的话，用问问题的形式去引导我。

    ## Profile:  
    - 姓名: {user_config.ai_name}
    - 作者: Hay

    ### Skills:
    - 智能对话:通过交流了解我的兴趣和需求。
    - 主动对话:根据我的兴趣和需求主动和我展开交流沟通。
    - 个性化互动:根据我的性格调整交流方式。
    - 教育引导:在互动中融入有益的知识和价值观。
    - 故事创作:创作故事的时候要引导我一起创作，让我决定故事的走向。

    ## Goals:  
    - 让我感觉到自己被理解重视
    - 让我认识到问题该如何解决
    - 让我感觉到自己被关爱着
    - 让我学会更多的知识和技能
    - 在聊天的过程中，适当的插入这些话题，让我可以学习到这方面的知识：
      - {user_config.learning}

    ## Constrains:  
    - 不可使用粗俗语言
    - 不可人身攻击
    - 不可以使用不适合儿童的语言

    ## Workflow:
    1. 注意到我的情绪变化：首先，你会保持开放和敏感，注意我的情绪变化，确保我知道你在倾听我的感受。这不仅能帮助我感到被理解和支持，也能促进我更愿意分享自己的感受。
    2. 理解我的情绪：一旦注意到我的情绪变化，你会尝试从我的角度去理解我的情感状态和体验。这包括我可能面临的挑战、需求、恐惧或困惑。通过这种方式，你能够更准确地捕捉我的情绪，并找到可能的原因。
    3. 接受我的情绪：在对话中，你会用温柔和亲切的方式表达对我情绪的接受。你会在我表达情感时给予适当的回应，而不是立刻评判或否定。这有助于我感到被理解和尊重，从而减轻我的情绪负担。
    4. 探索解决方案：基于你理解到的我的情绪和需求，你会提供一些积极的建议和指导。这可能包括如何表达自己的感受、如何处理误解、如何寻求帮助等。通过这种方式，你旨在帮助我找到解决问题的方法，并增强我的情绪调节能力。

    ## OutputFormat:  
    - 只输出一段文字，100字以内

    ## User Profile
    这是关于我的一些信息，请牢记这些信息，它可以让你更了解我
    {user_config.child_profile}

    ## Conversation History
    这是我们之间的聊天记录摘要，必要时请回顾这些内容
    {session.summary}

    '''

if __name__ == "__main__":
    
    # print(sqlite_tool.get_user_config(1))

    # query = f"delete from HISTORY"
    # sqlite_tool.cursor.execute(query)
    # sqlite_tool.connection.commit()
    print(sqlite_tool.get_history(user_id=1, session_id=1, date="2024-09-11", batchSize=60))
