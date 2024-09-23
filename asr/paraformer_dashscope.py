# For prerequisites running the following sample, visit https://help.aliyun.com/document_detail/611472.html

from http import HTTPStatus
import dashscope
from dashscope.audio.asr import Recognition
import json, yaml
import requests
 
with open("secrets/cfg.yaml", "r", encoding='utf-8') as file:
    conf = yaml.safe_load(file)
 
dashscope.api_key = conf["api"]["dashscope_api_key"]
 
def get_asr_text(audio_path):
    recognition = Recognition(model='paraformer-realtime-v1',
                            format='wav',
                            sample_rate=16000,
                            language_hints=['zh', 'en'],
                            callback=None)
    result = recognition.call(audio_path)
    print(result)
    text = None
    if result.status_code == HTTPStatus.OK:
        for sentence in result.get_sentence():
            text = sentence['text']
            print(text)
    else:
        print('Error: ', result.message)
        
    return text
    
if __name__ == '__main__':
    get_asr_text('/home/lighthouse/HayLM/user_data/output_audio/2024-09-20-00-12-38.wav')