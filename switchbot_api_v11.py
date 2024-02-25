import json
import time
import hashlib
import hmac
import base64
import uuid
import requests
from config import TOKEN, SECRET
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

api_endpoint = f'https://api.switch-bot.com/v1.1/devices'

res = requests.get(api_endpoint, headers=headers)

data = res.json()

print("デバイスリスト")
print(data)
