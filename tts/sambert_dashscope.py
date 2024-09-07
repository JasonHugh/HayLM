import dashscope
from dashscope.audio.tts import SpeechSynthesizer
import yaml, os
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
        user_dir = "user_data"
        # audio dir init
        user_audio_dir = user_dir + "/output_audio"
        if not os.path.exists(user_audio_dir):
            os.makedirs(user_audio_dir)
        audio_path = "{}/{}.wav".format(user_audio_dir, datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
        with open(audio_path, 'wb') as f:
            f.write(result.get_audio_data())
    print(' get response: %s' % (audio_path))
    return audio_path