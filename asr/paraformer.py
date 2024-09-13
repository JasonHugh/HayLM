from funasr import AutoModel

model_dir = "paraformer-zh"

def load_asr_model() -> AutoModel:
	model = AutoModel(
		model="paraformer-zh",  
		vad_model="fsmn-vad",  
		punc_model="ct-punc",
		device="cpu", 
		# spk_model="cam++", 
	)
	return model

def get_asr_text(model: AutoModel, absolute_audio_path):
	res = model.generate(input=absolute_audio_path, 
                     batch_size_s=300, 
                     hotword='魔搭',
					 language="auto")
	return res[0]["text"]

if __name__ == "__main__":
	print(get_asr_text(load_asr_model(), "/root/learning/HayLM/user_data/input_audio/out-2024-09-07-20-41-26.wav"))
