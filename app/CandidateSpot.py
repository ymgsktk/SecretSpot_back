from Spot import Spot
from datetime import datetime

# スポット候補地を表すクラス
class CandidateSpot(Spot):
    def __init__(self, name: str, address: str, latitude: str, longitude: str, evaluate: int, url: str, price_level) -> None:
        # 親クラス(Place)の属性を初期化
        super().__init__(name, address, latitude, longitude)
        self.evaluate=evaluate
        self.url=url 
        self.price_level=price_level
        #self.explanation=explanation
        
    def set_arrivalTime(self,estimated_arrival_time: datetime):
        self.estimated_arrival_time=estimated_arrival_time    
        
    def get_arrivalTime(self):
        return self.arrival_time
    
    def set_arrivalTime(self,arrival_time: datetime):
        self.arrival_time=arrival_time
    
    def get_evaluate(self):
        return self.evaluate
    
    def get_url(self):
        return self.url
    def get_price_level(self):
        return self.price_level