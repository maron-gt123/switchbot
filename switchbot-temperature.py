import json
import time
import hashlib
import hmac
import base64
import uuid
import requests
from config import TOKEN, SECRET, DEVICE_1, INFLUXDB_URL, INFLUXDB_TOKEN, INFLUXDB_ORG, INFLUXDB_BUCKET
from rich import print
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# InfluxDBの接続
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

# データをInfluxDBに書き込む関数
def write_to_influxdb(device, humidity, temperature, battery, version):
    point = Point("device_data").tag("device", device).field("humidity", humidity).field("temperature", temperature).field("battery", battery).field("version", version)
    write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)

while True:
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

    api_endpoint = f'https://api.switch-bot.com/v1.1/devices/{DEVICE_1}/status'

    res = requests.get(api_endpoint, headers=headers)

    data = res.json()

    device = data["body"]['deviceId'] #デバイスID
    humidity = data["body"]["humidity"] # 湿度計
    temperature = data["body"]["temperature"] # 温度計
    battery = data["body"]["battery"] # バッテリ
    version = data["body"]["version"] # バージョン

    # デバック用
    #print("デバイス名")
    #print(device)
    #print("湿度")
    #print(humidity)
    #print("温度")
    #print(temperature)
    #print("バッテリ")
    #print(battery)
    #print("バージョン")
    #print(version)

    # データをInfluxDBに書き込む
    write_to_influxdb(device, humidity, temperature, battery, version)
    print("書き込みました")
    # 5分待機
    time.sleep(300)  # 300秒 = 5分
