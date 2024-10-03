from Spot import Spot
from datetime import datetime

class DepartureSpot(Spot):
    def __init__(self, address: str, latitude: str, longitude:str, departure_time: datetime) -> None:
        # 親クラス(Place)の属性を初期化
        super().__init__(address, latitude, longitude)
        
        self.departure_time=departure_time #出発時刻
        
        
    def get_departureTime(self):
        return self.departure_time
    
    def set_departureTime(self,Departure_time: datetime):
        self.departure_time=Departure_time