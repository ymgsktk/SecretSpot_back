from typing import Final
from datetime import datetime, timedelta
import urllib.request, json
import app.DepartureSpot as DepartureSpot
import app.CandidateSpot as CandidateSpot

class Distance:
    
    # API関連情報
    endpoint: Final[str] = 'https://maps.googleapis.com/maps/api/directions/json?'
    api_key: Final[str] = 'AIzaSyB-UFNTN_spIRoXDKlAr5o2sh5RQRKj1uM'
    
    def __init__(self,departureTime,origin: DepartureSpot,destination: CandidateSpot):
        self.departureTIme=departureTime
        self.origin=origin
        self.destination=destination
        
    def calculateDistance(self):
        
        #リクエスト作成
        origin_coordinates=self.origin.get_latitude()+","+self.origin.get_longitude()
        destination_coordinates=self.destination.get_latitude()+","+self.destination.get_longitude()
        mode="driving"
        
        nav_request = 'language=ja&mode={}&origin={}&destination={}&key={}'.format(mode,origin_coordinates,destination_coordinates,self.api_key)
        nav_request = urllib.parse.quote_plus(nav_request, safe='=&')
        request = self.endpoint + nav_request

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
                print(key2['duration']['value'])
                print(key2['duration']['text'])
                print('=====')
        current_time = datetime.now()
        duration_seconds= key2['duration']['value']
        arrival_time = current_time + timedelta(seconds=duration_seconds)
        print(f"到着予定時刻: {arrival_time.strftime('%Y-%m-%d %H:%M:%S')}")
        

    
def main():
    origin = "35.681236,139.767125"
    destination = "34.985849,135.758766"
    departureTime = datetime.now()
    distance=Distance(departureTime,origin,destination)
    distance.calculateDistance()
if __name__ == "__main__":
    main()