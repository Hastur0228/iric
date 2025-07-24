import os
import subprocess
import sys
import tempfile

# 依赖库：yt-dlp, openai-whisper, googletrans, gtts
# 安装命令：
# pip install yt-dlp openai-whisper googletrans==4.0.0-rc1 gtts

from googletrans import Translator
from gtts import gTTS
import whisper


def download_audio_from_youtube(url, output_path):
    """使用yt-dlp下载YouTube视频音频为mp3"""
    cmd = [
        'yt-dlp',
        '-f', 'bestaudio',
        '--extract-audio',
        '--audio-format', 'mp3',
        '-o', output_path,
        url
    ]
    subprocess.run(cmd, check=True)


def transcribe_audio(audio_path, model_name="base"):  # 可选：tiny, base, small, medium, large
    """用Whisper将音频转为英文文本"""
    model = whisper.load_model(model_name)
    result = model.transcribe(audio_path, language='en')
    return result['text']


def translate_text(text, dest_lang="zh-cn"):
    """用Google翻译将英文转为中文"""
    translator = Translator()
    translated = translator.translate(text, dest=dest_lang)
    return translated.text


def text_to_speech(text, output_audio_path, lang="zh-cn"):
    """用gTTS将中文文本转为音频"""
    tts = gTTS(text, lang=lang)
    tts.save(output_audio_path)


def main():
    url = input("请输入YouTube视频链接：").strip()
    with tempfile.TemporaryDirectory() as tmpdir:
        audio_path = os.path.join(tmpdir, "audio.mp3")
        print("[1/5] 正在下载音频...")
        download_audio_from_youtube(url, audio_path)

        print("[2/5] 正在语音转文字...")
        text = transcribe_audio(audio_path)
        print("识别文本：", text[:100], "...")

        print("[3/5] 正在翻译为中文...")
        translated = translate_text(text)
        print("翻译结果：", translated[:100], "...")

        output_audio = "output_zh.mp3"
        print("[4/5] 正在合成中文音频...")
        text_to_speech(translated, output_audio)
        print(f"[5/5] 新音轨已保存为 {output_audio}")

if __name__ == "__main__":
    main() 