import whisper
import os

# 将 ffmpeg/bin 加入 PATH
ffmpeg_bin = os.path.abspath("ffmpeg/bin")
os.environ["PATH"] = ffmpeg_bin + os.pathsep + os.environ.get("PATH", "")

model = whisper.load_model("base")
result = model.transcribe('temp/videoplayback_audio.mp3', language='en')