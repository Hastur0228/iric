import whisper
import os



model = whisper.load_model("base")
result = model.transcribe('temp/videoplayback_audio.mp3', language='en')