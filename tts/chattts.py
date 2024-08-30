import ChatTTS
import torch
import torchaudio
import yaml
import streamlit as st
from datetime import datetime

with open("secrets/cfg.yaml", "r", encoding='utf-8') as file:
    conf = yaml.safe_load(file)

chattts_model_path = conf["tts"]["chattts_model_path"]

@st.cache_resource
def load_tts_model():
    model = ChatTTS.Chat()
    model.load(compile=False,source="custom",custom_path=chattts_model_path) # Set to True for better performance
    return model

def get_tts_audio(model, text):
    texts = [text]
    wavs = model.infer(texts)
    if len(wavs) > 0:
        audio_folder = "audio"
        audio_path = "{}/out-{}.wav".format(audio_folder, datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
        try:
            torchaudio.save(audio_path, torch.from_numpy(wavs[0]).unsqueeze(0), 24000)
        except:
            torchaudio.save(audio_path, torch.from_numpy(wavs[0]), 24000)
    return audio_path
        
        