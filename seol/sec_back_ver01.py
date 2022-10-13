import math
#--------------------------------------------------
#    직사각형 단철근보 단면검토 (도로교설계기준 2012)
#--------------------------------------------------
class Sec_back:

    def __init__(self, line):
        sentence=[]                        #리스트를 초기화 하여 sentence에 지정
        for iresult in line[2:]:           #모든줄의 리스트 요소[0번째,1번째,2번째....]중 1번째부터 세어서 개체수 만큼 반복 (즉 0이면 공백줄이 없고, 1이면 첫번째줄까지 공백을 2이면 두번째줄까지 공백 의미)
            isplt = iresult.split()            #isplt의 요소를 순차적으로 문자열에서 공백을 기준으로 리스트를 분할
            sentence.append(isplt)           #리스트 속의 리스트 작성[[],[],[]...](append함수 이용)
        senlist = sentence                   #senlist에 하나의 리스트로 변수지정
        self.fck = int((senlist[0][1]))           #fck설정
        self.fy = int((senlist[1][1]))            #fy설정
        self.Øc = float(senlist[2][1])            #Øc설정
        self.Øs = float(senlist[3][1])            #Øs설정
        self.Mu = float(senlist[4][1])            #Mu설정
        self.Vu = float(senlist[5][1])            #Vu설정  
        self.Nu = float(senlist[6][1])            #Nu설정
        self.Ms = float(senlist[7][1])            #Ms설정
        self.H = float(senlist[8][1])             #단면두께 설정
        self.B = float(senlist[9][1])             #단면 폭 설정
        self.Dc = float(senlist[10][1])           #피복두께 설정
        self.AsDia = int(senlist[11][1])          #철근직경 설정
        self.AsNum = int(senlist[12][1])          #철근개수 설정
        self.δ = float(senlist[13][1])            #재분배 모멘트율 설정
        self.AvDia = int(senlist[14][1])          #전단철근 직경
        self.AvLeg = float(senlist[15][1])        #전단철근 다리개수
        self.AvSpace = int(senlist[16][1])        #전단철근 배치간격
        self.Es = 200000 #철근의 탄성계수
        self.nε = 2.0        #곡선계수
        self.εco = 0.002
        self.εcu = 0.0033
        self.α = 0.789
        self.β = 0.412
        
    def rebar(self, AsDia):                                  #철근직경 함수선언
        if AsDia == 10:                                  #사용철근 1개당 단면적
            As = 71.33
        elif AsDia == 13:
            As = 126.7
        elif AsDia == 16:
            As = 198.6
        elif AsDia == 19:
            As = 286.5
        elif AsDia == 22:
            As = 387.1
        elif AsDia == 25:
            As = 506.7
        elif AsDia == 29:
            As = 642.4
        elif AsDia == 32:
            As = 794.2
        elif AsDia == 35:
            As = 956.6
        else:
            print("단면두께를 조정하십시요!!")
        return(As)    

#------------------------------
#          휨모멘트 검토
#------------------------------

    def calmoment(self) :
        self.pmin = max(0.25*math.sqrt(self.fck)/self.fy,1.4/self.fy) #최소철근비
        print(self.pmin)
        self.D = self.H-self.Dc                             #단면 유효높이
        
        self.Asuse = self.rebar(self.AsDia)*self.AsNum                        #사용철근량
        self.p = self.Asuse/(self.B*self.D)                                   #사용철근비

        cs=0
        while cs < 1000:    #중립축 깊이 1000mm이하로 가정
            self.As1 = self.Mu*10**6/(self.Øs*self.fy*(self.D-self.β*cs))
            self.c = round((self.As1*self.Øs*self.fy)/(self.α*self.Øc*0.85*self.fck*self.B),3)
            if self.c == cs:
                self.cd = self.c
            cs = round((cs + 0.001),3)
        self.As1 = self.Mu*10**6/(self.Øs*self.fy*(self.D-self.β*self.cd))
        self.c = round((self.As1*self.Øs*self.fy)/(self.α*self.Øc*0.85*self.fck*self.B),3)

        self.ρreq = ((self.Mu*10**6)/(self.Øs*self.fy*(self.D-self.β*self.c)))/(self.B*self.D) #소요철근량 산정
        self.ρ = self.Asuse/(self.B*self.D) #사용철근량 철근비

        self.Asreq = self.ρreq*(self.B*self.D)
        if self.Asreq < self.Asuse:
            self.ch = "< 사용철근량...O.K"
        else:
            self.ch = "> 사용철근량...N.G"    

        if  self.pmin <= self.ρ:
            self.ch1 ="ρmin ≤ ρ    .......    ∴ O.K"
        else:
            self.ch1 ="ρmin > ρ    .......    ∴ N.G"

        self.c_max = (self.δ*self.εcu / 0.0033 - 0.6) * self.D   

        self.cc = (self.Asuse*self.Øs*self.fy)/(self.α*self.Øc*0.85*self.fck*self.B)
        if self.cc <= self.c_max:
            self.ch2 = "≤ c_max... ∴ O.K"
        else:
            self.ch2 = "> c_max... ∴ N.G"

        self.εyd = self.Øs*self.fy / self.Es
        self.εs  = (self.D - self.cc) / self.cc *self.εcu
        if self.εs >= self.εyd:
            self.ch3 = "≥ εyd ... ∴ 철근항복"
        else:
            self.ch3 = "< εyd ... ∴ 철근 미항복"

        self.Mr = self.Asuse*self.Øs*self.fy*( self.D - self.β*self.cc )
        if self.Mr/(10**6) > self.Mu:
            self.ch4 = ">"
        else:
            self.ch4 = "<"

        if self.Mr/(10**6) > self.Mu:
            self.ch5 = "... ∴ O.K"
        else:
            self.ch5 = "... ∴ N.G"   
        self.sf = (self.Mr/(10**6)/self.Mu)    


#------------------------------
#          전단력 검토
#------------------------------

    def calshear(self) :
        self.κ = 1+math.sqrt(200/self.D)     #단면크기효과 고려한 계수
        if self.κ <= 2:
            self.sh1 = " ≤  2.0"
        else:
            self.sh1 = " 단면두께를 조정하십시요..."    
        if self.fck < 40:
            self.Δf = 4
        else:
            self.Δf = 6
        self.fctk = 0.7*0.3*(self.fck+self.Δf)**(2/3)     #콘크리트 인장강도
        self.fn = self.Nu/(self.H*self.B)
        self.Vc  = (0.85*self.Øc*self.κ*(self.ρ*self.fck)**(1/3) + 0.15*self.fn)*(self.B*self.D) / 1000  #전단철근이 없는 부재의 설계전단강도

        self.Vcdmin = (0.4*self.Øc*self.fctk + 0.15*self.fn)*(self.B*self.D) / 1000  #최소설계 전단강도

        self.Vcd = max(self.Vc,self.Vcdmin)

        if self.Vcd < self.Vu:
            self.sh2 = "< Vu"
        else:
            self.sh2 = "> Vu"
    
        self.Avs = self.rebar(self.AvDia)*self.AvLeg #전단철근량  

        if self.Vcd >= self.Vu:
            self.sh3 = "... ∴전단철근 불필요."    
        elif self.Vcd < self.Vu:
            self.sh3 = "... ∴전단철근 필요."
            self.z = 0.9*self.D
            self.fn = self.Nu/(self.B*self.H)  #축응력
            if self.fn == 0:
                self.αcw = 1.0
            elif self.fn > 0 and self.fn <= 0.25*self.Øc*self.fck:
                self.αcw = 1.0+self.fn/(self.Øc*self.fck)
            elif self.fn >= 0.25*self.Øc*self.fck and self.fn <= 0.5*self.Øc*self.fck:
                self.αcw = 1.25
            elif self.fn >= 0.5*self.Øc*self.fck and self.fn <= 1.0*self.Øc*self.fck:
                self.αcw = 2.5*(1-self.fn/(Øc*self.fck))    
            else:
                print("단면두께를 조정하십시요!!")            
    
#cotθ = math.sqrt((Øc*αcw*(1-fck/250)*fck*B*AvSpace)/(Øs*fy*Avs)-1)  # 1/tanθ
#θ=math.degrees(math.atan(tanθ))
            self.cotθ = 1.732051    #도로교설계기준에 1 ≤ cotθ ≤ 2.5 중 중간값 사용 각도로30도
            self.tanθ = 1/self.cotθ
            self.θ = math.degrees(math.atan(self.tanθ))
            self.α = 90.0
            self.ν = 0.6*(1 - self.fck/250)
            self.Vd = (self.Øs*self.fy*self.Avs*0.9*self.D / self.AvSpace)*self.cotθ/1000 
            self.Vdmax = (self.ν*self.Øc*self.fck*self.B*self.z) / (self.cotθ+self.tanθ) / 1000

            if self.Vdmax >=  self.Vd :
                self.sh4 = "≥"
            else:
                self.sh4 = "<" 

            if self.Vdmax >=  self.Vd :
                self.sh5 = "...∴ O.K"
            else:
                self.sh5 = "...∴ N.G"   
        
            self.ρvuse = self.Avs / (self.AvSpace*self.B*math.sin(self.α))
            self.ρvmin = 0.08*math.sqrt(self.fck) / self.fy
            self.s1max = 0.75*self.D*(1+(1/math.tan(self.α*math.pi/180)))   #종방향 전단철근 간격규정
            self.s2max = min(0.75*self.D, 600)   #횡방향 철근 최대폭 
            self.s2 = self.B-2*self.Dc   #횡방향 철근 간격
    
            if self.ρvmin <= self.ρvuse:
                self.sh6 = "≤  ρv.use ... ∴O.K"
            else:
                self.sh6 = ">  ρv.use ... ∴N.G"
    
            if self.AvSpace <= self.s1max:
                self.sh7 = "≥"
            else:
                self.sh7 = "<"
            if self.AvSpace <= self.s1max:
                self.sh8 = "... ∴O.K"
            else:
                self.sh8 = "... ∴N.G" 
            if self.s2 <= self.s2max:
                self.sh9 = "≥"
            else:
                self.sh9 = "<"    
            if self.s2 <= self.s2max:
                self.sh10 = "... ∴O.K"
            else:
                self.sh10 = "... ∴N.G"     

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
            self.k = -self.nr*self.p+ math.sqrt((self.nr*self.p)**2+ 2*self.nr*self.p)       #중립축비
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

            self.Asmin = self.kc*self.k*self.Act*self.fct / self.fsa   #최소철근량 산정
            if self.Asmin <= self.Asuse:
                self.cr7 = "≤"
            else:
                self.cr7 = ">"    
            if self.Asmin <= self.Asuse:
                self.cr8 = "... ∴O.K"
            else:
                self.cr8 = "... ∴N.G"
        
        print('새로 생성된 "section_check.txt"를 확인하세요!!')