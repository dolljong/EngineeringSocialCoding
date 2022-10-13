#--------------------------------------------------
#    직사각형 단철근보 단면검토 (도로교설계기준 2012)
#--------------------------------------------------

f=open("d:/python/sec_input.txt", 'r') #d드라이브 python폴더의 sec_input.txt을 읽어드림
line=f.readlines()
f.close()

sentence=[]                        #리스트를 초기화 하여 sentence에 지정
for iresult in line[2:]:           #모든줄의 리스트 요소[0번째,1번째,2번째....]중 1번째부터 세어서 개체수 만큼 반복 (즉 0이면 공백줄이 없고, 1이면 첫번째줄까지 공백을 2이면 두번째줄까지 공백 의미)
  isplt=iresult.split()            #isplt의 요소를 순차적으로 문자열에서 공백을 기준으로 리스트를 분할
  sentence.append(isplt)           #리스트 속의 리스트 작성[[],[],[]...](append함수 이용)
senlist=sentence                   #senlist에 하나의 리스트로 변수지정
fck=int((senlist[0][1]))           #fck설정
fy=int((senlist[1][1]))            #fy설정
Øc=float(senlist[2][1])            #Øc설정
Øs=float(senlist[3][1])            #Øs설정
Mu=float(senlist[4][1])            #Mu설정
Vu=float(senlist[5][1])            #Vu설정  
Nu=float(senlist[6][1])            #Nu설정
Ms=float(senlist[7][1])            #Ms설정
H=float(senlist[8][1])             #단면두께 설정
B=float(senlist[9][1])             #단면 폭 설정
Dc=float(senlist[10][1])           #피복두께 설정
AsDia=int(senlist[11][1])          #철근직경 설정
AsNum=int(senlist[12][1])          #철근개수 설정
δ=float(senlist[13][1])            #재분배 모멘트율 설정
AvDia=int(senlist[14][1])          #전단철근 직경
AvLeg=float(senlist[15][1])        #전단철근 다리개수
AvSpace=int(senlist[16][1])        #전단철근 배치간격

f=open("d:/python/section_check.txt", 'w')           #d드라이브 python폴더의 section_check.txt를 출력함

f.write('◈ 직사각형 보\n\n')                          #메모장 출력
f.write('   ▷ 검 토 조 건\n\n')                       #메모장 출력   

#fck=float(input("콘크리트 재료강도(fck≤40MPa)):"))    #재료강도 입력
#fy=float(input("철근의 항복강도(fy):"))               #철근항보강도 입력
#Øc=float(input("콘크리트의 재료저항계수(Øc=0.65):"))   #콘크리트 저항계수 입력
#Øs=float(input("철근의 재료저항계수(Øs=0.90):"))
f.write(f'     재 료  강 도 : fck = {fck:2.1f} MPa,     fy = {fy:2.1f} MPa\n     재료저항계수 : Øc = {Øc:2.3f},       Øs = {Øs:2.3f}\n')  #메모장 출력

nε=2.0        #곡선계수
εco=0.002
εcu=0.0033
α=0.789
β=0.412
f.write(f'     곡 선  계 수 : nε = {nε:2.3f},     εco = {εco:2.5f},     εcu = {εcu:2.5f}\n                    α = {α:2.3f},       β = {β:2.3f}\n')  #메모장 출력

import math
pmin=max(0.25*math.sqrt(fck)/fy,1.4/fy) #최소철근비
f.write(f'     최소 철근비 : pmin = max(0.25√(fck)/fy,1.4/fy) = {pmin:2.5f}\n\n')  #메모장 출력

#Mu=float(input("계수 모멘트 Mu(kN.m)="))
#Vu=float(input("계수 전단력 Vu(kN)="))
#H=float(input("단면의 두께 H(mm)="))
#B=float(input("단면의 폭 B(mm)="))
#Dc=float(input("피복두께 Dc(mm)="))
D=H-Dc                             #단면 유효높이
f.write(f'     계수 모멘트 Mu = {Mu:2.3f} kN.m       계수 전단력 Vu = {Vu:2.3f} kN\n     단면의 두께 H = {H:2.3f} mm         단  면  폭  B = {B:2.3f} mm\n     유 효 깊 이 D = {D:2.3f} mm          피 복 두 께 Dc = {Dc:2.3f} mm\n\n')   #메모장 출력


#------------------------------
#          휨모멘트 검토
#------------------------------

f.write('   ▷ 휨모멘트 검토\n\n')

#AsDia=int(input("사용철근직경을 입력하십시요:"))     #사용철근 직경
#AsNum=int(input("사용철근 갯수를 입력하십시요:"))    #사용철근 개수

def rebar(AsDia):                                  #철근직경 함수선언
    if AsDia==10:                                  #사용철근 1개당 단면적
        As=71.33
    elif AsDia==13:
        As=126.7
    elif AsDia==16:
        As=198.6
    elif AsDia==19:
        As=286.5
    elif AsDia==22:
        As=387.1
    elif AsDia==25:
        As=506.7
    elif AsDia==29:
        As=642.4
    elif AsDia==32:
        As=794.2
    elif AsDia==35:
        As=956.6
    else:
        print("단면두께를 조정하십시요!!")
    return(As)    

Asuse=rebar(AsDia)*AsNum                        #사용철근량
p=Asuse/(B*D)                                   #사용철근비
f.write(f'     사용철근량 As.use = H{AsDia:2d} x {AsNum:2d}EA   (Dc = {Dc:2.3f} mm)\n                       = {Asuse:2.3f}㎟    ∴ P = As/(B.D) = {p:2.5f}\n\n')   #메모장 출력   

f.write('    - 필요철근량 및 철근비 검토\n')

cs=0
while cs < 1000:    #중립축 깊이 1000mm이하로 가정
    As1=Mu*10**6/(Øs*fy*(D-β*cs))
    c=round((As1*Øs*fy)/(α*Øc*0.85*fck*B),3)
    #print(cs,c)
    if c==cs:
        cd=c
    cs =round((cs + 0.001),3)
f.write(f'     소요중립축깊이 c = {cd:2.3f} mm로 가정\n')   #메모장 출력
As1=Mu*10**6/(Øs*fy*(D-β*cd))
c=round((As1*Øs*fy)/(α*Øc*0.85*fck*B),3)
f.write(f'     As=Mu/(Øs*fy*(D-β*c)) = {As1:2.3f}㎟ \n')   #메모장 출력
f.write(f'     c=(As*Øs*fy)/(α*Øc*0.85*fck*B) = {c:2.3f}mm ∴가정과 비슷함 O.K\n')   #메모장 출력

ρreq=((Mu*10**6)/(Øs*fy*(D-β*c)))/(B*D) #소요철근량 산정
ρ=Asuse/(B*D) #사용철근량 철근비
f.write(f'     ρreq=Mu/(Øs*fy*(D-β*c)) = {ρreq:2.5f} ⇒ 4/3 ρreq ={(4/3)*ρreq:2.5f}\n')   #메모장 출력

Asreq=ρreq*(B*D)
if Asreq < Asuse:
    ch= "< 사용철근량...O.K"
else:
    ch= "> 사용철근량...N.G"    
f.write(f'     ∴ 필요철근량 As.req = ρreq × (B·D) = {Asreq:2.3f}㎟ {ch:2s}\n')   #메모장 출력

if  pmin <= ρ:
    ch1="ρmin ≤ ρ    .......    ∴ O.K"
else:
    ch1="ρmin > ρ    .......    ∴ N.G"
f.write(f'     철근비검토 : = {ch1:2s}\n\n')   #메모장 출력 

f.write('    - 허용최대중립축 및 인장철근 변형률 검토\n')
#δ=float(input("재분배 후 모멘트율을 입력하십시요. (δ=1.0):"))
c_max = (δ*εcu / 0.0033 - 0.6) * D   
f.write(f'     c_max = (δ·εcu / 0.0033 - 0.6) × D = {c_max:2.3f}mm\n        ...여기서 δ (재분배 후 모멘트율) = {δ:2.3}\n')   #메모장 출력

cc=(Asuse*Øs*fy)/(α*Øc*0.85*fck*B)
if cc <= c_max:
    ch2="≤ c_max... ∴ O.K"
else:
    ch2="> c_max... ∴ N.G"
f.write(f'     c  = (As.use·Øs·fy) / (α Øc 0.85 fck·B) = {cc:2.3f}mm  {ch2:2s}\n')   #메모장 출력

Es=200000 #철근의 탄성계수
εyd = Øs*fy / Es
εs  = (D - cc) / cc *εcu
if εs >= εyd:
    ch3="≥ εyd ... ∴ 철근항복"
else:
    ch3="< εyd ... ∴ 철근 미항복"
f.write(f'     εyd = Øs·fy / Es = {εyd:2.5f} (철근 설계항복변형률)\n     εs  = (d - c) / c ×εcu = {εs:2.5f} {ch3:2s}\n\n')   #메모장 출력

f.write('    - 휨강도 검토\n')
Mr = Asuse*Øs*fy*( D - β*cc )
if Mr/(10**6) > Mu:
    ch4=">"
else:
    ch4="<"

if Mr/(10**6) > Mu:
    ch5="... ∴ O.K"
else:
    ch5="... ∴ N.G"   
sf=(Mr/(10**6)/Mu)    
f.write(f'     Mr = As·Øs·fy·( D - β·c ) = {Mr:2.3f}N.mm\n        = {Mr/(10**6):2.3f}kN.m {ch4:2s} Mu= {Mu:2.3f}kN.m   {ch5:2s}  (S.F ={sf:2.3f})\n\n')   #메모장 출력


#------------------------------
#          전단력 검토
#------------------------------

f.write('   ▷ 전단력 검토 검토\n\n')
f.write('    - 전단강도 검토\n')

κ=1+math.sqrt(200/D)     #단면크기효과 고려한 계수
if κ <= 2:
    sh1=" ≤  2.0"
else:
    sh1=" 단면두께를 조정하십시요..."    
f.write(f'      κ  = 1 + √(200/D) = {κ:2.3f} {sh1:2s}\n')   #메모장 출력


if fck<40:
    Δf=4
else:
    Δf=6
fctk= 0.7*0.3*(fck+Δf)**(2/3)     #콘크리트 인장강도
f.write(f'      fctk= 0.7×0.3×(fck+Δf)^⅔ = {fctk:2.3f}MPa\n')   #메모장 출력

fn=Nu/(H*B)
Vc  = (0.85*Øc*κ*(ρ*fck)**(1/3) + 0.15*fn)*(B*D) / 1000  #전단철근이 없는 부재의 설계전단강도
f.write(f'      Vc  = [0.85 Øc·κ·(p fck)^⅓ + 0.15 fn] B·D / 1000 = {Vc:2.3f}kN\n')   #메모장 출력  

Vcdmin = (0.4*Øc*fctk + 0.15*fn)*(B*D) / 1000  #최소설계 전단강도
f.write(f'      Vcd.min = (0.4 Øc·fctk + 0.15 fn) B·D / 1000 = {Vcdmin:2.3f}kN\n')   #메모장 출력 
Vcd=max(Vc,Vcdmin)

if Vcd < Vu:
    sh2="< Vu"
else:
    sh2="> Vu"
    
Avs=rebar(AvDia)*AvLeg #전단철근량  


if Vcd >= Vu:
    sh3="... ∴전단철근 불필요."    
    f.write(f'      ∴ Vcd = Max(Vc, Vcd.min) = {Vcd:2.3f}kN {sh2:2s} = {Vu:2.3f}kN {sh3:2s}\n\n')   #메모장 출력
    #print('새로 생성된 "section_check.txt"를 확인하세요!!')
          
elif Vcd < Vu:
    sh3="... ∴전단철근 필요."
    z=0.9*D
    f.write(f'      ∴ Vcd = Max(Vc, Vcd.min) = {Vcd:2.3f}kN {sh2:2s} = {Vu:2.3f}kN {sh3:2s}\n\n')   #메모장 출력 
    f.write(f'      사용 전단철근량 Av.use = H{AvDia:2d} x {AvLeg:2.3f}ea = {Avs:2.3f}㎟  (간격 s = {AvSpace:2d}mm)\n')   #전단철근량 산정 출력
    f.write(f'       z  = 0.9 D = {z:2.3f}mm\n')   #단면내부 팔길이 출력 
    
    fn=Nu/(B*H)  #축응력
    if fn==0:
        αcw=1.0
    elif fn >0 and fn <= 0.25*Øc*fck:
        αcw=1.0+fn/(Øc*fck)
    elif fn >= 0.25*Øc*fck and fn <= 0.5*Øc*fck:
        αcw=1.25
    elif fn >= 0.5*Øc*fck and fn <= 1.0*Øc*fck:
        αcw=2.5*(1-fn/(Øc*fck))    
    else:
        print("단면두께를 조정하십시요!!")            
    
    #cotθ = math.sqrt((Øc*αcw*(1-fck/250)*fck*B*AvSpace)/(Øs*fy*Avs)-1)  # 1/tanθ
    #θ=math.degrees(math.atan(tanθ))
    cotθ = 1.732051    #도로교설계기준에 1 ≤ cotθ ≤ 2.5 중 중간값 사용 각도로30도
    tanθ =1/cotθ
    θ=math.degrees(math.atan(tanθ))
    α = 90.0
    ν = 0.6*(1 - fck/250)
    Vd = (Øs*fy*Avs*0.9*D / AvSpace)*cotθ/1000 
    Vdmax = (ν*Øc*fck*B*z) / (cotθ+tanθ) / 1000
     
    if Vdmax >=  Vd :
        sh4="≥"
    else:
        sh4="<" 

    if Vdmax >=  Vd :
        sh5="...∴ O.K"
    else:
        sh5="...∴ N.G"   
        
    f.write(f'      θ = {θ:2.3f}°  (콘크리트 스트럿과 주인장철근의 경사각)\n')   #메모장 출력  
    f.write(f'      α = {α:2.3f}°  (전단철근과 부재축의 경사각)\n')   #메모장 출력  
    f.write(f'      Vd = (Øs·fy·Av·z / s) ×cotθ/1000 = {Vd:2.3f}kN\n')   #메모장 출력 
    f.write(f'      Vd.max = (νØc fck B z) / (cotθ+tantθ) / 1000 = {Vdmax:2.3f}kN  {sh4:2s} Vd\n')   #메모장 출력
    f.write(f'      ∴ Vd = Min(Vd, Vd.max) = {min(Vd,Vdmax):2.3f}kN  {sh4:2s} Vu = {Vu:2.3f}kN {sh5:2s} (S.F = {Vd/Vu:2.3f})\n\n')   #메모장 출력

    f.write('    - 최소 전단철근비 및 전단철근간격 검토 \n')
    ρvuse = Avs / (AvSpace*B*math.sin(α))
    ρvmin = 0.08*math.sqrt(fck) / fy
    s1max =0.75*D*(1+(1/math.tan(α*math.pi/180)))   #종방향 전단철근 간격규정
    s2max = min(0.75*D, 600)   #횡방향 철근 최대폭 
    s2=B-2*Dc   #횡방향 철근 간격
    
    if ρvmin <= ρvuse:
        sh6="≤  ρv.use ... ∴O.K"
    else:
        sh6=">  ρv.use ... ∴N.G"
    
        f.write(f'      사용 전단철근비 ρv.use = Av / (s·B·sinα) = {ρvuse:2.5f}\n')   #메모장 출력
        f.write(f'      최소 전단철근비 ρv.min = 0.08 √(fck) / fy = {ρvmin:2.5f} {sh6:2s}\n')   #메모장 출력
        
    if AvSpace <= s1max:
        sh7="≥"
    else:
            sh7="<"
    if AvSpace <= s1max:
        sh8="... ∴O.K"
    else:
        sh8="... ∴N.G" 
    if s2 <= s2max:
        sh9="≥"
    else:
        sh9="<"    
    if s2 <= s2max:
        sh10="... ∴O.K"
    else:
        sh10="... ∴N.G"     

    f.write(f'      종방향 최대간격 s₁max = 0.75D (1+cotα) = {s1max:2.5f}mm {sh7:2s} s₁= {AvSpace:2.3f}mm {sh8:2s}\n')   #메모장 출력
    f.write(f'      횡방향 최대간격 s₂max = Min(0.75D, 600) = {s2max:2.5f}mm {sh9:2s} s₂= {s2:2.3f}mm {sh10:2s}\n\n')   #메모장 출력


#--------------------------------------
#          사용성 검토(균열검토)
#--------------------------------------

f.write('   ▷ 사용성 검토(균열검토)\n\n')
f.write(f'      Ms = {Ms:2.3f}kN.m  (사용하중조합-Ⅰ)\n')   #메모장 출력
f.write('    - 균열발생 여부 검토 (비균열 단면으로 가정)\n')

nr  =round( Es / (0.077*(2300)**(1.5)*(fck + Δf)**(1/3)))     #철근비 산정(반올림)
Xo = (B*H**2/2 + (nr-1)*Asuse*D) / (B*H + (nr-1)*Asuse) 
Io = B*H**3/12 + B*H*(H/2-Xo)**2 + (nr-1)*Asuse*(D-Xo)**2
fct = Ms*10**6 / Io*(H-Xo)

f.write(f'      n  = Es/Ec = 200,000 / (0.077 mc^1.5 * ³√(Fck + Δf)) = {nr:2d}\n')   #메모장 출력
f.write(f'      Xo = (B·H²/2 + (n-1)·As·D) / (B·H + (n-1)·As) = {Xo:2.3f}mm\n')   #메모장 출력
f.write(f'      Io = B·H³/12 + B·H·(H/2-Xo)²+ (n-1)·As·(D-Xo)²= {Io:2.3f}mm⁴\n')   #메모장 출력

fs = nr*Ms*10**6 / Io*(D-Xo) #사용철근의 응력

if fct <= fctk :
    cr1="≤"
else:
    cr1=">"
    
if fs < 0.8*fy:
    cr3="≤"
else:
    cr3=">"    
if fs < 0.8*fy:
    cr4="... ∴O.K"
else:
    cr4="... ∴N.G"

if fct <= fctk :
    cr2="∴ 비균열 단면 ⇒ 균열검토 생략"
    
    f.write(f'      fct = Ms / Io×(H-Xo) = {fct:2.3f}MPa {cr1:2s} fctk = {fctk:2.3f}MPa {cr2:2s} \n')   #메모장 출력
    f.write('    - 철근응력제한 검토\n')
    f.write(f'      fs = n·Ms / Io×(D-Xo) =  {fs:2.3f}MPa {cr3:2s} 0.8fy = {0.8*fy:2.3f}MPa {cr4:2s}\n\n')   #메모장
else:
    cr2="∴ 균열 단면 검토"
    k = -nr*p+ math.sqrt((nr*p)**2+ 2*nr*p)       #중립축비
    x = k*D
    fc = 2*Ms*10**6 / (B*x*(D - x/3))
    fs = Ms*10**6 / (Asuse*(D - x/3))
    
    f.write(f'      fct = Ms / Io×(H-Xo) = {fct:2.3f}MPa {cr1:2s} fctk = {fctk:2.3f}MPa {cr2:2s}\n\n')   #메모장 출력
    f.write('    - 철근응력제한 검토\n')
    f.write(f'      ρ = As/(B·D) =  {p:2.5f}\n')   #메모장
    f.write(f'      k  = -nρ+ √((nρ)²+ 2nρ) = {k:2.3f}  (j= 1-k/3= {1-k/3:2.3f})\n')   #메모장
    f.write(f'      x  = k·d =  {x:2.5f}mm\n')   #메모장
    f.write(f'      fc = 2·Ms / (B·x·(D - x/3)) =  {fc:2.5f}MPa\n')   #메모장
    f.write(f'      fs = Ms / (As ·(D - x/3))   =  {fs:2.5f}MPa {cr3:2s} 0.8fy = {0.8*fy:2.3f}MPa {cr4:2s}\n\n')  #메모장
    
    f.write('    - 간접균열제어 및 최소철근량\n')
    f.write(f'      철 근 직 경 : {AsDia:2d}mm,    철 근 간 격 : {(B-2*Dc)/AsNum:2.3f}mm\n')   #메모장

    fsa=max(160,360)

    if fsa >= fs:
        cr5="≥"
    else:
        cr5="<"    
    if fsa >= fs:
        cr6="... ∴O.K"
    else:
        cr6="... ∴N.G"
    f.write(f'      허 용 응 력 : fsa = Max(160,360) = {fsa:2d}MPa {cr5:2s} fs = {fs:2.3f}MPa {cr6:2s}\n')   #메모장

    Act = B*(H-Xo)
    if Nu>=0:       #압축(+)
        k1=1.5
    elif Nu<0:      #인장(-)
        if H<1000:
            h1=H
        elif H>=1000:
            h1=1000
        k1=2*h1/(3*H)

    if H<=300:    #부등분포 반영 계수
        k=1.0
    elif H<=300 and H<800:
        k=-0.0007*H+1.21
    elif H>=800:
        k=0.65
    fct=fctk/0.7 #fct = fctm

    if H<1000:
        h1=H
    elif H>=1000:
        h1=1000
        
    kc = 0.4*(1 - fn/(k1*(H/h1)*fct))

    Asmin = kc*k*Act*fct / fsa   #최소철근량 산정
    if Asmin <= Asuse:
        cr7="≤"
    else:
        cr7=">"    
    if Asmin <= Asuse:
        cr8="... ∴O.K"
    else:
        cr8="... ∴N.G"
    f.write(f'      최소 철근량 : As.min = kc·k·Act·fct / fsa = {Asmin:2.3f} ㎟ {cr7:2s} As={Asuse:2.3f}㎟ {cr8:2s}\n')   #메모장
    f.write(f'            여기서... Act = B·(H-Xo) = {Act:2.3f} ㎟\n')   #메모장
    f.write(f'                      kc  = 0.4×[1 - fn/(k₁(h/h*)×fct)] = {kc:2.3f}\n')   #메모장    
    f.write(f'                      k   =  {k:2.3f}\n')   #메모장 
    f.write(f'                      fct = fctm = {fct:2.3f}MPa\n')   #메모장  
    f.write(f'                      fsa = {fsa:2.3f}MPa\n')   #메모장    

    
print('새로 생성된 "section_check.txt"를 확인하세요!!')