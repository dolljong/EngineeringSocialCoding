
f=open("d:/python/section_check.txt", 'w')            #생성파일 저장 디렉토리

f.write('◈ 직사각형 보\n\n')                           #메모장 출력
f.write('   ▷ 검 토 조 건\n\n')                        #메모장 출력   

fck=float(input("콘크리트 재료강도(fck≤40MPa)):"))              #재료강도 입력
fy=float(input("철근의 항복강도(fy):"))                  #철근항보강도 입력
Øc=float(input("콘크리트의 재료저항계수(Øc=0.65):"))   #콘크리트 저항계수 입력
Øs=float(input("철근의 재료저항계수(Øs=0.90):"))
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

Mu=float(input("계수 모멘트 Mu(kN.m)="))
Vu=float(input("계수 전단력 Vu(kN)="))
H=float(input("단면의 두께 H(mm)="))
B=float(input("단면의 폭 B(mm)="))
Dc=float(input("피복두께 Dc(mm)="))
D=H-Dc                             #단면 유효높이
f.write(f'     계수 모멘트 Mu = {Mu:2.3f} kN.m      계수 전단력 Vu = {Vu} kN\n     단면의 두께 H = {H:2.3f} mm          단  면  폭  B = {B:2.3f} mm\n     유 효 깊 이 D = {D:2.3f} mm          피 복 두 께 Dc = {Dc:2.3f} mm\n\n')   #메모장 출력

f.write('   ▷ 휨모멘트 검토\n\n')

AsDia=int(input("사용철근직경을 입력하십시요:"))     #사용철근 직경
AsNum=int(input("사용철근 갯수를 입력하십시요:"))    #사용철근 개수

if AsDia==10:                                    #사용철근 1개당 단면적
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

Asuse=As*AsNum 
p=Asuse/(B*D)                                   #사용철근량
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
c=round((As*Øs*fy)/(α*Øc*0.85*fck*B),3)
f.write(f'     As1=Mu/(Øs*fy*(D-β*c)) = {As1:2.3f}㎟ \n')   #메모장 출력
f.write(f'     c=(As1*Øs*fy)/(α*Øc*0.85*fck*B) = {c:2.3f}mm ∴가정과 비슷함 O.K\n')   #메모장 출력

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
δ=float(input("재분배 후 모멘트율을 입력하십시요. (δ=1.0):"))
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
    ch3="≥... ∴ 철근항복"
else:
    ch3="<... ∴ 철근 미항복"
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
f.write(f'     Mr = As·Øs·fy·( D - β·c ) = {Mr:2.3f}N.mm\n       = {Mr/(10**6):2.3f}kN.m {ch4:2s} Mu= {Mu:2.3f}kN.m   {ch5:2s}  (S.F ={sf:2.3f})\n\n')   #메모장 출력