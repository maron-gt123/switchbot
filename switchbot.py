import json
import time
import hashlib
import hmac
import base64
import uuid
import requests
import mariadb
import datetime
from config import TOKEN, SECRET, DEVICE_1, DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE, DB_SCHEMA
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
#    version = data["body"]["version"] # バージョン　※必要に感じたら使う

# データベースに接続
    try:
        conn = mariadb.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            database=DB_DATABASE
        )
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                time TIMESTAMP,
                humidity FLOAT,
                temperature FLOAT,
                battery FLOAT
            )
        """)

    # データベースに挿入
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO sensor_data (time, humidity, temperature, battery) VALUES (?, ?, ?, ?)", (current_time, humidity, temperature, battery))
        conn.commit()
        print("データを記録しました")
        cursor.execute(DB_SCHEMA)

    except mariadb.Error as e:
        print(f"Error: {e}")

    finally:
        if conn:
            conn.close()

# 1分ごとにデータを記録
while True:
    record_sensor_data()
    time.sleep(60)  # 60秒待つ
