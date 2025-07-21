import json
import os

import pysrt
import sys
import uuid
import requests
import hashlib
from importlib import reload

import time

reload(sys)

YOUDAO_URL = 'https://openapi.youdao.com/api'
APP_KEY = '5b776e062bbdc974'
APP_SECRET = '9XhyrhxDf33Zf7zsar52FXNYDBLjbrtY'


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


def connect(q,source_lang='auto', target_lang='zh-CHS'):

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
    data['vocabId'] = "您的用户词表ID"

    response = do_request(data)
    contentType = response.headers['Content-Type']
    if contentType == "audio/mp3":
        millis = int(round(time.time() * 1000))
        filePath = "合成的音频存储路径" + str(millis) + ".mp3"
        fo = open(filePath, 'wb')
        fo.write(response.content)
        fo.close()
    else:
        result= response.content.decode('utf-8')
        result =json.loads(result)
        if 'errorCode' in result and result['errorCode'] == '0':
            return ''.join(result['translation'])
        else:
            print("错误代码：", result.get('errorCode', '未知错误'))


if __name__ == "__main__":
    for file in os.listdir('Subs'):
        if file.endswith('.srt'):
            print(f"Processing file: {file}")
            if not file.endswith('.eng.srt'):
                print(f"Skipping file: {file} (not an English subtitle file)")
                continue
            new_file_name = file.replace('.eng.srt', '.zh&eng.srt')
            new_file_path = os.path.join('Subs', new_file_name)
            if os.path.exists(new_file_path):
                print(f"已存在: {new_file_name}，跳过。")
                continue
            # Load the SRT file
            subs = pysrt.open(os.path.join('Subs', file))
            print(f"Translated subtitle: ")
            # Print each subtitle
            for sub in subs:
                time.sleep(1)
                trans = connect(sub.text, source_lang='en', target_lang='zh-CHS')
                sub.text = sub.text + "\n" + trans
                print(sub.text)
            # Save the modified subtitles to a new SRT file
            new_file_name = file.replace('.eng.srt', '.zh&eng.srt')
            subs.save(os.path.join('Subs', new_file_name), encoding='utf-8')
            print(f"Saved translated subtitles to: {new_file_name}")