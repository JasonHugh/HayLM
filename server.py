from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from asr import sense_voice
import os, yaml
from datetime import datetime
from util import chat
from sys_prompt import get_sys_prompt
from util import db
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from util.data_model import User
from pydantic import ValidationError

app = FastAPI()

JWT_SECRET_KEY = "haylm"
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_DAYS = 90

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

asr_model = sense_voice.load_asr_model()
user_dir = "user_data"
user_audio_dir = user_dir + "/input_audio"
if not os.path.exists(user_audio_dir):
    os.makedirs(user_audio_dir)

with open("secrets/cfg.yaml", "r", encoding='utf-8') as file:
    conf = yaml.safe_load(file)
user_messages = {
    "1": [
        {"role": "system", "content": get_sys_prompt(conf)},
    ],
    "2": [
        {"role": "system", "content": get_sys_prompt(conf)},
    ]
}
 
@app.get("/")
async def index():
    return {"msg": "Hello World!"}

def __get_memory_messages(user_id: int):
    user_messages.get(user_id)


@app.post("/user/register")
def register(name: str = None, phone: str = None, SN: str = None, password: str = None):
    try:
        user = User.model_validate({"name":name, "phone":phone, "SN":SN, "password":pwd_context.hash(password)})
    except ValidationError as e:
        return {"success": False, "message": e.json()}
    
    success, result = db.add_user(user) 
    if success:
        # generate jwt token
        access_token = __create_access_token(
            data={"user_id":result,"name":name,"SN":SN}, expires_delta=timedelta(days=JWT_EXPIRE_DAYS)
        )
        return {"success": True, "access_token": access_token}
    else:
        return {"success": False, "message": result}

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = __authenticate_user(form_data.username, form_data.password)
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

def __authenticate_user(user_name, password):
    user = db.get_user(user_name)
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
    user = db.get_user(username=username)
    if not user:
        raise credentials_exception
    return user

@app.post("/user/config")
def config(user: User = Depends(__get_current_user)):
    return {"success": True, "message": user}
    pass


@app.post("/chat/response")
async def get_response(ser: User = Depends(__get_current_user), user_input: str = None, wav: UploadFile = File(...)):
    # asr
    audio_path = "{}/{}.wav".format(user_audio_dir, datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
    with open(audio_path, "wb") as f:
        f.write(wav.file.read())
    user_input = sense_voice.get_asr_text(asr_model, os.path.abspath(audio_path))
    print("User Input: "+user_input)
    os.remove(audio_path)

    # get response from llm
    chat.get_response()