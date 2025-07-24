import whisper
import os
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Whisper将使用设备: {device.upper()}（{'GPU加速' if device == 'cuda' else 'CPU'}）")


model = whisper.load_model("base")
result = model.transcribe('temp/videoplayback_audio.mp3', language='en')