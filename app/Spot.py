
# スポットを表現するクラス(親クラス)
class Spot:
    
    def __init__(self, address: str, latitude: str,longitude: str) -> None:
        
        self.address=address #住所
        self.latitude=latitude # 緯度
        self.longitude=longitude # 経度
    
    def get_address(self) -> str:
        return self.address
    
    def set_address(self, address: str) -> None:
        self.address = address
    
    def get_latitude(self) -> str:
        return self.latitude
    
    def set_latitude(self, latitude: str) -> None:
        self.latitude = latitude
    
    def get_longitude(self) -> str:
        return self.longitude
    
    def set_longitude(self, longitude: str) -> None:
        self.longitude = longitude
    
    
    
    
    
    