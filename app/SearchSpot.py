#from flask import Flask, request, jsonify
from .DepartureSpot import DepartureSpot
from .CandidateSpot import CandidateSpot
from typing import Final
import requests
import time as Time
import numpy as np
from datetime import datetime, timedelta
import urllib.request, json



class SearchSpot:
    API_KEY: Final[str] = 'AIzaSyB-UFNTN_spIRoXDKlAr5o2sh5RQRKj1uM' # APIキー
    #@app.route('/api/selected-spot', methods=['POST'])

    """
    const DepPoint = { lat: 35.6586, lng: 139.7454 };  // DepPointとして緯度と経度を設定
    const DepAddress = "1-1 Marunouchi, Chiyoda City, Tokyo";  // 出発地点の住所
    const DepartureTime = { hour: 9, min: 30 };  // 出発時刻を設定
    const ArrivalTime = { hour: 17, min: 30 };  // 到着時刻を設定
    const Budget = 30000;  // 予算を設定
    """
    #@staticmethod
    async def run(self, dep_point, dep_address, departure_time, arrival_time, budget):

        address = dep_address
        lat = dep_point['lat']
        lng = dep_point['lng']
        now_time=datetime.now() #時刻だけ扱うのは不可能なので、現在時刻で年、月、日だけ埋める
        departure_time=now_time.replace(hour=departure_time['hour'],minute=departure_time['min'])
        """
        name="東京駅"
        address="11"
        lat="35.681236"
        lng="139.767125"
        departure_time=datetime.now()
        """
        departure_spot=DepartureSpot(address,lat,lng,departure_time)
        #候補地探索
        type="tourist_attraction"
        candidates=self.search_spot(departure_spot,type)
        
        #出発地から候補地の到着予定時間算出
        self.calculateArrivalTime(departure_spot,candidates,departure_time)
        return self.json_make(candidates)
    
            
    # 候補地を探索
    def search_spot(self,departure_spot :DepartureSpot,type):
        #検索条件定義
        location=str(departure_spot.get_latitude())+", "+str(departure_spot.get_longitude())
        radius=30000 #捜索する半径[m]
        #リクエストURL作成
        endpoint_searchSpot = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
        request_url=f'language={'ja'}&location={location}&radius={radius}&type={type}&key={self.API_KEY}'
        url=endpoint_searchSpot+request_url
        
        # search結果取得
        response = requests.get(url)
        places_data = response.json()
        
        if places_data['status'] == 'OK':
            all_places = []
            all_places.extend(places_data.get('results', []))

            # ページネーション処理
            next_page_token = places_data.get('next_page_token')
            
            # 次のページが存在する場合データを取得
            for i in range(2):
                if next_page_token:
                    Time.sleep(2)  # next_page_tokenが有効になるまで少し待つ（通常数秒）

                    # 次のページのリクエスト
                    next_url = f'{url}&pagetoken={next_page_token}'
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
            sorted_and_filtered_places = sorted(filtered_places_3, key=lambda x: x['rating'],reverse=True)
            
            # レート上位7個の穴場スポットを取得
            candidates=[]
            place_count=len(sorted_and_filtered_places)
            if(place_count>=7):
                hidden_gem = sorted_and_filtered_places[:7]
            else:
                hidden_gem = sorted_and_filtered_places[place_count]
                
            for place in hidden_gem:
                
                name = place.get('name', 'N/A') #スポット名
                address = place.get('vicinity', 'N/A') # 住所
                lat = place['geometry']['location'].get('lat', 'N/A') # 緯度
                lng = place['geometry']['location'].get('lng', 'N/A') # 経度
                evaluate = place.get('rating', '記載情報なし') # 評価
                price_level=place.get('price_level','記載情報なし') # プライスレベル
                
                if 'photos' in place:
                    photo_reference = place['photos'][0]['photo_reference']
                    PHOTO_URL = "https://maps.googleapis.com/maps/api/place/photo"
                    photo_params = {
                        'maxwidth': 300,  # 任意の幅（最大400px）
                        'photoreference': photo_reference,
                        'key': self.API_KEY
                    }
                    photo_url = requests.Request('GET', PHOTO_URL, params=photo_params).prepare().url
                else:
                    photo_url = "No photo available"
                
                candidate_spot=CandidateSpot(name,address,lat,lng,evaluate,photo_url,price_level)
                candidates.append(candidate_spot)
            return candidates
            
    #到着予定時間算出
    def calculateArrivalTime(self,departure_spot, candidates,departure_time):
        endpoint_route: Final[str] = 'https://maps.googleapis.com/maps/api/directions/json?'
        for destination in candidates:
        
            #リクエスト作成
            origin_coordinates=str(departure_spot.get_latitude())+","+str(departure_spot.get_longitude())
            destination_coordinates=str(destination.get_latitude())+","+str(destination.get_longitude())
            mode="driving"
            
            nav_request = 'language=ja&mode={}&origin={}&destination={}&key={}'.format(mode,origin_coordinates,destination_coordinates,self.API_KEY)
            nav_request = urllib.parse.quote_plus(nav_request, safe='=&')
            request = endpoint_route + nav_request

            print('')
            print('=====')
            print('url')
            print(request)
            print('=====')

            #Google Maps Platform Directions APIを実行
            response = urllib.request.urlopen(request).read()

            #結果(JSON)を取得
            directions = json.loads(response)

            #所要時間を取得
            for key in directions['routes']:
                #print(key) # titleのみ参照
                #print(key['legs']) 
                for key2 in key['legs']:
                    print('')
                    print('=====')
                    print(key2['distance']['text'])
                    print(key2['duration']['text'])
                    print('=====')
            
            #所要時間を取得(秒)
            duration_seconds= key2['duration']['value']
            #出発時刻に所要時間を加算
            arrival_time = departure_time + timedelta(seconds=duration_seconds)
            
            print(f"到着予定時刻: {arrival_time.strftime('%H:%M')}")
            
            destination.set_arrivalTime(arrival_time)
            print(destination.get_name())
            print(destination.get_url())
            print(destination.get_evaluate())
            print(destination.get_arrivalTime())
            
            
    # json形式に落とし込む
    def json_make(self,candidates):
        spot_list=[]
        for place in candidates:
            spot={'name': place.get_name(), 'address': place.get_address(),
                'evaluate': place.get_evaluate(),'lat':str(place.get_latitude()),'lng': str(place.get_longitude()),
                'distanceTime':{"hour": place.get_arrivalTime().hour,"min": place.get_arrivalTime().minute},
                'url': place.get_url(),'price_level': place.get_price_level()
                }
            spot_list.append(spot)
        return spot_list
        print(spot_list)  
        