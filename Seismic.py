
class Seismic:
    #self.seismic_zone = ""

    def __init__(self, seismic_classification: int, zone : str, return_period : int) -> None:
        self.seismic_zone = zone
        self.zone = zone
        self.seismic_classification = seismic_classification
        if seismic_classification == 0:
            self.seismic_class_str = "내진특등급"
        elif  seismic_classification == 1:  
            self.seismic_class_str = "내진I등급"
        elif  seismic_classification == 2:  
            self.seismic_class_str = "내진II등급"  

        seismiczone1 = ["서울", "인천", "대전", "부산", "대구", "울산", "광주", "세종",
                        "경기", "충북", "충남", "경북", "경남", "전북", "전남",
                        "영월", "정선", "삼척", "강릉", "동해", "원주", "태백"]
        seismiczone2 = ["홍천", "철원", "화천", "횡성", "평창", "양구", "인제", 
                        "고성", "양양", "춘천", "속초", "제주"]
        if zone in seismiczone1:
            self.seismic_zone = "I"
            self.seismic_zone_coeff =0.11
            
        elif zone in seismiczone2:
            self.seismic_zone = "II"
            self.seismic_zone_coeff =0.07
            
        else:
            self.seismic_zone_coeff = 0.00 
        
        if return_period == 50:
            self.risk_factor = 0.40
        elif return_period == 100:
            self.risk_factor = 0.57
        elif return_period == 200:
            self.risk_factor = 0.73
        elif return_period == 500:
            self.risk_factor = 1.0
        elif return_period == 1000:
            self.risk_factor = 1.40
        elif return_period == 2400:
            self.risk_factor = 2.00
        elif return_period == 4800:
            self.risk_factor = 2.60

    def __str__(self):
        return f"""내진등급: {self.seismic_class_str}  위험도계수 : {self.risk_factor:.2f}
지진구역 : {self.seismic_zone} ({self.zone}) 지진구역계수: {self.seismic_zone_coeff:.2f} """
                    
if __name__ == "__main__":
    seismic = Seismic(seismic_classification=1,zone="홍천",return_period=1000)
    print(seismic.__dict__)
    print(seismic.__str__())
