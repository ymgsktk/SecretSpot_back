from flask import Flask, request, jsonify
import app.DepartureSpot as DepartureSpot
from typing import Final
import requests
import time
import numpy as np

class SearchSpot:
    
    
    @app.route('/api/selected-spot', methods=['POST'])
    def receive_departure_place(self):
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data received"}), 400
        
        self.searchSpot(data)
        name = data.get('name')
        address = data.get('address')
        lat = data.get('lat')
        lng = data.get('lng')
        departure_time=data.get('departure')
        Departure_spot=DepartureSpot(name,address,lat,lng,departure_time)
        self.searchSpot(Departure_spot)
        

    
    def searchSpot(Departure_point :DepartureSpot):
        location=DepartureSpot.get_latitude()+", "+DepartureSpot.get_longitude()
        radius=5000
        API_KEY: Final[str] = '' # APIキー
        base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
        request_url=f'location={location}&radius={radius}&type={'tourist_attraction'}&key={API_KEY}'
        url=base_url+request_url
        
        # search結果取得
        response = requests.get(base_url)
        places_data = response.json()
        
        if places_data['status'] == 'OK':
            all_places = []
            all_places.extend(places_data.get('results', []))

            # ページネーション処理
            next_page_token = places_data.get('next_page_token')
            
            # 次のページが存在する場合データを取得
            for i in range(2):
                if next_page_token:
                    time.sleep(2)  # next_page_tokenが有効になるまで少し待つ（通常数秒）

                    # 次のページのリクエスト
                    next_url = f'{base_url}&pagetoken={next_page_token}'
                    response = requests.get(next_url)
                    next_data = response.json()

                    # 新しいページの結果をリストに追加
                    all_places.extend(next_data.get('results', []))

                    # 新しいnext_page_tokenを取得
                    next_page_token = next_data.get('next_page_token')
                    
            # 総評価数の取得
            user_ratings_total_list = [place['user_ratings_total'] for place in all_places]
            
            # 第1四分位数Q1を取得
            Q1 = np.percentile(user_ratings_total_list, 25)
            Q1 = float(Q1)
            
            # レート3.5以上、第1四分位範囲に入るデータを取得
            
            #↓　過去に選んだスポットを除外する
            #filtered_places_1 = [place for place in all_places if place['vicinity'] != address]
            
            filtered_places_2 = [place for place in all_places if place['rating']>=3.5]
            filtered_places_3 = [place for place in filtered_places_2 if place['user_ratings_total']<=Q1]

            # レート順に並べ替え
            sorted_and_filtered_places = sorted(filtered_places_2, key=lambda x: x['rating'],reverse=True)
            
            # レート上位7個の穴場スポットを取得
            hidden_gem = sorted_and_filtered_places[:7]
            for place in hidden_gem:
                
                name = place.get('name', 'N/A') #スポット名
                address = place.get('vicinity', 'N/A') # 住所
                lat = place['geometry']['location'].get('lat', 'N/A') # 緯度
                lng = place['geometry']['location'].get('lng', 'N/A') # 経度
                rating = place.get('rating', 'N/A') # 評価
            if 'photos' in place:
                photo_reference = place['photos'][0]['photo_reference']
                PHOTO_URL = "https://maps.googleapis.com/maps/api/place/photo"
                photo_params = {
                    'maxwidth': 400,  # 任意の幅（最大400px）
                    'photoreference': photo_reference,
                    'key': API_KEY
                }
                
                photo_url = requests.Request('GET', PHOTO_URL, params=photo_params).prepare().url
            else:
                photo_url = "No photo available"

        
