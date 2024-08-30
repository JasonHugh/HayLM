import dashscope
from dashscope.audio.tts import SpeechSynthesizer
import yaml
from datetime import datetime

with open("secrets/cfg.yaml", "r", encoding='utf-8') as file:
    conf = yaml.safe_load(file)
 
dashscope.api_key = conf["api"]["dashscope_api_key"]

def get_tts_audio(text):
    result = SpeechSynthesizer.call(model='sambert-zhiying-v1',
                                text=text,
                                sample_rate=48000,
                                format='wav')

    if result.get_audio_data() is not None:
        audio_folder = "audio"
        audio_path = "{}/out-{}.wav".format(audio_folder, datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
        with open(audio_path, 'wb') as f:
            f.write(result.get_audio_data())
    print(' get response: %s' % (audio_path))
    return audio_path