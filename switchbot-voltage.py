import json
import time
import hashlib
import hmac
import base64
import uuid
import requests
from config import TOKEN, SECRET, DEVICE_2, DEVICE_CM_2, INFLUXDB_URL, INFLUXDB_TOKEN, INFLUXDB_ORG, INFLUXDB_BUCKET
from rich import print
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# InfluxDBの接続
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

# データをInfluxDBに書き込む関数
def write_to_influxdb(device, voltage, weight, electricityOfDay, electricCurrent, version):
    # 電圧、電力、デバイス使用時間、電流を浮動小数点数に変換
    voltage = float(voltage)
    weight = float(weight)
    electricityOfDay = float(electricityOfDay)
    electricCurrent = float(electricCurrent)
    point = Point("device_data").tag("device", device).field("voltage", voltage).field("weight", weight).field("electricityOfDay", electricityOfDay).field("electricCurrent", electricCurrent).field("version", version)
    write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)

nonce = uuid.uuid4()
t = f"{time.time() * 1000:.0f}"
string_to_sign = '{}{}{}'.format(TOKEN, t, nonce)
string_to_sign = bytes(string_to_sign, 'utf-8')
secret = bytes(SECRET, 'utf-8')
sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())

# Build api header JSON
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

#device = data["body"]['deviceId'] #デバイスID
device = DEVICE_CM_2 #デバイス名
voltage = data["body"]["voltage"] # 電圧
weight = data["body"]["weight"] # 電力
electricityOfDay = data["body"]["electricityOfDay"] # デバイス使用時間
electricCurrent =  data["body"]["electricCurrent"] # 電流
version = data["body"]["version"] # バージョン

# デバック用
#print("デバイス名")
#print(device)
#print("電圧")
#print(voltage)
#print("電力")
#print(weight)
#print("デバイス使用時間")
#print(electricityOfDay)
#print("電流")
#print(electricCurrent)
#print("バージョン")
#print(version)

# データをInfluxDBに書き込む
write_to_influxdb(device, voltage, weight, electricityOfDay, electricCurrent, version)
print("書き込みました")
