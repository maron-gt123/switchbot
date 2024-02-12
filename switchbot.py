import json
import time
import hashlib
import hmac
import base64
import uuid
import requests
from config import TOKEN, SECRET, DEVICE_1
from rich import print

nonce = uuid.uuid4()
t = f"{time.time() * 1000:.0f}"
#t = int(round(time.time() * 1000))
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

api_endpoint = f'https://api.switch-bot.com/v1.1/devices/{DEVICE_1}/status'

res = requests.get(api_endpoint, headers=headers)

data = res.json()

humidity = data["body"]["humidity"]
temperature = data["body"]["temperature"]
battery = data["body"]["battery"]
version = data["body"]["version"]

print(humidity)
print(temperature)
print(battery)
print(version)
