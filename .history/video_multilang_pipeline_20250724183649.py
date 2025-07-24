import os
import subprocess
import tempfile
from googletrans import Translator
from gtts import gTTS
import whisper
from moviepy import AudioFileClip
import shutil
from tqdm import tqdm
import time
import threading
import torch
import hashlib
import uuid
import requests
import json

# 将 ffmpeg/bin 加入 PATH
ffmpeg_bin = os.path.abspath("ffmpeg/bin")
os.environ["PATH"] = ffmpeg_bin + os.pathsep + os.environ.get("PATH", "")

INPUT_DIR = 'Input_mp4'
OUTPUT_DIR = 'Output_mp4'
TEMP_DIR = 'temp'

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)
YOUDAO_URL = 'https://openapi.youdao.com/api'
APP_KEY = '5b776e062bbdc974'
APP_SECRET = '9XhyrhxDf33Zf7zsar52FXNYDBLjbrtY'

def extract_audio_from_video(video_path, audio_path):
    """
    用moviepy从视频文件中提取音频并保存为mp3格式。
    参数：
        video_path (str): 输入视频文件路径。
        audio_path (str): 输出音频文件路径（mp3）。
    """
    audio_clip = AudioFileClip(video_path)
    audio_clip.write_audiofile(audio_path)

def transcribe_audio(audio_path, model_name="base"):
    """
    使用OpenAI Whisper模型将音频文件转为英文文本。
    参数：
        audio_path (str): 输入音频文件路径（mp3）。
        model_name (str): Whisper模型名称，可选'tiny', 'base', 'small', 'medium', 'large'。
    返回：
        str: 识别出的英文文本。
    """
    print(f"正在使用{model_name}模型进行语音转文字...")
    print(f"音频文件路径: {audio_path}")
    stop_flag = threading.Event()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Whisper将使用设备: {device.upper()}（{'GPU加速' if device == 'cuda' else 'CPU'}）")
    def progress_bar():
        with tqdm(desc="Whisper转录中", ncols=80, bar_format='{l_bar}{bar}| {elapsed}', total=0) as pbar:
            while not stop_flag.is_set():
                pbar.update(1)
                time.sleep(0.1)
    t = threading.Thread(target=progress_bar)
    t.start()
    try:   
        model = whisper.load_model(model_name, device=device)
        result = model.transcribe(audio_path, language='en')
    finally:
        stop_flag.set()
        t.join()
    return result['text']

def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()

def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]

def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)

def connect(q, source_lang='auto', target_lang='zh-CHS'):
    data = {}
    data['from'] = source_lang
    data['to'] = target_lang
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['q'] = q
    data['salt'] = salt
    data['sign'] = sign
    data['vocabId'] = ""
    response = do_request(data)
    contentType = response.headers['Content-Type']
    if contentType == "audio/mp3":
        return "[音频返回，未处理]"
    else:
        result = response.content.decode('utf-8')
        result = json.loads(result)
        if 'errorCode' in result and result['errorCode'] == '0':
            return ''.join(result['translation'])
        else:
            print("错误代码：", result.get('errorCode', '未知错误'))
            return "[翻译错误]"

def translate_text(text, dest_lang="zh-cn"):
    """
    使用有道翻译API将英文文本翻译为目标语言（默认中文）。
    参数：
        text (str): 待翻译的英文文本。
        dest_lang (str): 目标语言代码，默认'zh-cn'（简体中文）。
    返回：
        str: 翻译后的文本。
    """
    # 有道API的中文代码为'zh-CHS'
    lang_map = {"zh-cn": "zh-CHS", "zh": "zh-CHS", "en": "en"}
    yd_lang = lang_map.get(dest_lang.lower(), dest_lang)
    return connect(text, source_lang='en', target_lang=yd_lang)

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
    # 清空temp文件夹
    # for f in os.listdir(TEMP_DIR):
    #     fp = os.path.join(TEMP_DIR, f)
    #     if os.path.isfile(fp):
    #         os.remove(fp)
    #     elif os.path.isdir(fp):
    #         shutil.rmtree(fp)
            
    audio_path = os.path.join(TEMP_DIR, f"{base}_audio.mp3")
    # print(f"[1/5] 正在提取音频: {video_file}")
    # extract_audio_from_video(video_file, audio_path)

    # print(f"[2/5] 正在语音转文字...")
    # text = transcribe_audio(audio_path)
    # print("识别文本：", text[:100], "...")
    # # 保存英文文本
    # en_txt_path = os.path.join(TEMP_DIR, f"{base}_en.txt")
    # with open(en_txt_path, 'w', encoding='utf-8') as f:
    #     f.write(text)

    print(f"[3/5] 正在翻译为中文...")
    # 从文件读取英文文本
    en_txt_path = os.path.join(TEMP_DIR, f"{base}_en.txt")
    with open(en_txt_path, 'r', encoding='utf-8') as f:
        text = f.read()
    translated = translate_text(text)
    print("翻译结果：", translated[:100], "...")
    # 保存中文文本
    zh_txt_path = os.path.join(TEMP_DIR, f"{base}_zh.txt")
    with open(zh_txt_path, 'w', encoding='utf-8') as f:
        f.write(translated)

    output_audio = os.path.join(TEMP_DIR, f"{base}_zh.mp3")
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