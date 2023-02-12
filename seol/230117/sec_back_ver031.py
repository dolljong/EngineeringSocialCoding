import math
import numpy as np
from scipy import interpolate #직선보간법
import pandas as pd
#--------------------------------------------------
#    직사각형 단철근보 단면검토 (도로교설계기준 2012)
#--------------------------------------------------
class Sec_back:
    """
    단면검토 backend class     
    """
    def __init__(self, data_rc_mat, data_mat_fac_ulsals, data_sec, data_usedas_band, data_usedas_shear, data_secforce):
        """
        생성자
        :param data_rc_mat : [fck, fy]
        :param data_mat_fac_ulsals : [[Øc, Øs],[Øc, Øs]]
        :param data_sec : [H, B]
        :param data_usedas_band : 휨철근 정보 [dia,num,dc, dia,num,dc, dia,num,dc]
        :param data_usedas_shear : 전단철근 정보 [dia,num,s,sg,seta]
        :param data_secforce : 부재력 정보 [Mu, Vu, Nu, Ms-1, Ms-5, method] 
        """
        self.fck = data_rc_mat[0]           #fck설정
        self.fy = data_rc_mat[1]            #fy설정
        self.Øc = data_mat_fac_ulsals[0][0]            #Øc설정
        self.Øs = data_mat_fac_ulsals[0][1]            #Øs설정
        self.H = data_sec[0]             #단면두께 설정
        self.B = data_sec[1]             #단면 폭 설정
        self.AsDia1 = data_usedas_band[0]       #1단 철근직경 설정
        self.AsNum1 = data_usedas_band[1]       #1단 철근개수 설정
        self.Dc1 = data_usedas_band[2]          #1단 피복두께 설정
        self.AsDia2 = data_usedas_band[3]       #2단 철근직경 설정
        self.AsNum2 = data_usedas_band[4]       #2단 철근개수 설정
        self.Dc2 = data_usedas_band[5]          #2단 피복두께 설정
        self.AsDia3 = data_usedas_band[6]       #3단 철근직경 설정
        self.AsNum3 = data_usedas_band[7]       #3단 철근개수 설정
        self.Dc3 = data_usedas_band[8]          #3단 피복두께 설정
        self.AvDia = data_usedas_shear[0]        #전단철근 직경
        self.AvLeg = data_usedas_shear[1]        #전단철근 다리개수
        self.AvSpace = data_usedas_shear[2]      #전단철근 배치간격
        self.sg = data_usedas_shear[3]           #복부스트럿 각도 입력방법 선택
        self.seta = data_usedas_shear[4]         #복부스트럿 각도 직접입력값
        self.αv = data_usedas_shear[5]           #전단철근과 주철근 각도(주철근으로부터 시계방향각도)
        self.Mu = data_secforce[0]            #Mu설정
        self.Vu = data_secforce[1]            #Vu설정  
        self.Nu = data_secforce[2]            #Nu설정
        self.Ms1 = data_secforce[3]            #Ms-1설정
        self.Ms5 = data_secforce[4]            #Ms-5설정
        self.crid = data_secforce[5]           #사용성검토방법 설정
        self.ulsals = data_secforce[6]          #극한한계 or 극단상황한계
        self.δ = 1                                #재분배 모멘트율 설정
        self.Es = 200000                          #철근의 탄성계수
        self.Mun = self.Mu*1000000
        self.Vun = self.Vu*1000
        self.Nun = self.Nu*1000
        self.Msn1 = self.Ms1*1000000
        self.Msn5 = self.Ms5*1000000
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
        if self.AsNum1 == 0 :
            self.Asspace1 = 0
        else :
            self.Asspace1 = self.B / self.AsNum1
        if self.AsNum2 == 0 :
            self.Asspace2 = 0
        else :
            self.Asspace2 = self.B / self.AsNum2
        if self.AsNum3 == 0 :
            self.Asspace3 = 0
        else :
            self.Asspace3 = self.B / self.AsNum3

        self.Dc = (self.Asuse1*self.AsNum1*self.Dc1 + self.Asuse2*self.AsNum2*self.Dc2 + self.Asuse3*self.AsNum3*self.Dc3)/(self.Asuse1*self.AsNum1 + self.Asuse2*self.AsNum2 + self.Asuse3*self.AsNum3)
        self.D = self.H-self.Dc                                      #단면 유효높이
        self.β1 = self.β * 2                                           #등가사각형 응력블록의 깊이계수

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

        #self.D = self.H-self.Dc                                      #단면 유효높이
        self.Asuse = self.Asuse1*self.AsNum1 + self.Asuse2*self.AsNum2 + self.Asuse3*self.AsNum3                       #전체 사용철근량
        self.ρ = self.Asuse/(self.B*self.D)                                   #사용철근비
        #self.β1 = self.β * 2                                           #등가사각형 응력블록의 깊이계수
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
        self.fnn = self.Nun/(self.H*self.B)  #전단철근이 없는경우 축인장응력
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

        self.ρvuse = self.Avs / (self.AvSpace*self.B*math.sin(self.αv))
        self.ρvmin = 0.08*math.sqrt(self.fck) / self.fy
        self.s1max = 0.75*self.D*(1+(1/math.tan(self.αv*math.pi/180)))  #종방향 전단철근 간격규정
        self.s2max = min(0.75*self.D, 600)                              #횡방향 철근 최대폭 
        self.s2 = self.B / self.AvLeg                                   #횡방향 철근 간격(직접입력 또는 도면에서 추출이 정확함)
        self.dTr = (self.Mr - self.Mun) / self.D                        #모멘트 철근량 이상으로 받을수 있는 주철근의 추가 인장력 
        self.dT = 0.5 * self.Vun *(self.cotθ - 1/math.tan(self.αv*math.pi/180)) #Vu에 의해 종방향 철근에 발생하는 추가 인장력

#--------------------------------------
#          사용성 검토(균열검토)
#--------------------------------------
    def calservice(self):
        self.nr  = round( self.Es / self.Ec)                             #철근비 산정(반올림)
        self.Xo = (self.B*self.H**2/2 + (self.nr-1)*self.Asuse*self.D) / (self.B*self.H + (self.nr-1)*self.Asuse) 
        self.Io = self.B*self.H**3/12 + self.B*self.H*(self.H/2-self.Xo)**2 + (self.nr-1)*self.Asuse*(self.D-self.Xo)**2
        self.fct1 = self.Msn1 / self.Io*(self.H-self.Xo)
        self.fct5 = self.Msn5 / self.Io*(self.H-self.Xo)
        
        #self.fs = self.nr*self.Msn / self.Io*(self.D-self.Xo) #사용철근의 응력
        self.D1 = self.H-self.Dc1
        self.c = -self.nr*self.ρ+ math.sqrt((self.nr*self.ρ)**2+ 2*self.nr*self.ρ)       #중립축비
        self.x = self.k*self.D
        self.fc1 = 2*self.Msn1 / (self.B*self.x*(self.D - self.x/3))
        self.fc5 = 2*self.Msn5 / (self.B*self.x*(self.D - self.x/3))
        self.fs1 = self.Msn1 / (self.Asuse*(self.D1 - self.x/3))
        self.fs5 = self.Msn5 / (self.Asuse*(self.D1 - self.x/3))
        self.fca1 = 0.6*self.fck
        self.fca5 = 0.45*self.fck
        self.fsa1 = 0.8*self.fy

        self.fsa = max(160,360)
        self.Act = self.B*(self.H-self.Xo)
        if self.Nu >= 0:       #k1산청 축력압축(+)
            self.k1 = 1.5
        elif self.Nu < 0:      #k1산정 축력인장(-)
            if self.H < 1000:
                self.h1 = self.H
            else:
                self.h1 = 1000
            self.k1 = 2*self.h1/(3*self.H)

        if self.H <= 300:    #부등분포 반영 계수
            self.k = 1.0
        elif self.H < 800:
            self.k = -0.0007*self.H+1.21
        else :
            self.k = 0.65
        self.fct = self.fctk / 0.7 #fct = fctm

        if self.H <= 1000:   #단면높이의 한계 산정
            self.h1 = self.H
        else:
            self.h1 = 1000
        self.kc = min(0.4*(1 - self.fn/(self.k1*(self.H/self.h1)*self.fct)),1)
        self.Asdmin = self.kc*self.k*self.Act*self.fct / self.fsa   #최소철근량 산정
    # 간접균열검토    
        crdia = [32,25,16,14,10,8]
        crspace = [300,250,200,150,100,50]
        index=[160,200,240,280,320,360]
        if self.AsDia1 <= crdia[5]:
            self.fsad = index[5]
        elif self.AsDia1 <= crdia[4] :
            self.fsad = index[4]
        elif self.AsDia1 <= crdia[3] :
            self.fsad = index[3]
        elif self.AsDia1 <= crdia[2] :
            self.fsad = index[2]
        elif self.AsDia1 <= crdia[1] :
            self.fsad = index[1]
        else :
            self.fsad = index[0]
        if self.Asspace1 <= crspace[5]:
            self.fsas = index[5]
        elif self.Asspace1 <= crspace[4]:
            self.fsas = index[4]
        elif self.Asspace1 <= crspace[3]:
            self.fsas = index[3]
        elif self.Asspace1 <= crspace[2]:
            self.fsas = index[2]
        elif self.Asspace1 <= crspace[1]:
            self.fsas = index[1]
        else :
            self.fsas = index[0]
        self.fsaf = max(self.fsad, self.fsas)



            
        
        