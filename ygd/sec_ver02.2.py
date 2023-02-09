#------------------------------
#    직사각형 단철근보 단면검토
#------------------------------

#f=open("d:/python/sec_input.txt", 'r') #d드라이브 python폴더의 sec_input.txt을 읽어드림
f=open("sec_input.txt", 'r') #d드라이브 python폴더의 sec_input.txt을 읽어드림
line=f.readlines()
f.close()

sentence=[]                        #리스트를 초기화 하여 sentence에 지정
for iresult in line[2:]:           #모든줄의 리스트 요소[0번째,1번째,2번째....]중 1번째부터 세어서 개체수 만큼 반복 (즉 0이면 공백줄이 없고, 1이면 첫번째줄까지 공백을 2이면 두번째줄까지 공백 의미)
  #isplt=iresult.split()            #isplt의 요소를 순차적으로 문자열에서 공백을 기준으로 리스트를 분할
  isplt=iresult.split()[1]
  sentence.append(isplt)           #리스트 속의 리스트 작성[[],[],[]...](append함수 이용)
senlist=sentence                   #senlist에 하나의 리스트로 변수지정
fck=int(senlist[0])           #fck설정
fy=int(senlist[1])            #fy설정
Øc=float(senlist[2])            #Øc설정
Øs=float(senlist[3])            #Øs설정
Mu=float(senlist[4])            #Mu설정
Vu=float(senlist[5])            #Vu설정  
Nu=float(senlist[6])            #Nu설정
Ms=float(senlist[7])            #Ms설정
H=float(senlist[8])             #단면두께 설정
B=float(senlist[9])             #단면 폭 설정
Dc=float(senlist[10])           #피복두께 설정
AsDia=int(senlist[11])          #철근직경 설정
AsNum=int(senlist[12])          #철근개수 설정
δ=float(senlist[13])            #재분배 모멘트율 설정
AvDia=int(senlist[14])          #전단철근 직경
AvLeg=float(senlist[15])        #전단철근 다리개수
AvSpace=int(senlist[16])        #전단철근 배치간격



#fck=float(input("콘크리트 재료강도(fck≤40MPa)):"))    #재료강도 입력
#fy=float(input("철근의 항복강도(fy):"))               #철근항보강도 입력
#Øc=float(input("콘크리트의 재료저항계수(Øc=0.65):"))   #콘크리트 저항계수 입력
#Øs=float(input("철근의 재료저항계수(Øs=0.90):"))
#f=open("d:/python/section_check.txt", 'w')           #d드라이브 python폴더의 section_check.txt를 출력함


nε=2.0        #곡선계수
εco=0.002
εcu=0.0033
α=0.789
β=0.412

import math
pmin=max(0.25*math.sqrt(fck)/fy,1.4/fy) #최소철근비


#Mu=float(input("계수 모멘트 Mu(kN.m)="))
#Vu=float(input("계수 전단력 Vu(kN)="))
#H=float(input("단면의 두께 H(mm)="))
#B=float(input("단면의 폭 B(mm)="))
#Dc=float(input("피복두께 Dc(mm)="))
D=H-Dc                             #단면 유효높이


#------------------------------
#          휨모멘트 검토
#------------------------------


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


cs=0
while cs < 1000:    #중립축 깊이 1000mm이하로 가정
    As1=Mu*10**6/(Øs*fy*(D-β*cs))
    c=round((As1*Øs*fy)/(α*Øc*0.85*fck*B),3)
    #print(cs,c)
    if c==cs:
        cd=c
    cs =round((cs + 0.001),3)

As1=Mu*10**6/(Øs*fy*(D-β*cd))
c=round((As1*Øs*fy)/(α*Øc*0.85*fck*B),3)



ρreq=((Mu*10**6)/(Øs*fy*(D-β*c)))/(B*D) #소요철근량 산정
ρ=Asuse/(B*D) #사용철근량 철근비


Asreq=ρreq*(B*D)
if Asreq < Asuse:
    ch= "< 사용철근량...O.K"
else:
    ch= "> 사용철근량...N.G"    

if  pmin <= ρ:
    ch1="ρmin ≤ ρ    .......    ∴ O.K"
else:
    ch1="ρmin > ρ    .......    ∴ N.G"
    

#δ=float(input("재분배 후 모멘트율을 입력하십시요. (δ=1.0):"))
c_max = (δ*εcu / 0.0033 - 0.6) * D   



cc=(Asuse*Øs*fy)/(α*Øc*0.85*fck*B)
if cc <= c_max:
    ch2="≤ c_max... ∴ O.K"
else:
    ch2="> c_max... ∴ N.G"
    


Es=200000 #철근의 탄성계수
εyd = Øs*fy / Es
εs  = (D - cc) / cc *εcu
if εs >= εyd:
    ch3="≥ εyd ... ∴ 철근항복"
else:
    ch3="< εyd ... ∴ 철근 미항복"
    

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



κ=1+math.sqrt(200/D)     #단면크기효과 고려한 계수
if κ <= 2:
    sh1=" ≤  2.0"
else:
    sh1=" 단면두께를 조정하십시요..."  



if fck<40:
    Δf=4
else:
    Δf=6
fctk= 0.7*0.3*(fck+Δf)**(2/3)     #콘크리트 인장강도


fn=Nu/(H*B)
Vc  = (0.85*Øc*κ*(ρ*fck)**(1/3) + 0.15*fn)*(B*D) / 1000  #전단철근이 없는 부재의 설계전단강도

Vcdmin = (0.4*Øc*fctk + 0.15*fn)*(B*D) / 1000  #최소설계 전단강도

Vcd=max(Vc,Vcdmin)

if Vcd < Vu:
    sh2="< Vu"
else:
    sh2="> Vu"
    
Avs=rebar(AvDia)*AvLeg #전단철근량  
if Vcd < Vu:
    sh3="... ∴전단철근 필요."
    # f.write(f'      ∴ Vcd = Max(Vc, Vcd.min) = {Vcd:2.3f}kN {sh2:2s} = {Vu:2.3f}kN {sh3:2s}\n\n')   #메모장 출력 
    # f.write(f'      사용 전단철근량 Av.use = H{AvDia:2d} x {AvLeg:2.3f}ea = {Avs:2.3f}㎟  (간격 s = {AvSpace:2d}mm)\n')   #전단철근량 산정 출력
    # f.write(f'       z  = 0.9 D = {0.9*D:2.3f}mm\n')   #단면내부 팔길이 출력 
    shearchk=f'''      ∴ Vcd = Max(Vc, Vcd.min) = {Vcd:2.3f}kN {sh2:2s} = {Vu:2.3f}kN {sh3:2s}\n\n
      사용 전단철근량 Av.use = H{AvDia:2d} x {AvLeg:2.3f}ea = {Avs:2.3f}㎟  (간격 s = {AvSpace:2d}mm)\n
       z  = 0.9 D = {0.9*D:2.3f}mm\n'''   #단면내부 팔길이 출력 
    
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
    
    cotθ = math.sqrt((Øc*αcw*(1-fck/250)*fck*B*AvSpace)/(Øs*fy*Avs)-1)  # 1/tanθ
    tanθ =1/cotθ
    θ=math.degrees(math.atan(tanθ))
  
else:
    sh3="... ∴전단철근 불필요."    
    #f.write(f'      ∴ Vcd = Max(Vc, Vcd.min) = {Vcd:2.3f}kN {sh2:2s} = {Vu:2.3f}kN {sh3:2s}\n')   #메모장 출력 
    shearchk=f'      ∴ Vcd = Max(Vc, Vcd.min) = {Vcd:2.3f}kN {sh2:2s} = {Vu:2.3f}kN {sh3:2s}\n'   #메모장 출력 


f=open("section_check.txt", 'w')
outputstr=f"""
◈ 직사각형 보\n\n
   ▷ 검 토 조 건\n\n  
     재 료  강 도 : fck = {fck:2.1f} MPa,     fy = {fy:2.1f} MPa\n     재료저항계수 : Øc = {Øc:2.3f},       Øs = {Øs:2.3f}\n
     곡 선  계 수 : nε = {nε:2.3f},     εco = {εco:2.5f},     εcu = {εcu:2.5f}\n                    α = {α:2.3f},       β = {β:2.3f}\n

     최소 철근비 : pmin = max(0.25√(fck)/fy,1.4/fy) = {pmin:2.5f}\n\n

     계수 모멘트 Mu = {Mu:2.3f} kN.m       계수 전단력 Vu = {Vu:2.3f} kN\n     단면의 두께 H = {H:2.3f} mm         단  면  폭  B = {B:2.3f} mm\n     유 효 깊 이 D = {D:2.3f} mm          피 복 두 께 Dc = {Dc:2.3f} mm\n\n

   ▷ 휨모멘트 검토\n\n
     사용철근량 As.use = H{AsDia:2d} x {AsNum:2d}EA   (Dc = {Dc:2.3f} mm)\n                       = {Asuse:2.3f}㎟    ∴ P = As/(B.D) = {p:2.5f}\n\n   

    - 필요철근량 및 철근비 검토\n    
     소요중립축깊이 c = {cd:2.3f} mm로 가정\n
     As=Mu/(Øs*fy*(D-β*c)) = {As1:2.3f}㎟ \n
     c=(As*Øs*fy)/(α*Øc*0.85*fck*B) = {c:2.3f}mm ∴가정과 비슷함 O.K\n
     ρreq=Mu/(Øs*fy*(D-β*c)) = {ρreq:2.5f} ⇒ 4/3 ρreq ={(4/3)*ρreq:2.5f}\n    
     ∴ 필요철근량 As.req = ρreq × (B·D) = {Asreq:2.3f}㎟ {ch:2s}\n

     철근비검토 : = {ch1:2s}\n\n

    - 허용최대중립축 및 인장철근 변형률 검토\n
     c_max = (δ·εcu / 0.0033 - 0.6) × D = {c_max:2.3f}mm\n        ...여기서 δ (재분배 후 모멘트율) = {δ:2.3}\n
     c  = (As.use·Øs·fy) / (α Øc 0.85 fck·B) = {cc:2.3f}mm  {ch2:2s}\n
     εyd = Øs·fy / Es = {εyd:2.5f} (철근 설계항복변형률)\n     εs  = (d - c) / c ×εcu = {εs:2.5f} {ch3:2s}\n\n

    - 휨강도 검토\n
     Mr = As·Øs·fy·( D - β·c ) = {Mr:2.3f}N.mm\n        = {Mr/(10**6):2.3f}kN.m {ch4:2s} Mu= {Mu:2.3f}kN.m   {ch5:2s}  (S.F ={sf:2.3f})\n\n


   ▷ 전단력 검토 검토\n\n
    - 전단강도 검토\n   
      κ  = 1 + √(200/D) = {κ:2.3f} {sh1:2s}\n

      fctk= 0.7×0.3×(fck+Δf)^⅔ = {fctk:2.3f}MPa\n
      Vc  = [0.85 Øc·κ·(p fck)^⅓ + 0.15 fn] B·D / 1000 = {Vc:2.3f}kN\n   
      Vcd.min = (0.4 Øc·fctk + 0.15 fn) B·D / 1000 = {Vcdmin:2.3f}kN\n"""   #메모장 출력 

outputstr=outputstr+shearchk

f.write(outputstr)

f.close()

print('새로 생성된 "section_check.txt"를 확인하세요!!')