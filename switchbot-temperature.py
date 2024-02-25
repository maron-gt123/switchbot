import json
import time
import hashlib
import hmac
import base64
import uuid
import requests
import datetime
from influxdb import InfluxDBClient
from config import TOKEN, SECRET, DEVICE_1, DB_HOST, DB_USER, DB_PASSWORD, DB_PORT, DB_DATABASE
from rich import print

def record_sensor_data():
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

    humidity = data["body"]["humidity"] # 湿度計
    temperature = data["body"]["temperature"] # 温度計
    battery = data["body"]["battery"] # バッテリ
    version = data["body"]["version"] # バージョン

# データベースに接続
    try:
        client = InfluxDBClient(
            username=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_DATABASE
        )
        json_body = [
            {
                "measurement": "sensor_data",
                "tags": {},
                "fields": {
                    "humidity": humidity,
                    "temperature": temperature,
                    "battery": battery,
                    "version": version
                }
            }
        ]
        client.write_points(json_body)
        print("データをInfluxDBに記録しました")
    except Exception as e:
        print(f"Error: {e}")

# 5分ごとにデータを記録
while True:
    record_sensor_data()
    time.sleep(300)  # 300秒待つ
