import json
import time
import hashlib
import hmac
import base64
import uuid
import requests
from config import TOKEN, SECRET, DEVICE_2
from rich import print

nonce = uuid.uuid4()
t = f"{time.time() * 1000:.0f}"
string_to_sign = '{}{}{}'.format(TOKEN, t, nonce)

string_to_sign = bytes(string_to_sign, 'utf-8')
secret = bytes(SECRET, 'utf-8')
sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())

#Build api header JSON
headers = {
    'Authorization': TOKEN,
    'sign': str(sign, "utf-8"),
    't': t,
    'nonce': str(nonce),
    'Content-Type': 'application/json',
    "charset": 'utf8'
}

api_endpoint = f'https://api.switch-bot.com/v1.1/devices/{DEVICE_2}/status'

res = requests.get(api_endpoint, headers=headers)

data = res.json()

device = data["body"]['deviceId'] #デバイスID
voltage = data["body"]["voltage"] # 電圧
weight = data["body"]["weight"] # 電力
electricityOfDay = data["body"]["electricityOfDay"] # デバイス使用時間
electricCurrent =  data["body"]["electricCurrent"] /10 # 電流
version = data["body"]["version"] # バージョン

print("デバイス名")
print(device)
print("電圧")
print(voltage)
print("電力")
print(weight)
print("デバイス使用時間")
print(electricityOfDay)
print("電流")
print(electricCurrent)
print("バージョン")
print(version)
