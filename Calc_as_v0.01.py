from cmath import sqrt
from glob import escape


fck = int(input('fck(MPa) = '))
fy = int(input('fy(MPa) = '))
pic = float(input('Φc = '))
pis = float(input('Φs = '))
width = float(input('Width B(mm) = '))
height = float(input('Height H(mm) = '))
cv = float(input("Cover d' = "))
mu = float(input('Mu(kN.m) = '))
if 1.2+1.5*((100-fck)/60)**4 >= 2 :
    n = 2
else :
    n = 1.2 + 1.5*((100-fck)/60)**4
print('n = ',n)
if 0.002 + ((fck-40)/100000) <= 0.002 :
    ecor = 0.002
else :
    ecor = 0.002 + ((fck-40)/100000)
print('ecor = ', ecor)
if 0.0033 - ((fck-40)/100000) >= 0.0033 :
    ecur = 0.0033
else :
    ecur = 0.0033 - ((fck-40)/100000)
print('ecur = ', ecur)
es = 200000 #MPa
alcc = 0.85
fcd = pic * alcc * fck
if fck < 40 :
    fcm = fck + 4
elif fck >= 60 :
    fcm = fck + 6
else :
    fcm = 4 + (fck - 40) / 10
elc = 0.077 * 2500**1.5 * fcm**(1/3)
fcklist = [40, 50, 60, 70, 80, 90]
alpalist = [0.8, 0.78, 0.72, 0.67, 0.63, 0.59]
betalist = [0.4, 0.4, 0.38, 0.37, 0.36, 0.35]
etalist = [1.0, 0.97, 0.95, 0.91, 0.87, 0.84]
if fck <= fcklist[0] :
    alpa = alpalist[0]
elif fck < fcklist[1] :
    alpa = alpalist[0] + (alpalist[1] - alpalist[0]) / (fcklist[1] - fcklist[0]) * (fck - fcklist[0])
elif fck < fcklist[2] :
    alpa = alpalist[1] + (alpalist[2] - alpalist[1]) / (fcklist[2] - fcklist[1]) * (fck - fcklist[1])
elif fck < fcklist[3] :
    alpa = alpalist[2] + (alpalist[3] - alpalist[2]) / (fcklist[3] - fcklist[2]) * (fck - fcklist[2])
elif fck < fcklist[4] :
    alpa = alpalist[3] + (alpalist[4] - alpalist[3]) / (fcklist[4] - fcklist[3]) * (fck - fcklist[3])
elif fck < fcklist[5] :
    alpa = alpalist[4] + (alpalist[5] - alpalist[4]) / (fcklist[5] - fcklist[4]) * (fck - fcklist[4])
else :
    alpa = alpalist[5]
print('alpa =', alpa)
if fck <= fcklist[0] :
    beta = betalist[0]
elif fck < fcklist[1] :
    beta = betalist[0] + (betalist[1] - betalist[0]) / (fcklist[1] - fcklist[0]) * (fck - fcklist[0])
elif fck < fcklist[2] :
    beta = betalist[1] + (betalist[2] - betalist[1]) / (fcklist[2] - fcklist[1]) * (fck - fcklist[1])
elif fck < fcklist[3] :
    beta = betalist[2] + (betalist[3] - betalist[2]) / (fcklist[3] - fcklist[2]) * (fck - fcklist[2])
elif fck < fcklist[4] :
    beta = betalist[3] + (betalist[4] - betalist[3]) / (fcklist[4] - fcklist[3]) * (fck - fcklist[3])
elif fck < fcklist[5] :
    beta = betalist[4] + (betalist[5] - betalist[4]) / (fcklist[5] - fcklist[4]) * (fck - fcklist[4])
else :
    beta = betalist[5]
print('beta = ', beta)
if fck <= fcklist[0] :
    eta = etalist[0]
elif fck < fcklist[1] :
    eta = etalist[0] + (etalist[1] - etalist[0]) / (fcklist[1] - fcklist[0]) * (fck - fcklist[0])
elif fck < fcklist[2] :
    eta = etalist[1] + (etalist[2] - etalist[1]) / (fcklist[2] - fcklist[1]) * (fck - fcklist[1])
elif fck < fcklist[3] :
    eta = etalist[2] + (etalist[3] - etalist[2]) / (fcklist[3] - fcklist[2]) * (fck - fcklist[2])
elif fck < fcklist[4] :
    eta = etalist[3] + (etalist[4] - etalist[3]) / (fcklist[4] - fcklist[3]) * (fck - fcklist[3])
elif fck < fcklist[5] :
    eta = etalist[4] + (etalist[5] - etalist[4]) / (fcklist[5] - fcklist[4]) * (fck - fcklist[4])
else :
    eta = etalist[5]
print('eta = ', eta)
beta1 = beta * 2
fyd = fy * pis
eyd = fyd / es
d = height - cv
A = (fyd**2)/(2*eta*fcd*width)
B = -fyd * d
C = mu * 1000000
asreq = (-B - (B**2 - 4*A*C)**(1/2)) / (2 * A)
print('Asreq = %6.3f mm2' %(asreq))
bararea = [71.30, 126.70, 198.60, 286.50, 387.10, 506.70, 642.40, 794.20]
tmp1 = 1
while tmp1 :
    tmp2 = 1
    while tmp2 :
        dr1 = int(input('Dia of Rebar d(mm) = '))
        nr1 = int(input('Num of Rebar n(ea) = '))
        if dr1 == 13 :
            uar = bararea[1]
        elif dr1 == 16 :
            uar = bararea[2]
        elif dr1 == 19 :
            uar = bararea[3]
        elif dr1 == 22 :
            uar = bararea[4]
        elif dr1 == 25 :
            uar = bararea[5]
        elif dr1 == 29 :
            uar = bararea[6]
        elif dr1 == 32 :
            uar = bararea[7]
        else :
            uar = 0
        asuse = nr1 * uar
        rasuse = asuse / asreq 
        print('Asuse = %6.3f mm2' %(asuse))
        print('Asuse / Asreq = %6.3f' %(rasuse))
        print('Change Rebar?')
        tmp2 = int(input('yes = 1 / no = 0\n'))
    asmin1 = 1.4 / fy * width * d
    asmin2 = 0.25 * fck**(1/2) / fy * width * d
    asmin3 = 4 * asreq / 3
    print('%6.3f, %6.3f, %6.3f' %(asmin1, asmin2, asmin3))
    asmin4 = max(asmin1, asmin2)
    print('Asmin = %6.3f mm2' %(asmin4))
    if asuse > asmin4 :
        print('Asuse > Asmin O.K !!!')
    elif asuse > asmin3 :
        print('Asmin > Asuse > 4/3 Asreq O.K!!!')
    else :
        print('4/3 Asreq > Asuse  N.G!!!')
    asmax = 0.04 * width * d
    print('Asmax = %6.3f mm2' %(asmax))
    if asmax > asuse :
        print('Asmax > Asuse  O.K!!!')
    else :
        print('Asmax < Asuse N.G!!!')
    smax = min(2*height, 250)
    suse = width / nr1
    if smax >= suse :
        print('smax = %6.3fmm >= suse = %6.3fmm   O.K!!!' %(smax, suse))
    else :
        print('smax = %6.3fmm < suse = %6.3fmm   N.G!!!' %(smax, suse))
    print('Change Rebar?')
    tmp1 = int(input('yes = 1 / no = 0\n'))
T = asuse * fyd
C = eta * fcd * width
a = asuse * fyd / (eta * fcd * width)
c = a / beta1
delta = 1 #모멘트 재분배 계수
cmax = ( delta * ecur / 0.0033 - 0.6 ) * d
if cmax >= c :
    print('cmax = %6.3f > c = %6.3f  O.K!!!' %(cmax, c))
else :
    print('cmax = %6.3f < c = %6.3f  N.G!!!' %(cmax, c))
mr = T * ( d - a / 2 ) / 10e5
msf = mr / mu
print('Mr =  %10.3f kN.m' %(mr))
if mr >= mu :
    print('Mr > Mu  O.K!!!, S.F = %3.3f' %(msf))
else :
    print('Mr < Mu  N.G!!!, S.F = %3.3f' %(msf))



    




