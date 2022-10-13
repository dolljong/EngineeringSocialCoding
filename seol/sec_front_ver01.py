from sec_back_ver01 import *
#--------------------------------------------------
#    직사각형 단철근보 단면검토 (도로교설계기준 2012)
#--------------------------------------------------

f=open("d:/python/이기동상무/sec_input_ver03.txt", 'r') #d드라이브 python폴더의 sec_input.txt을 읽어드림
line=f.readlines()
f.close()

f=open("d:/python/section_check-cf.txt", 'w')           #d드라이브 python폴더의 section_check.txt를 출력함

f.write('◈ 직사각형 보\n\n')                          #메모장 출력
f.write('   ▷ 검 토 조 건\n\n')                       #메모장 출력   

calc = Sec_back(line)
calc.calmoment()
f.write(f'     재 료  강 도 : fck = {calc.fck:2.1f} MPa,     fy = {calc.fy:2.1f} MPa\n     재료저항계수 : Øc = {calc.Øc:2.3f},       Øs = {calc.Øs:2.3f}\n')  #메모장 출력
f.write(f'     곡 선  계 수 : nε = {calc.nε:2.3f},     εco = {calc.εco:2.5f},     εcu = {calc.εcu:2.5f}\n                    α = {calc.α:2.3f},       β = {calc.β:2.3f}\n')  #메모장 출력
f.write(f'     최소 철근비 : pmin = max(0.25√(fck)/fy,1.4/fy) = {calc.pmin:2.5f}\n\n')  #메모장 출력
f.write(f'     계수 모멘트 Mu = {calc.Mu:2.3f} kN.m       계수 전단력 Vu = {calc.Vu:2.3f} kN\n     단면의 두께 H = {calc.H:2.3f} mm         단  면  폭  B = {calc.B:2.3f} mm\n     유 효 깊 이 D = {calc.D:2.3f} mm          피 복 두 께 Dc = {calc.Dc:2.3f} mm\n\n')   #메모장 출력

#------------------------------
#          휨모멘트 검토
#------------------------------

f.write('   ▷ 휨모멘트 검토\n\n')
f.write(f'     사용철근량 As.use = H{calc.AsDia:2d} x {calc.AsNum:2d}EA   (Dc = {calc.Dc:2.3f} mm)\n                       = {calc.Asuse:2.3f}㎟    ∴ P = As/(B.D) = {calc.p:2.5f}\n\n')   #메모장 출력   
f.write('    - 필요철근량 및 철근비 검토\n')
f.write(f'     소요중립축깊이 c = {calc.cd:2.3f} mm로 가정\n')   #메모장 출력
f.write(f'     As=Mu/(Øs*fy*(D-β*c)) = {calc.As1:2.3f}㎟ \n')   #메모장 출력
f.write(f'     c=(As*Øs*fy)/(α*Øc*0.85*fck*B) = {calc.c:2.3f}mm ∴가정과 비슷함 O.K\n')   #메모장 출력
f.write(f'     ρreq=Mu/(Øs*fy*(D-β*c)) = {calc.ρreq:2.5f} ⇒ 4/3 ρreq ={(4/3)*calc.ρreq:2.5f}\n')   #메모장 출력

f.write(f'     ∴ 필요철근량 As.req = ρreq × (B·D) = {calc.Asreq:2.3f}㎟ {calc.ch:2s}\n')   #메모장 출력
f.write(f'     철근비검토 : = {calc.ch1:2s}\n\n')   #메모장 출력 
f.write('    - 허용최대중립축 및 인장철근 변형률 검토\n')
f.write(f'     c_max = (δ·εcu / 0.0033 - 0.6) × D = {calc.c_max:2.3f}mm\n        ...여기서 δ (재분배 후 모멘트율) = {calc.δ:2.3}\n')   #메모장 출력
f.write(f'     c  = (As.use·Øs·fy) / (α Øc 0.85 fck·B) = {calc.cc:2.3f}mm  {calc.ch2:2s}\n')   #메모장 출력
f.write(f'     εyd = Øs·fy / Es = {calc.εyd:2.5f} (철근 설계항복변형률)\n     εs  = (d - c) / c ×εcu = {calc.εs:2.5f} {calc.ch3:2s}\n\n')   #메모장 출력
f.write('    - 휨강도 검토\n')
f.write(f'     Mr = As·Øs·fy·( D - β·c ) = {calc.Mr:2.3f}N.mm\n        = {calc.Mr/(10**6):2.3f}kN.m {calc.ch4:2s} Mu= {calc.Mu:2.3f}kN.m   {calc.ch5:2s}  (S.F ={calc.sf:2.3f})\n\n')   #메모장 출력

#------------------------------
#          전단력 검토
#------------------------------
calc.calshear()
f.write('   ▷ 전단력 검토 검토\n\n')
f.write('    - 전단강도 검토\n')
f.write(f'      κ  = 1 + √(200/D) = {calc.κ:2.3f} {calc.sh1:2s}\n')   #메모장 출력
f.write(f'      fctk= 0.7×0.3×(fck+Δf)^⅔ = {calc.fctk:2.3f}MPa\n')   #메모장 출력
f.write(f'      Vc  = [0.85 Øc·κ·(p fck)^⅓ + 0.15 fn] B·D / 1000 = {calc.Vc:2.3f}kN\n')   #메모장 출력  
f.write(f'      Vcd.min = (0.4 Øc·fctk + 0.15 fn) B·D / 1000 = {calc.Vcdmin:2.3f}kN\n')   #메모장 출력 
f.write(f'      ∴ Vcd = Max(Vc, Vcd.min) = {calc.Vcd:2.3f}kN {calc.sh2:2s} = {calc.Vu:2.3f}kN {calc.sh3:2s}\n\n')   #메모장 출력
if calc.Vcd < calc.Vu:
    f.write(f'      사용 전단철근량 Av.use = H{calc.AvDia:2d} x {calc.AvLeg:2.3f}ea = {calc.Avs:2.3f}㎟  (간격 s = {calc.AvSpace:2d}mm)\n')   #전단철근량 산정 출력
    f.write(f'       z  = 0.9 D = {calc.z:2.3f}mm\n')   #단면내부 팔길이 출력 
    
    f.write(f'      θ = {calc.θ:2.3f}°  (콘크리트 스트럿과 주인장철근의 경사각)\n')   #메모장 출력  
    f.write(f'      α = {calc.α:2.3f}°  (전단철근과 부재축의 경사각)\n')   #메모장 출력  
    f.write(f'      Vd = (Øs·fy·Av·z / s) ×cotθ/1000 = {calc.Vd:2.3f}kN\n')   #메모장 출력 
    f.write(f'      Vd.max = (νØc fck B z) / (cotθ+tantθ) / 1000 = {calc.Vdmax:2.3f}kN  {calc.sh4:2s} Vd\n')   #메모장 출력
    f.write(f'      ∴ Vd = Min(Vd, Vd.max) = {min(calc.Vd,calc.Vdmax):2.3f}kN  {calc.sh4:2s} Vu = {calc.Vu:2.3f}kN {calc.sh5:2s} (S.F = {calc.Vd/calc.Vu:2.3f})\n\n')   #메모장 출력

    f.write('    - 최소 전단철근비 및 전단철근간격 검토 \n')
    if calc.ρvmin > calc.ρvuse:
        f.write(f'      사용 전단철근비 ρv.use = Av / (s·B·sinα) = {calc.ρvuse:2.5f}\n')   #메모장 출력
        f.write(f'      최소 전단철근비 ρv.min = 0.08 √(fck) / fy = {calc.ρvmin:2.5f} {calc.sh6:2s}\n')   #메모장 출력
#        
    f.write(f'      종방향 최대간격 s₁max = 0.75D (1+cotα) = {calc.s1max:2.5f}mm {calc.sh7:2s} s₁= {calc.AvSpace:2.3f}mm {calc.sh8:2s}\n')   #메모장 출력
    f.write(f'      횡방향 최대간격 s₂max = Min(0.75D, 600) = {calc.s2max:2.5f}mm {calc.sh9:2s} s₂= {calc.s2:2.3f}mm {calc.sh10:2s}\n\n')   #메모장 출력

#--------------------------------------
#          사용성 검토(균열검토)
#--------------------------------------
calc.calservice()
f.write('   ▷ 사용성 검토(균열검토)\n\n')
f.write(f'      Ms = {calc.Ms:2.3f}kN.m  (사용하중조합-Ⅰ)\n')   #메모장 출력
f.write('    - 균열발생 여부 검토 (비균열 단면으로 가정)\n')
f.write(f'      n  = Es/Ec = 200,000 / (0.077 mc^1.5 * ³√(Fck + Δf)) = {calc.nr:2d}\n')   #메모장 출력
f.write(f'      Xo = (B·H²/2 + (n-1)·As·D) / (B·H + (n-1)·As) = {calc.Xo:2.3f}mm\n')   #메모장 출력
f.write(f'      Io = B·H³/12 + B·H·(H/2-Xo)²+ (n-1)·As·(D-Xo)²= {calc.Io:2.3f}mm⁴\n')   #메모장 출력
if calc.fct <= calc.fctk :
    f.write(f'      fct = Ms / Io×(H-Xo) = {calc.fct:2.3f}MPa {calc.cr1:2s} fctk = {calc.fctk:2.3f}MPa {calc.cr2:2s} \n')   #메모장 출력
    f.write('    - 철근응력제한 검토\n')
    f.write(f'      fs = n·Ms / Io×(D-Xo) =  {calc.fs:2.3f}MPa {calc.cr3:2s} 0.8fy = {0.8*calc.fy:2.3f}MPa {calc.cr4:2s}\n\n')   #메모장
else :
    f.write(f'      fct = Ms / Io×(H-Xo) = {calc.fct:2.3f}MPa {calc.cr1:2s} fctk = {calc.fctk:2.3f}MPa {calc.cr2:2s}\n\n')   #메모장 출력
    f.write('    - 철근응력제한 검토\n')
    f.write(f'      ρ = As/(B·D) =  {calc.p:2.5f}\n')   #메모장
    f.write(f'      k  = -nρ+ √((nρ)²+ 2nρ) = {calc.k:2.3f}  (j= 1-k/3= {1-calc.k/3:2.3f})\n')   #메모장
    f.write(f'      x  = k·d =  {calc.x:2.5f}mm\n')   #메모장
    f.write(f'      fc = 2·Ms / (B·x·(D - x/3)) =  {calc.fc:2.5f}MPa\n')   #메모장
    f.write(f'      fs = Ms / (As ·(D - x/3))   =  {calc.fs:2.5f}MPa {calc.cr3:2s} 0.8fy = {0.8*calc.fy:2.3f}MPa {calc.cr4:2s}\n\n')  #메모장
    
    f.write('    - 간접균열제어 및 최소철근량\n')
    f.write(f'      철 근 직 경 : {calc.AsDia:2d}mm,    철 근 간 격 : {(calc.B-2*calc.Dc)/calc.AsNum:2.3f}mm\n')   #메모장

    f.write(f'      허 용 응 력 : fsa = Max(160,360) = {calc.fsa:2d}MPa {calc.cr5:2s} fs = {calc.fs:2.3f}MPa {calc.cr6:2s}\n')   #메모장

    f.write(f'      최소 철근량 : As.min = kc·k·Act·fct / fsa = {calc.Asmin:2.3f} ㎟ {calc.cr7:2s} As={calc.Asuse:2.3f}㎟ {calc.cr8:2s}\n')   #메모장
    f.write(f'            여기서... Act = B·(H-Xo) = {calc.Act:2.3f} ㎟\n')   #메모장
    f.write(f'                      kc  = 0.4×[1 - fn/(k₁(h/h*)×fct)] = {calc.kc:2.3f}\n')   #메모장    
    f.write(f'                      k   =  {calc.k:2.3f}\n')   #메모장 
    f.write(f'                      fct = fctm = {calc.fct:2.3f}MPa\n')   #메모장  
    f.write(f'                      fsa = {calc.fsa:2.3f}MPa\n')   #메모장    
    