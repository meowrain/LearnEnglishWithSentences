from dotenv import load_dotenv
import requests
import hashlib
import time
import uuid
import os
# 加载.env文件中的环境变量
load_dotenv()
appKey = os.getenv("youdao_appKey")
appSecret = os.getenv("youdao_appSecret")


def getInput(input):
    if input is None:
        return input
    inputLen = len(input)
    return input if inputLen <= 20 else input[0:10] + str(inputLen) + input[inputLen - 10:inputLen]


def calculateSign(appKey, appSecret, q, salt, curtime):
    strSrc = appKey + getInput(q) + salt + curtime + appSecret
    return encrypt(strSrc)


def encrypt(strSrc):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(strSrc.encode('utf-8'))
    return hash_algorithm.hexdigest()


def fetch_youdao_definition(word):
    salt = str(uuid.uuid1())
    curtime = str(int(time.time()))
    sign = calculateSign(appKey, appSecret, word, salt, curtime)
    url = f"https://openapi.youdao.com/api/?q={word}&from=auto&to=auto&appKey={appKey}&salt={salt}&sign={sign}&signType=v3&curtime={curtime}"
    response = requests.get(url)
    data = response.json()
    # print(data)
    basic_data = data.get('basic', {})
    explains = basic_data.get('explains', [])
    explain = ""
    explain += f'音标：[{basic_data.get("us-phonetic", [])}]\t'
    for mean in explains:
        explain += mean
    return explain