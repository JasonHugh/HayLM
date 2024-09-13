from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess
import os

model_dir = "iic/SenseVoiceSmall"

def load_asr_model() -> AutoModel:
	model = AutoModel(
		model=model_dir,
		trust_remote_code=True,
		remote_code="./model.py",  
		vad_model="fsmn-vad",
		vad_kwargs={"max_single_segment_time": 30000},
		device="cpu",
	)
	return model

def get_asr_text(model: AutoModel, absolute_audio_path):
	res = model.generate(
		input=absolute_audio_path,
		cache={},
		language="auto",  # "zh", "en", "yue", "ja", "ko", "nospeech"
		use_itn=True,
		batch_size_s=60,
		merge_vad=True,
		merge_length_s=15,
	)
	text = rich_transcription_postprocess(res[0]["text"])
	return text

if __name__ == "__main__":
	print(get_asr_text(load_asr_model(), "/root/learning/HayLM/user_data/input_audio/out-2024-09-07-20-41-26.wav"))