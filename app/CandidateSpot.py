from .Spot import Spot
from datetime import datetime

# スポット候補地を表すクラス
class CandidateSpot(Spot):
    def __init__(self, name: str, address: str, latitude: str, longitude: str, evaluate: int, url: str, price_level, information_url: str,explanation: str) -> None:
        # 親クラス(Place)の属性を初期化
        super().__init__(address, latitude, longitude)
        self.evaluate=evaluate
        self.url=url 
        self.price_level=price_level
        self.name=name
        self.information_url=information_url
        self.explanation=explanation
        
    def set_arrivalTime(self,estimated_arrival_time: datetime):
        self.estimated_arrival_time=estimated_arrival_time    
        
    def get_arrivalTime(self):
        return self.arrival_time
    
    def set_arrivalTime(self,arrival_time: datetime):
        self.arrival_time=arrival_time
    
    def get_evaluate(self):
        return self.evaluate
    
    def get_url(self)  -> str:
        return self.url
    
    def get_price_level(self):
        return self.price_level
    
    def get_name(self)  -> str:
        return self.name
    
    def set_name(self, name: str) -> None:
        self.name = name
        
    def set_information_url(self, information_url: str):
        self.information_url=information_url
    
    def get_information_url(self)  -> str:
        return self.information_url
    def get_explanation(self)  -> str:
        return self.explanation