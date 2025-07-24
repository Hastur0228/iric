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


def download_video_from_youtube(url, output_path):
    """使用yt-dlp下载YouTube视频（仅视频流，无音频）"""
    cmd = [
        'yt-dlp',
        '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
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


def merge_audio_video(video_path, audio_path, output_path):
    """用ffmpeg将新音轨与原视频合成新mp4"""
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


def main():
    url = input("请输入YouTube视频链接：").strip()
    with tempfile.TemporaryDirectory() as tmpdir:
        audio_path = os.path.join(tmpdir, "audio.mp3")
        video_path = os.path.join(tmpdir, "video.mp4")
        print("[1/6] 正在下载音频...")
        download_audio_from_youtube(url, audio_path)

        print("[2/6] 正在下载原视频...")
        download_video_from_youtube(url, video_path)

        print("[3/6] 正在语音转文字...")
        text = transcribe_audio(audio_path)
        print("识别文本：", text[:100], "...")

        print("[4/6] 正在翻译为中文...")
        translated = translate_text(text)
        print("翻译结果：", translated[:100], "...")

        output_audio = "output_zh.mp3"
        print("[5/6] 正在合成中文音频...")
        text_to_speech(translated, output_audio)
        print(f"新音轨已保存为 {output_audio}")

        output_video = "output_zh.mp4"
        print("[6/6] 正在合成新视频（中文音轨）...")
        merge_audio_video(video_path, output_audio, output_video)
        print(f"新视频已保存为 {output_video}")

if __name__ == "__main__":
    main() 