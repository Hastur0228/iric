import os
import subprocess
import tempfile
from googletrans import Translator
from gtts import gTTS
import whisper

INPUT_DIR = 'Input_mp4'
OUTPUT_DIR = 'Output_mp4'

os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_audio_from_video(video_path, audio_path):
    """用ffmpeg从视频中提取音频为mp3"""
    cmd = [
        'ffmpeg', '-y',
        '-i', video_path,
        '-vn',
        '-acodec', 'mp3',
        audio_path
    ]
    subprocess.run(cmd, check=True)

def transcribe_audio(audio_path, model_name="base"):
    model = whisper.load_model(model_name)
    result = model.transcribe(audio_path, language='en')
    return result['text']

def translate_text(text, dest_lang="zh-cn"):
    translator = Translator()
    translated = translator.translate(text, dest=dest_lang)
    return translated.text

def text_to_speech(text, output_audio_path, lang="zh-cn"):
    tts = gTTS(text, lang=lang)
    tts.save(output_audio_path)

def merge_audio_video(video_path, audio_path, output_path):
    cmd = [
        'ffmpeg', '-y',
        '-i', video_path,
        '-i', audio_path,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-map', '0:v:0',
        '-map', '1:a:0',
        '-shortest',
        output_path
    ]
    subprocess.run(cmd, check=True)

def process_video_file(video_file):
    base = os.path.splitext(os.path.basename(video_file))[0]
    with tempfile.TemporaryDirectory() as tmpdir:
        audio_path = os.path.join(tmpdir, f"{base}_audio.mp3")
        print(f"[1/5] 正在提取音频: {video_file}")
        extract_audio_from_video(video_file, audio_path)

        print(f"[2/5] 正在语音转文字...")
        text = transcribe_audio(audio_path)
        print("识别文本：", text[:100], "...")

        print(f"[3/5] 正在翻译为中文...")
        translated = translate_text(text)
        print("翻译结果：", translated[:100], "...")

        output_audio = os.path.join(tmpdir, f"{base}_zh.mp3")
        print(f"[4/5] 正在合成中文音频...")
        text_to_speech(translated, output_audio)

        output_video = os.path.join(OUTPUT_DIR, f"{base}_zh.mp4")
        print(f"[5/5] 正在合成新视频（中文音轨）...")
        merge_audio_video(video_file, output_audio, output_video)
        print(f"新视频已保存为 {output_video}\n")

def main():
    mp4_files = [os.path.join(INPUT_DIR, f) for f in os.listdir(INPUT_DIR) if f.lower().endswith('.mp4')]
    if not mp4_files:
        print(f"未在 {INPUT_DIR} 目录下找到MP4文件。")
        return
    for video_file in mp4_files:
        try:
            process_video_file(video_file)
        except Exception as e:
            print(f"处理 {video_file} 时出错: {e}")

if __name__ == "__main__":
    main() 