from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

# サンプルの観光スポットデータ（本来はデータベースや外部APIから取得）
spots = [
    {
        "Name": "Tokyo Tower",
        "address": "4 Chome-2-8 Shibakoen, Minato City, Tokyo",
        "Evaluate": 4.5,
        "lat": "35.6586",
        "lng": "139.7454",
        "priceLevels": 3,
        "DistanceTime": 30  # 出発地点からの時間（例）
    },
    {
        "Name": "Sensoji Temple",
        "address": "2 Chome-3-1 Asakusa, Taito City, Tokyo",
        "Evaluate": 4.7,
        "lat": "35.7148",
        "lng": "139.7967",
        "priceLevels": 2,
        "DistanceTime": 40  # 出発地点からの時間（例）
    }
]

@app.route('/get_spots', methods=['GET'])
def get_spots():
    # クエリパラメータの取得
    dep_point = request.args.get('DepPoint')
    departure_time = request.args.get('DepartureTime')
    arrival_time = request.args.get('ArrivalTime')
    budget = request.args.get('Budget')

    # パラメータがない場合のエラーハンドリング
    if not (dep_point and departure_time and arrival_time and budget):
        return jsonify({"error": "Missing parameters"}), 400

    # ロジックの簡略化：サンプルのデータをそのまま返す（実際には条件によってフィルタリング）
    result = []
    for spot in spots:
        # 例えば、予算や時間の条件に合致するものをフィルタリングする（簡易版）
        if int(budget) >= spot['priceLevels']:
            result.append(spot)

    # 結果のJSONを返す
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
