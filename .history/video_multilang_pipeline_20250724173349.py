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
    """
    用ffmpeg从视频文件中提取音频并保存为mp3格式。
    参数：
        video_path (str): 输入视频文件路径。
        audio_path (str): 输出音频文件路径（mp3）。
    """
    cmd = [
        'ffmpeg', '-y',
        '-i', video_path,
        '-vn',
        '-acodec', 'mp3',
        audio_path
    ]
    subprocess.run(cmd, check=True, shell=True, executable='cmd.exe')

def transcribe_audio(audio_path, model_name="base"):
    """
    使用OpenAI Whisper模型将音频文件转为英文文本。
    参数：
        audio_path (str): 输入音频文件路径（mp3）。
        model_name (str): Whisper模型名称，可选'tiny', 'base', 'small', 'medium', 'large'。
    返回：
        str: 识别出的英文文本。
    """
    model = whisper.load_model(model_name)
    result = model.transcribe(audio_path, language='en')
    return result['text']

def translate_text(text, dest_lang="zh-cn"):
    """
    使用Google翻译将英文文本翻译为目标语言（默认中文）。
    参数：
        text (str): 待翻译的英文文本。
        dest_lang (str): 目标语言代码，默认'zh-cn'（简体中文）。
    返回：
        str: 翻译后的文本。
    """
    translator = Translator()
    translated = translator.translate(text, dest=dest_lang)
    return translated.text

def text_to_speech(text, output_audio_path, lang="zh-cn"):
    """
    使用gTTS将文本合成为语音（mp3）。
    参数：
        text (str): 需要合成的文本。
        output_audio_path (str): 输出音频文件路径（mp3）。
        lang (str): 语音语言代码，默认'zh-cn'。
    """
    tts = gTTS(text, lang=lang)
    tts.save(output_audio_path)

def merge_audio_video(video_path, audio_path, output_path):
    """
    使用ffmpeg将新音轨与原视频合成为新mp4文件。
    参数：
        video_path (str): 原视频文件路径。
        audio_path (str): 新音频文件路径（mp3）。
        output_path (str): 输出视频文件路径（mp4）。
    """
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
    subprocess.run(cmd, check=True, shell=True, executable='cmd.exe')

def process_video_file(video_file):
    """
    处理单个视频文件：提取音频、语音识别、翻译、TTS合成、合成新视频。
    参数：
        video_file (str): 输入视频文件路径。
    """
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
    """
    主程序：遍历Input_mp4文件夹下所有MP4文件，批量处理并输出到Output_mp4。
    """
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