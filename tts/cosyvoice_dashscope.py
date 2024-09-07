# coding=utf-8

import dashscope, yaml
from dashscope.audio.tts_v2 import *
from datetime import datetime
import os

with open("secrets/cfg.yaml", "r", encoding='utf-8') as file:
    conf = yaml.safe_load(file)
 
dashscope.api_key = conf["api"]["dashscope_api_key"]
model = "cosyvoice-v1"
voice = "longjielidou"


def get_tts_audio(text):
    user_dir = "user_data"
    # audio dir init
    user_audio_dir = user_dir + "/output_audio"
    if not os.path.exists(user_audio_dir):
        os.makedirs(user_audio_dir)
    audio_path = "{}/{}.wav".format(user_audio_dir, datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))

    class Callback(ResultCallback):
        _player = None
        _stream = None

        def on_open(self):
            self.file = open(audio_path, "wb")
            print("websocket is open.")

        def on_complete(self):
            print("speech synthesis task complete successfully.")

        def on_error(self, message: str):
            print(f"speech synthesis task failed, {message}")

        def on_close(self):
            print("websocket is closed.")
            self.file.close()

        def on_event(self, message):
            print(f"recv speech synthsis message {message}")

        def on_data(self, data: bytes) -> None:
            print("audio result length:", len(data))
            self.file.write(data)

    callback = Callback()

    synthesizer = SpeechSynthesizer(
        model=model,
        voice=voice,
        callback=callback,
    )

    synthesizer.call(text)
    print('requestId: ', synthesizer.get_last_request_id())
    return audio_path