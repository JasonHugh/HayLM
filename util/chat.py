from openai import OpenAI
import os
import yaml
 
with open("secrets/cfg.yaml", "r", encoding='utf-8') as file:
    conf = yaml.safe_load(file)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or conf["api"]["openai_api_key"]
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL") or conf["api"]["openai_base_url"]
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME") or conf["api"]["openai_model_name"]

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
)

def get_streaming_response(messages, model_name = OPENAI_MODEL_NAME):
    completion = client.chat.completions.create(
        model=model_name,
        messages=messages,
        stream=True,
        temperature=0.8
    )
    for chunk in completion:
        yield chunk.choices[0].delta.content

def get_response(messages, model_name = OPENAI_MODEL_NAME):
    completion = client.chat.completions.create(
        model=model_name,
        messages=messages,
        stream=False,
        temperature=0.8
    )
    return completion.choices[0].message.content

if __name__ == "__main__":
    for text in get_streaming_response([
        {
    "role":"user",
        "content":"你好"
        }
    ]):
        print(text)