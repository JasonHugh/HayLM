from http import HTTPStatus
import dashscope
import json
import yaml
 
with open("secrets/cfg.yaml", "r", encoding='utf-8') as file:
    conf = yaml.safe_load(file)
    
 
dashscope.api_key = conf["api"]["dashscope_api_key"]

def get_asr_text(audio_path):
    task_response=dashscope.audio.asr.Transcription.async_call(
        model='paraformer-v1',
        file_urls=[audio_path],
        language_hints=['zh']
    )
    transcribe_response=dashscope.audio.asr.Transcription.wait(task=task_response.output.task_id)
    if transcribe_response.status_code == HTTPStatus.OK:
        print(json.dumps(transcribe_response.output, indent=4, ensure_ascii=False))
        print('transcription done!')