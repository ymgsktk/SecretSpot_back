from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import asyncio
from dotenv import load_dotenv
import os
import sys
sys.path.append('../')
#以下のappからspotに変更する
from app import scraping_main
from spot import motoki

from config import Localization

load_dotenv()
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": os.environ.get("FRONT_API_URL")}})

@app.route("/")
def index():
	return "Welcome to ASEticle."

@app.route('/api/execute', methods=['POST'])
# リクエストボディに複数のパラメータを含む場合、POSTメソッドのほうがデータの扱いがシンプルで安全です。（ChatGPT）
def execute_route():
    # リクエストデータのJSONを取得
    data = request.get_json()
    
    # 必須パラメータがすべて存在するか確認
    if not all(key in data for key in ['DepPoint', 'DepartureTime', 'ArrivalTime', 'Budget']):
        return jsonify({"error": Localization.get('config.routes.bad_request')}), 400

    # パラメータを取得
    dep_point = data['DepPoint']
    departure_time = data['DepartureTime']
    arrival_time = data['ArrivalTime']
    budget = data['Budget']

    # 非同期関数の呼び出し
    result = asyncio.run(motoki(dep_point, departure_time, arrival_time, budget))

    # JSONレスポンスとして返す
    return jsonify(result)


	if request.args.get('params') is not None:
		params = request.args.get('params')
	else:
		return jsonify({"error": Localization.get('config.routes.bad_request')}), 400

	result = asyncio.run(scraping_main(params))

	return result

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)