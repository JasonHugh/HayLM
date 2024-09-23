import sndhdr
from pydub import AudioSegment

 
# 音频文件路径
audio_file_path = '/home/lighthouse/HayLM/user_data/output_audio/2024-09-20-00-12-38.wav'
 
print(sndhdr.what(audio_file_path))

audio = AudioSegment.from_file(audio_file_path)
audio.set_frame_rate(16000).set_sample_width(2).export(audio_file_path, format="wav")