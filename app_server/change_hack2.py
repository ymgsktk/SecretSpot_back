from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import asyncio
from dotenv import load_dotenv
import os
import sys
sys.path.append('../')
#以下のappからspotに変更する
#from app import scraping_main
#from spot import spot_motoki

from localization import Localization

load_dotenv()
app = Flask(__name__)

FRONT_URL = "http://localhost:3000"
CORS(app, resources={r"/api/*": {"origins": FRONT_URL}})

@app.route("/")
def index():
	return "Welcome to ASEticle."

@app.route('/api/execute', methods=['POST'])
# リクエストボディに複数のパラメータを含む場合、POSTメソッドのほうがデータの扱いがシンプルで安全です。（ChatGPT）
def execute_route():
    # リクエストデータのJSONを取得
    data = request.get_json()
    
    # 必須パラメータがすべて存在するか確認
    if not all(key in data for key in ['DepPoint', 'DepAddress', 'DepartureTime', 'ArrivalTime', 'Budget']):
        return jsonify({"error": Localization.get('app_server.routes.bad_request')}), 400

    # パラメータを取得
    dep_point = data['DepPoint']
    dep_address = data['DepAddress']
    departure_time = data['DepartureTime']
    arrival_time = data['ArrivalTime']
    budget = data['Budget']

    # 非同期関数の呼び出し
    result = asyncio.run(spot_motoki(dep_point, dep_address, departure_time, arrival_time, budget))

    # JSONレスポンスとして返す
    return jsonify(result)


# ダミーデータを返すspot_motoki関数
async def spot_motoki(dep_point, dep_address, departure_time, arrival_time, budget):
    # ダミーデータとしてスポット情報を返す
    return [
        {
            "Name": "Tokyo Tower",
            "address": "4 Chome-2-8 Shibakoen, Minato City, Tokyo",
            "Evaluate": 4.5,
            "lat": "35.6586",
            "lng": "139.7454",
            "priceLevels": 3,
            "DistanceTime (hour)": 1,
            "DistanceTime (minute)": 30 
        },
        {
            "Name": "Shinjuku Gyoen National Garden",
            "address": "11 Naitomachi, Shinjuku City, Tokyo",
            "Evaluate": 4.7,
            "lat": "35.6852",
            "lng": "139.7100",
            "priceLevels": 2,
            "DistanceTime (hour)": 0,
            "DistanceTime (minute)": 45   
        }
    ]


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)