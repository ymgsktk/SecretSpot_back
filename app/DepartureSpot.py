import app.Spot as Spot
from datetime import datetime

class PlaceOfDeparture(Spot):
    def __init__(self, name: str, address: str, latitude: str, longitude:str, departure_time: datetime) -> None:
        # 親クラス(Place)の属性を初期化
        super().__init__(name, address, latitude, longitude)
        
        self.departure_time=departure_time #出発時刻
        
    def getDepartureTime(self):
        return self.departure_time
    
    def setDepartureTime(self,Departure_time: datetime):
        self.departure_time=Departure_time