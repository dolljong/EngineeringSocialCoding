# GUI 한계상태 단면검토 계산기 

# 심세훈 / shsim@soosungeng.com / 22.09.08 작성

#from distutils.cmd import Command
import tkinter.ttk as ttk 
import tkinter.messagebox as msgbox
from tkinter import *

root = Tk()
root.title("LSD calculator SSH")
root.geometry("480x400") 

#ㅡㅡㅡㅡㅡㅡㅡ제원 입력창ㅡㅡㅡㅡㅡㅡㅡㅡ

# pi_c
label_pi_c = Label(root, text="Φc") 
label_pi_c.pack()
e_pi_c = Entry(root, width=6) 
e_pi_c.pack()
e_pi_c.insert(END,0.65)

# pi_s
label_pi_s = Label(root, text="Φs") 
label_pi_s.pack()
e_pi_s = Entry(root, width=6) 
e_pi_s.pack()
e_pi_s.insert(END,0.90)

# alpa
label_alpa = Label(root, text="α") 
label_alpa.pack()
e_alpa = Entry(root, width=6) 
e_alpa.pack()
e_alpa.insert(END,0.80)

# beta
label_beta = Label(root, text="β") 
label_beta.pack()
e_beta = Entry(root, width=6) 
e_beta.pack()
e_beta.insert(END,0.40)

# fy 
label_fy = Label(root, text="fy(Mpa)") 
label_fy.pack()
e_fy = Entry(root, width=6) 
e_fy.pack()
#e_fy.insert(END,400)

# fck 
label_fck = Label(root, text="fck(Mpa)") 
label_fck.pack()
e_fck = Entry(root, width=6) 
e_fck.pack()
#e_fck.insert(END,30)

# B
label_B = Label(root, text="B(mm)") 
label_B.pack()
e_B = Entry(root, width=6) 
e_B.pack()
e_B.insert(END,1000)

# H(mm)
label_H = Label(root, text="H(mm)") 
label_H.pack()
e_H = Entry(root, width=6) 
e_H.pack()
#e_H.insert(END,600)

# dp (피복) / d = H-dp
label_dp = Label(root, text="d'(mm)") 
label_dp.pack()
e_dp = Entry(root, width=6) 
e_dp.pack()
#e_dp.insert(END,100)

# Mu
label_Mu = Label(root, text="Mu(kN.m)") 
label_Mu.pack()
e_Mu = Entry(root, width=8) 
e_Mu.pack()
#e_Mu.insert(END,150.75)

# 철근직경 
label_dia = Label(root, text="Dia(mm) \n ex) 10,13,16...32")
label_dia.pack() 
e_dia = Entry(root, width=8) 
e_dia.pack()
#e_dia.insert(END,22)

# C.T.C
label_CTC = Label(root, text="C.T.C(mm)") 
label_CTC.pack()
e_CTC = Entry(root, width=8) 
e_CTC.pack()
#e_CTC.insert(END,125)

#ㅡㅡㅡㅡㅡㅡ계산함수ㅡㅡㅡㅡㅡㅡㅡ

# 함수1 : 필요철근량 계산
def cal_As(): 
    global pi_c #전역번수로 지정
    global pi_s 
    global alpa 
    global beta 
    global fy 
    global fck  
    global B 
    global H 
    global dp 
    global Mu 
    global d
  
    pi_c = float(e_pi_c.get()) # 입력값을 이름에 맞게 변수로 지정
    pi_s = float(e_pi_s.get())
    alpa = float(e_alpa.get())
    beta = float(e_beta.get())
    fy = int(e_fy.get())
    fck = int(e_fck.get())
    B = int(e_B.get())
    H = int(e_H.get())
    dp = int(e_dp.get())
    Mu = float(e_Mu.get())
    d = H-dp
  
    # V1,2,3 : V1*As²+V2*As+V3=0
    V1 = beta*pi_s**2*fy**2/(alpa*pi_c*0.85*fck*B)
    V2 = pi_s*fy*d
    V3 = Mu*10**6
    
    As = (V2-(V2**2-4*V1*V3)**0.5)/(2*V1)
    global As_round #전역변수 : 이 변수는 이 함수가 끝난 이후에도 사라지지 않음 ! 지정안해주면 함수 인식X 그래서 함수2에서 if로 비교해줄수있음! 
    As_round = round(As,3) # round(변수, 수소점자리) : 소수점자리 표기
    label_Asreq.configure(text="As.req = " + str(As_round) + "mm²") # configure : 해당레이블에 값 출력  

# 함수2 : 사용철근량 및 안전율 
# 콤보박스로 바꾸는것도 고려해보기. but 타이핑이 더 빠르고 편하다.

def cal_Ause(): 
    dia = float(e_dia.get())
    if dia == 10:
        dia = 71.33 #사용철근 1개당 단면적
    elif dia==13:
        dia=126.7
    elif dia==16:
        dia=198.6
    elif dia==19:
        dia=286.5
    elif dia==22:
        dia=387.1
    elif dia==25:
        dia=506.7
    elif dia==29:
        dia=642.4
    elif dia==32:
        dia=794.2
    elif dia==35:
        dia=956.6
    else : msgbox.showwarning("경고","해당 규격의 철근은 지원되지 않습나다.") #철근직경 경고 메시지 띄우기
    
    # CTC로 사용철근량 산출
    CTC = float(e_CTC.get())
    CTC2 = 1000/CTC
    Ause = dia*CTC2
    global Ause_round
    Ause_round = round(Ause,3)
    global As_round 
    
    # 레이블에 보여줄 Fs, As.min
    if Ause_round > As_round : #global로 전역변수 지정해줘서 이렇게 비교가능 !
        Fs = round(Ause_round/As_round,2) #안전율 소수 2번째까지 
        label_Asuse.configure(text=
        "As.use = " + str(Ause_round) + "mm² " + " [Fs= "+str(Fs)+"]  ∴ O.K " )
    else:
        Fs = round(Ause_round/As_round,2) #안전율 소수 2번째까지 
        label_Asuse.configure(text="As.use = " + str(Ause_round) + "mm² " + " \nFs= "+str(Fs)+"  ∴ N.G") 
       # configure : 해당레이블에 값 출력 

# 함수3 : Asmin 최소철근량 검토
def cal_Asmin():
    Asmin1 = 0.25*(fck)**0.5/fy*B*d
    Asmin2 = 1.4/fy*B*d
    Asmin3 = As_round*4/3
    Asmin = round(min(Asmin1,Asmin2,Asmin3),3)
    if As_round < Asmin :
        label_Asmin.configure(text="As = "+str(Ause_round)+"< As.min = "+str(Asmin)+" ∴ O.K ")  
    else : 
        label_Asmin.configure(text="As = "+str(Ause_round)+"> As.min = "+str(Asmin)+" ∴ N.G ") 

# 함수4 : 중립축 깊이 검토
#  εcu 계산

def cal_Cmax():
    if 0.0033 - ((fck-40)/100000) >= 0.0033 :
        ecu = 0.0033
    else :
        ecu = 0.0033 - ((fck-40)/100000)

    Cmax = (1*ecu/0.0033-0.6)*d
    c = pi_s*Ause_round*fy/(alpa*pi_c*0.85*fck*B)
    global c_round
    c_round = round(c,3)
    if c < Cmax :
        label_Cmax.configure(text="c = "+str(c_round)+"mm < Cmax = "+str(Cmax)+"mm ∴ O.K ")
    else :
        label_Cmax.configure(text="c = "+str(c_round)+"mm > Cmax = "+str(Cmax)+"mm ∴ N.G ")

# 함수5 : 설계휨강도 검토
def cal_Mr():
    Mr1 = Ause_round*pi_s*fy*(d-beta*c_round)/10**6
    Mr = round(Mr1,3)
    if Mr > Mu :
        label_Mr.configure(text="Mr = "+str(Mr)+"kN.m > Mu = "+str(Mu)+"kN.m ∴ O.K ")
    else :
        label_Mr.configure(text="Mr = "+str(Mr)+"kN.m < Mu = "+str(Mu)+"kN.m ∴ N.G ")

#ㅡㅡㅡㅡㅡㅡㅡ레이블 및 버튼 ㅡㅡㅡㅡㅡㅡㅡ
      
# 계산결과 레이블1 : As,req = ?
label_Asreq = Label(root, text="As.req = ?",width=40, height=2, bg="white", relief="solid" ) 
label_Asreq.pack()
# 검토버튼1 : [SOLVE] As.req
btn1 = Button(root, text="[SOLVE] As.req", command=cal_As)
btn1.pack()

# 계산결과 레이블2 : As.use = ?
label_Asuse = Label(root, text="As.use = ?",width=40, height=2, bg="white", relief="solid"  ) 
label_Asuse.pack()
# 검토버튼2 : [SOLVE] As.use
btn2 = Button(root, text="[SOLVE] As.use", command=lambda:[cal_Ause(), cal_Asmin()]) #lambda : 한 버튼에 여러함수를 동시에 실행
btn2.pack()

# 계산결과 레이블 Asmin
label_Asmin = Label(root, text="As.min = ?",width=40, height=2, bg="white", relief="solid"  ) 
label_Asmin.pack()

# 계산결과 레이블 Mr : Cmax = ?
label_Cmax = Label(root, text="Cmax = ?",width=40, height=2, bg="white", relief="solid"  ) 
label_Cmax.pack()

# 계산결과 레이블 Mr :  Mr = ?
label_Mr = Label(root, text="Mr = ?",width=40, height=2, bg="white", relief="solid"  ) 
label_Mr.pack()

# 검토버튼 Cmax, Mr : [SOLVE] others
btn3 = Button(root, text="[SOLVE] Cmax, Mr ", command=lambda:[cal_Cmax(), cal_Mr()])
btn3.pack()

# ㅡㅡㅡㅡㅡ위젯 위치조정ㅡㅡㅡㅡㅡㅡ
# grid로 배치하면 왜 안되는지 모르겠음.

# 위젯 위치조정1 : 레이블위치

#전체위치 조정
x_all=0
y_all=0

# 1열 : 레이블위치
label_pi_c.place(x=30+x_all, y=30+y_all)
e_pi_c.place(x=60+x_all, y=30+y_all)

label_pi_s.place(x=140+x_all, y=30+y_all)
e_pi_s.place(x=170+x_all, y=30+y_all)

label_alpa.place(x=270+x_all, y=30+y_all)
e_alpa.place(x=290+x_all, y=30+y_all)

label_beta.place(x=370+x_all, y=30+y_all)
e_beta.place(x=400+x_all, y=30+y_all)

#2열
label_fy.place(x=10+x_all, y=60+y_all)
e_fy.place(x=60+x_all, y=60+y_all)

label_fck.place(x=110+x_all, y=60+y_all)
e_fck.place(x=170+x_all, y=60+y_all)

label_B.place(x=240+x_all, y=60+y_all)
e_B.place(x=290+x_all, y=60+y_all)
           
label_H.place(x=350+x_all, y=60+y_all)
e_H.place(x=400+x_all, y=60+y_all)

#3열          
label_dp.place(x=10+x_all, y=90+y_all)
e_dp.place(x=60+x_all, y=90+y_all)
           
label_Mu.place(x=110+x_all, y=90+y_all)
e_Mu.place(x=170+x_all, y=90+y_all)

#4열
label_dia.place(x=15+x_all, y=180+y_all)
e_dia.place(x=100+x_all, y=175+y_all)

label_CTC.place(x=180+x_all, y=180+y_all)
e_CTC.place(x=250+x_all, y=175+y_all)

# 위젯 위치조정2 : 버튼, 출력창 위치
btn1.place(x=30+x_all, y=120+y_all)
label_Asreq.place(x=160+x_all, y=120+y_all)

btn2.place(x=30+x_all, y=220+y_all)
label_Asuse.place(x=160+x_all, y=220+y_all)
label_Asmin.place(x=160+x_all, y=254+y_all)

btn3.place(x=15+x_all, y=300+y_all)
label_Cmax.place(x=160+x_all, y=300+y_all)
label_Mr.place(x=160+x_all, y=330+y_all)

#ㅡㅡㅡㅡㅡ메뉴바ㅡㅡㅡㅡㅡ
# 메뉴바 함수 : 메시지박스 
def info(): # showinfo : 메시지박스에 알림 아이콘 뜸
    msgbox.showinfo("제작정보","버전 : ver.0(프로토타입) \n\n 제작일 : 22.09.08 \n\n 제작자 : 심세훈") 
def quit():
       root.destroy()

# 메뉴바 선언
menubar = Menu(root)

#메뉴1 : 파일
menu_file = Menu(menubar, tearoff=0) # 메뉴바정의. tearoff=0 안하면 필요없는 선 생김
menu_file.add_command(label="열기(Ctrl+O)") #메뉴바 하위 메뉴 
menu_file.add_command(label="저장(Ctrl+S)")
menu_file.add_command(label="인쇄(Ctrl+P)")
menu_file.add_separator() #하위메뉴 구분선
menu_file.add_command(label="나가기(Ctrl+W)",command=quit)
menubar.add_cascade(label="파일(F)", menu=menu_file) #메뉴바의 제목

#메뉴2 : 설계기준(S)
menu_standard = Menu(menubar, tearoff=0) # 메뉴바정의. 
menu_standard.add_radiobutton(label="도로교설계기준 2015") # checkbutton : 하나만 유지되는 체크 버튼
menu_standard.add_radiobutton(label="KDS 24 14 21")
menubar.add_cascade(label="설계기준(S)", menu=menu_standard) #메뉴바의 제목
root.config(menu=menubar) #메뉴바를 보이게 해줌

#메뉴3 : 도움말(H)
menu_help = Menu(menubar, tearoff=0) # 메뉴바정의. 
menu_help.add_command(label="도움말목차(Contents)") #메뉴바 하위 메뉴 
menu_help.add_command(label="도움사이트 : 다정다감")
menu_help.add_separator() #하위메뉴 구분선
menu_help.add_command(label="About...", command=info)
menubar.add_cascade(label="도움말(H)", menu=menu_help) #메뉴바의 제목
root.config(menu=menubar) #메뉴바를 보이게 해줌

root.mainloop()
