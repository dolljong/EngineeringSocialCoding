import math
import numpy as np
from scipy import interpolate #직선보간법
#--------------------------------------------------
#    직사각형 단철근보 단면검토 (도로교설계기준 2012)
#--------------------------------------------------
class Sec_back:

    def __init__(self, datalist, datalist1, datalist2):
        self.fck = datalist[0]           #fck설정
        self.fy = datalist[1]            #fy설정
        self.Øc = datalist[2]            #Øc설정
        self.Øs = datalist[3]            #Øs설정
        self.Mu = datalist[4]            #Mu설정
        self.Vu = datalist[5]            #Vu설정  
        self.Nu = datalist[6]            #Nu설정
        self.Ms = datalist[7]            #Ms설정
        self.H = datalist[8]             #단면두께 설정
        self.B = datalist[9]             #단면 폭 설정
        self.AsDia1 = datalist1[0]       #1단 철근직경 설정
        self.AsNum1 = datalist1[1]       #1단 철근개수 설정
        self.Dc1 = datalist1[2]          #1단 피복두께 설정
        self.AsDia2 = datalist1[3]       #2단 철근직경 설정
        self.AsNum2 = datalist1[4]       #2단 철근개수 설정
        self.Dc2 = datalist1[5]          #2단 피복두께 설정
        self.AsDia3 = datalist1[6]       #3단 철근직경 설정
        self.AsNum3 = datalist1[7]       #3단 철근개수 설정
        self.Dc3 = datalist1[8]          #3단 피복두께 설정
        self.AvDia = datalist2[0]        #전단철근 직경
        self.AvLeg = datalist2[1]        #전단철근 다리개수
        self.AvSpace = datalist2[2]      #전단철근 배치간격
        self.sg = datalist2[3]           #복부스트럿 각도 입력방법 선택
        self.seta = datalist2[4]         #복부스트럿 각도 직접입력값
        self.α = datalist2[5]            #전단철근과 주철근 각도(주철근으로부터 시계방향각도)
        self.δ = 1                                #재분배 모멘트율 설정
        self.Es = 200000                          #철근의 탄성계수
        self.Mun = self.Mu*1000000
        self.Vun = self.Vu*1000
        self.Nun = self.Nu*1000
        self.αcc = 0.85                           #유효계수
        if self.fy <= 300 :
            self.rebarid = "D"
        else :
            self.rebarid = "H"
        self.fcd =  self.fck * self.Øc * self.αcc #콘크리트 설계압축강도
        if self.fck < 40 :                        #콘크리트 평균압축강도
            self.fcm = self.fck + 4
        elif self.fck >= 60 :
            self.fcm = self.fck + 6
        else :
            self.fcm = 4 + (self.fck - 40) / 10  
        self.Ec = 0.077 * 2500**1.5 * self.fcm**(1/3)  #콘크리트 탄성계수
        if 1.2+1.5*((100-self.fck)/60)**4 >= 2 :       #상승곡선부의 형상을 나타내는 지수
            self.nε = 2
        else :
            self.nε = 1.2 + 1.5*((100-self.fck)/60)**4
        if 0.002 + ((self.fck-40)/100000) <= 0.002 :   #최대응력에 처음 도달했을때의 변형률
            self.εco = 0.002
        else :
            self.εco = 0.002 + ((self.fck-40)/100000)
        if 0.0033 - ((self.fck-40)/100000) >= 0.0033 : #콘크리트 극한변형율
            self.εcu = 0.0033
        else :
            self.εcu = 0.0033 - ((self.fck-40)/100000)
        self.fcklist = [40, 50, 60, 70, 80, 90]
        self.alpalist = [0.8, 0.78, 0.72, 0.67, 0.63, 0.59]
        self.betalist = [0.4, 0.4, 0.38, 0.37, 0.36, 0.35]
        self.etalist = [1.0, 0.97, 0.95, 0.91, 0.87, 0.84]        
        if self.fck <= 40 :                             #압축합력의 응력계수 α    
            self.α = self.alpalist[0]
        elif self.fck >=90 :
            self.α = self.alpalist[5]
        else :
            self.fα = interpolate.interp1d(self.fcklist,self.alpalist)
            self.α = self.fα(self.fck)
        if self.fck <= 40 :                             #압축합력의 작용점 위치계수 β
            self.β = self.betalist[0]
        elif self.fck >=90 :
            self.β = self.betalist[5]
        else :
            self.fβ = interpolate.interp1d(self.fcklist,self.betalist)
            self.β = self.fβ(self.fck)
        if self.fck <= 40 :                             #등가사각형 응력블록의 크기계수 η
            self.η = self.etalist[0]
        elif self.fck >=90 :
            self.η = self.etalist[5]
        else :
            self.fη = interpolate.interp1d(self.fcklist,self.etalist)
            self.η = self.fη(self.fck)
        self.Asuse1 = self.rebar(self.AsDia1)
        self.Asuse2 = self.rebar(self.AsDia2)
        self.Asuse3 = self.rebar(self.AsDia3)
        self.Dc = (self.Asuse1*self.AsNum1*self.Dc1 + self.Asuse2*self.AsNum2*self.Dc2 + self.Asuse3*self.AsNum3*self.Dc3)/(self.Asuse1*self.AsNum1 + self.Asuse2*self.AsNum2 + self.Asuse3*self.AsNum3)

    def rebar(self, AsDia):                              #철근직경 함수선언
        ubarea = [71.30, 126.70, 198.60, 286.50, 387.10, 506.70, 642.40, 794.20, 956.6]
        if AsDia == 10:                                  #사용철근 1개당 단면적
            As = ubarea[0]
        elif AsDia == 13:
            As = ubarea[1]
        elif AsDia == 16:
            As = ubarea[2]
        elif AsDia == 19:
            As = ubarea[3]
        elif AsDia == 22:
            As = ubarea[4]
        elif AsDia == 25:
            As = ubarea[5]
        elif AsDia == 29:
            As = ubarea[6]
        elif AsDia == 32:
            As = ubarea[7]
        elif AsDia == 35:
            As = ubarea[8]
        else:
            As = 0
        return(As)    
    
    
#------------------------------
#          휨모멘트 검토
#------------------------------

    def calmoment(self) :
        self.pmin = max(0.25*math.sqrt(self.fck)/self.fy,1.4/self.fy) #최소철근비

        self.D = self.H-self.Dc                                      #단면 유효높이
        self.Asuse = self.Asuse1*self.AsNum1 + self.Asuse2*self.AsNum2 + self.Asuse3*self.AsNum3                       #전체 사용철근량
        self.ρ = self.Asuse/(self.B*self.D)                                   #사용철근비
        self.β1 = self.β * 2                                           #등가사각형 응력블록의 깊이계수
        self.fyd = self.fy * self.Øs                                   #철근 설계인장강도
        self.εyd = self.fyd / self.Es
        self.ta = (self.fyd**2)/(2*self.η*self.fcd*self.B)
        self.tb = -self.fyd * self.D
        self.Asreq = (-self.tb - (self.tb**2 - 4*self.ta*self.Mun)**(1/2)) / (2 * self.ta)  #필요철근량 산정
        
        self.Asmin1 = 0.25 * math.sqrt(self.fck) * self.B * self.D / self.fy
        self.Asmin2 = 1.4 * self.B * self.D / self.fy
        self.Asmin3 = 4 * self.Asreq / 3
        self.Asmin = min(max(self.Asmin1,self.Asmin2), self.Asmin3)
        self.Asmax = 0.04 * self.B * self.D

        self.c_max = (self.δ*self.εcu / 0.0033 - 0.6) * self.D   

        self.cc = (self.Asuse*self.Øs*self.fy)/(self.α*self.Øc*0.85*self.fck*self.B)
        
        self.εyd = self.Øs*self.fy / self.Es
        self.εs  = (self.D - self.cc) / self.cc * self.εcu
        
        self.Mr = self.Asuse*self.Øs*self.fy*( self.D - self.β*self.cc )
        
        self.Msf = (self.Mr/self.Mun)


#------------------------------
#          전단력 검토
#------------------------------

    def calshear(self) :
        self.k = 1+math.sqrt(200/self.D)     #단면크기효과 고려한 계수
        if self.k > 2 :
            self.k1 = 2
        else :
            self.k1 = self.k
        self.fctk = 0.7*0.3*self.fcm**(2/3)     #콘크리트 인장강도
        self.fnn = self.Nu*1000/(self.H*self.B)  #전단철근이 없는경우 축인장응력
        self.fnmax = 0.2*self.Øc*self.fck       #이값이상 사용금지인지 단면을 증가시켜야 되는지 알수 없음
        self.fn = min(self.fnn, self.fnmax)
        self.ρs = min(self.ρ, 0.02)
        self.Vc  = (0.85*self.Øc*self.k*(self.ρs*self.fck)**(1/3) + 0.15*self.fn)*(self.B*self.D)  #전단철근이 없는 부재의 설계전단강도
        self.Vcdmin = (0.4*self.Øc*self.fctk + 0.15*self.fn)*(self.B*self.D)   #최소설계 전단강도
        self.Vcd = max(self.Vc,self.Vcdmin)
                    
        self.Avs = self.rebar(self.AvDia)*self.AvLeg #전단철근량  
        self.α = 90.0
        self.ν = 0.6*(1 - self.fck/250)
        self.z = 0.9*self.D
        if self.fnn < 0 :
            self.αcw = 0
        elif self.fnn == 0:
            self.αcw = 1.0
        elif self.fnn <= 0.25*self.Øc*self.fck:
            self.αcw = 1.0+self.fnn/(self.Øc*self.fck)
        elif self.fnn <= 0.5*self.Øc*self.fck:
            self.αcw = 1.25
        elif self.fnn <= 1.0*self.Øc*self.fck:
            self.αcw = 2.5*(1-self.fnn/(self.Øc*self.fck))    
        else:
            self.αcw = 0
    
        self.cotθ1 = 2.5              #cotθ = 2.5(θ=21.8도) 적용시
        self.tanθ1 = 1/self.cotθ1
        self.cotθ2 = 1                #cotθ = 1.0(θ=45.0도) 적용시
        self.tanθ2 = 1/self.cotθ2
        self.Vdmax1 = (self.ν*self.Øc*self.fck*self.B*self.z) / (self.cotθ1+self.tanθ1)
        self.Vdmax2 = (self.ν*self.Øc*self.fck*self.B*self.z) / (self.cotθ2+self.tanθ2)
        if self.sg == 1 :             #input에 1번 직접입력시 입력값 적용
            self.cotθ = self.seta
        elif self.sg == 2 :           #input에 2번 중간값입력시 중간값 적용  
            self.cotθ = (1+2.5)/2
        else :                        #input에 3번 자동산출입력시 자동계산 적용 (Eurocode 적용)
            if self.Vun <= self.Vdmax1 :   #Vu가 Vmax1 보다 작은경우 cotθ = 2.5(θ=21.8도) 적용 
                self.cotθ = 2.5
            elif self.Vun > self.Vdmax2 :  #Vu가 Vmax2 보다 큰경우 cotθ = 0 적용으로 단면 증가 필요
                self.cotθ = 0
            else :
                self.cotθ = 1/math.tan(0.5*math.asin(self.Vun /(0.2*self.fck*(1-self.fck/250)*self.B*self.z)))  #Vu가 Vmax2 보다 큰경우 산정불가식
        self.tanθ = 1/self.cotθ
        self.θ = math.degrees(math.atan(self.tanθ))
                
        self.Vd = (self.Øs*self.fy*self.Avs*0.9*self.D / self.AvSpace)*self.cotθ 
        self.Vdmax = (self.ν*self.Øc*self.fck*self.B*self.z) / (self.cotθ+self.tanθ)

        self.ρvuse = self.Avs / (self.AvSpace*self.B*math.sin(self.α))
        self.ρvmin = 0.08*math.sqrt(self.fck) / self.fy
        self.s1max = 0.75*self.D*(1+(1/math.tan(self.α*math.pi/180)))   #종방향 전단철근 간격규정
        self.s2max = min(0.75*self.D, 600)                              #횡방향 철근 최대폭 
        self.s2 = self.B-2*self.Dc                                      #횡방향 철근 간격
    

#--------------------------------------
#          사용성 검토(균열검토)
#--------------------------------------
    def calservice(self):
        self.nr  = round( self.Es / (0.077*(2300)**(1.5)*(self.fck + self.Δf)**(1/3)))     #철근비 산정(반올림)
        self.Xo = (self.B*self.H**2/2 + (self.nr-1)*self.Asuse*self.D) / (self.B*self.H + (self.nr-1)*self.Asuse) 
        self.Io = self.B*self.H**3/12 + self.B*self.H*(self.H/2-self.Xo)**2 + (self.nr-1)*self.Asuse*(self.D-self.Xo)**2
        self.fct = self.Ms*10**6 / self.Io*(self.H-self.Xo)

        self.fs = self.nr*self.Ms*10**6 / self.Io*(self.D-self.Xo) #사용철근의 응력

        if self.fct <= self.fctk :
            self.cr1 = "≤"
        else:
            self.cr1 = ">"

        if self.fs < 0.8*self.fy:
            self.cr3 = "≤"
        else:
            self.cr3 = ">"    
        if self.fs < 0.8*self.fy:
            self.cr4 = "... ∴O.K"
        else:
            self.cr4 = "... ∴N.G"

        if self.fct <= self.fctk :
            self.cr2 = "∴ 비균열 단면 ⇒ 균열검토 생략"
        else:
            self.cr2 = "∴ 균열 단면 검토"
            self.k = -self.nr*self.ρ+ math.sqrt((self.nr*self.ρ)**2+ 2*self.nr*self.ρ)       #중립축비
            self.x = self.k*self.D
            self.fc = 2*self.Ms*10**6 / (self.B*self.x*(self.D - self.x/3))
            self.fs = self.Ms*10**6 / (self.Asuse*(self.D - self.x/3))
    
            self.fsa = max(160,360)

            if self.fsa >= self.fs:
                self.cr5 = "≥"
            else:
                self.cr5 = "<"    
            if self.fsa >= self.fs:
                self.cr6 = "... ∴O.K"
            else:
                self.cr6 = "... ∴N.G"
            self.Act = self.B*(self.H-self.Xo)
            if self.Nu >= 0:       #압축(+)
                self.k1 = 1.5
            elif self.Nu < 0:      #인장(-)
                if self.H < 1000:
                    self.h1 = self.H
                elif self.H >= 1000:
                    self.h1 = 1000
                self.k1 = 2*self.h1/(3*self.H)

            if self.H <= 300:    #부등분포 반영 계수
                self.k = 1.0
            elif self.H <= 300 and self.H < 800:
                self.k = -0.0007*self.H+1.21
            elif self.H >= 800:
                self.k = 0.65
            self.fct = self.fctk / 0.7 #fct = fctm

            if self.H < 1000:
                self.h1 = self.H
            elif self.H >= 1000:
                self.h1 = 1000
        
            self.kc = 0.4*(1 - self.fn/(self.k1*(self.H/self.h1)*self.fct))

            self.Asdmin = self.kc*self.k*self.Act*self.fct / self.fsa   #최소철근량 산정
            if self.Asdmin <= self.Asuse:
                self.cr7 = "≤"
            else:
                self.cr7 = ">"    
            if self.Asdmin <= self.Asuse:
                self.cr8 = "... ∴O.K"
            else:
                self.cr8 = "... ∴N.G"
        
        print('새로 생성된 "section_check.txt"를 확인하세요!!')