import app.Spot as Spot
from datetime import datetime

# スポット候補地を表すクラス
class PlaceOfCandidate(Spot):
    def __init__(self, name: str, address: str, latitude: str, longitude: str, evaluate: int, url: str) -> None:
        # 親クラス(Place)の属性を初期化
        super().__init__(name, address, latitude, longitude)
        self.evaluate=evaluate
        #self.url=url 
        #self.explanation=explanation
        
    def setEstimatedArrivalTime(self,estimated_arrival_time: datetime):
        self.estimated_arrival_time=estimated_arrival_time    
        
    def getEstimatedArrivalTime(self):
        return self.estimated_arrival_time
    
    def setEstimatedArrivalTime(self,estimated_arrival_time: datetime):
        self.estimated_arrival_time=estimated_arrival_time
    
    def getEvaluation(self):
        return self.evaluate
    