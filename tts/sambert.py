from modelscope.outputs import OutputKeys
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from datetime import datetime
import streamlit as st

# pip install kantts -f https://modelscope.oss-cn-beijing.aliyuncs.com/releases/repo.html
# pip install pytorch_wavelets tensorboardX scipy==1.12.0

@st.cache_resource
def load_tts_model():
    model_id = 'damo/speech_sambert-hifigan_tts_zh-cn_16k'
    model = pipeline(task=Tasks.text_to_speech, model=model_id)
    return model

def get_tts_audio(model, text):
    output = model(input=text, voice='zhibei_emo')
    wav = output[OutputKeys.OUTPUT_WAV]
    if len(wav) > 0:
        audio_folder = "audio"
        audio_path = "{}/out-{}.wav".format(audio_folder, datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
        with open(audio_path, 'wb') as f:
            f.write(wav)
    return audio_path