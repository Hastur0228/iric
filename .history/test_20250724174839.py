import whisper

model = whisper.load_model("base")
result = model.transcribe(audio_path, language='en')