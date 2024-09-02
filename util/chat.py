from openai import OpenAI
import os
import yaml
 
with open("cfg.yaml", "r", encoding='utf-8') as file:
    conf = yaml.safe_load(file)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or conf["api"]["openai_api_key"]
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL") or conf["api"]["openai_base_url"]
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME") or conf["api"]["openai_model_name"]

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
)

def get_streaming_response(messages):
    completion = client.chat.completions.create(
        model=OPENAI_MODEL_NAME,
        messages=messages,
        stream=True,
        temperature=0.8
    )
    # for chunk in completion:
    #     print(chunk.choices[0].delta.content, end="")
    return completion

def get_response(messages):
    completion = client.chat.completions.create(
        model=OPENAI_MODEL_NAME,
        messages=messages,
        stream=False,
        temperature=0.8
    )
    print(completion.choices[0].message)
    return completion.choices[0].message

def add_user_message(history:list, message:str):
    history.append({"role": "user", "content": message})
    return history

def add_ai_message(history:list, message:str):
    history.append({"role": "assistent", "content": message})
    return history

if __name__ == "__main__":
    get_response([
        {
    "role":"user",
        "content":"你好"
        },{
    "role":"assistant",
        "content":"你好！有什么我可以帮助你的吗？"
        },{
    "role":"user",
        "content":"教我做披萨"
        }
    ])