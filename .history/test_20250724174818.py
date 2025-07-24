
model = whisper.load_model(model_name)
result = model.transcribe(audio_path, language='en')