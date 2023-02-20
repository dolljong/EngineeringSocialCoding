# 강희의 원대한 꿈을 위해 시작하는 코딩 작업
# 중단 하지 말고...
# 외부 프로그램을 구동하는 방법

import tkinter as tk  # tkinter 모듈을 프로그램의 네임 스페이스로 가져 오지만 이름을 tk로 바꾼다.
from tkinter import ttk
from math import *
from tkinter.font import Font  # tkinter.font 모듈을 임포트하고 Font 클래스 생성자를 사용 '글꼴 객체'를 만듬
from tkinter.filedialog import *
from tkinter import scrolledtext
from tkinter import messagebox as msg
# import pymysql  # DB활용을 위한... 실패!!!!!!!!!!!!!!!!!!
import os  # 파일 이름을 가져오기 위해 os모듈을 임포트
import subprocess  # 외부파일 실행용
import datetime  # 날짜+시간탑재


# 메인 메뉴 코드 ---------------------------------------------------------------
RCDesign = tk.Tk()  # 생성자를 호출해 Tk클래스의 인스턴스를 생성한다. RCDesign이라는 메인창을 정의

RCDesign.title('Kanghee Project-RC단면검토')  # 창 우상단 제목
RCDesign.geometry('1300x700+100+30')  # 크기+x좌표+y좌표

RCDesign_pwin=ttk.Panedwindow(RCDesign, orient=tk.HORIZONTAL)  # 페인드 윈도우 생성, 윈도내 의젯은 수평배열(VERTICAL하면 수직배열)
## 페인드윈도, 프레임,위젯등은 원칙적으로 수직배열이 원칙인듯 orient=tk.HORIZONTAL 요게 수평배열로 만드는듯
RCDesign_pwin.pack(fill=tk.BOTH, expand=True)  # 양쪽채우기, 확장가능

#-각종변수들 -----------------------------------------------------------------
fck_var = tk.DoubleVar() # fck_var 라는 IntVar()는 Integer변수 선언
fy_var = tk.DoubleVar()
fvy_var = tk.DoubleVar()
width_var = tk.DoubleVar() 
height_var = tk.DoubleVar()
cover_var = tk.DoubleVar() 
pi_c = tk.DoubleVar() # 콘크리트 재료계수
pi_s = tk.DoubleVar() # 철근 또는 PT의 재료계수
ne = tk.DoubleVar() # 상승 곡선부의 형상을 나타내는 지수
eco = tk.DoubleVar() # 최대응력에 처음 도달할 때의 변형률
ecu = tk.DoubleVar() # 극한변형률
alpha = tk.DoubleVar() # 압축합력의 크기계수
beta = tk.DoubleVar() # 직용점 위치계수
nu = tk.DoubleVar() # 극한한계상태에서 등가응력의 크기를 나타내는 계수
beta1 = tk.DoubleVar() # 등가직사각형 응력블록 계수, 중립축 깊이 구할때 사용
Mu_var = tk.DoubleVar() 
Vu_var = tk.DoubleVar() 
depth_var = tk.DoubleVar()
a1 = tk.DoubleVar()
#------------------------------------------------------------------------------
#===============================================================================
input_frm = tk.LabelFrame(RCDesign_pwin, text='자료 입력',padx = 4, pady = 4, bd = 2, relief = tk.RIDGE,labelanchor=tk.NW)  # 페인드윈도1안에 라벨프레임 추가배치, 페인드윈도내에서는 위 orient=HOR..에 의해 수평 배치

input1_frm = tk.Frame(input_frm, padx = 4, pady = 4, bd = 2, relief = tk.RIDGE)  # 프레임안에 또 프레임 넣기 Layout정리 땜에
input1_frm.pack()

def TitleWrite(event):
    text="검토부재 : "+str(member_var.get())  # text는 단순 옮겨 적기용이므로 global 변수 지정은 필요 없다?
    input_box.insert(tk.END,text)
    output_box.insert(tk.END,text)
    
member_lbl = ttk.Label(input1_frm, text = "검토부재 : ") 
member_lbl.grid(column = 0, row = 0, pady = 3, sticky = tk.E)

member_var = tk.StringVar()
# StringVar()는 string변수 선언, IntVar()는 Integer변수 선언,DoubleVar()는 float변수선언, BooleanVar()는 True False변수선언
member_ent = ttk.Entry(input1_frm,width=49, justify=tk.RIGHT,textvariable=member_var)
member_ent.bind("<FocusOut>",TitleWrite)
member_ent.grid(column = 1, row = 0, padx = 3, pady = 3, sticky = tk.W)

def check():
    global pi_c
    global pi_s
    combi_val = str(combi_var.get())
    if combi_val == "1":
        pi_c = 0.65
        pi_s = 0.90
    else:
        pi_c = 1.0
        pi_s = 1.0
    pi_c_out_lbl.config(text= str(pi_c))
    pi_s_out_lbl.config(text= str(pi_s))
    text="\n재료계수 : "+str(pi_c)+"  "+str(pi_s)
    input_box.insert(tk.END,text)

combi_var=tk.IntVar()
combi1_rdo=tk.Radiobutton(input1_frm, text="극한하중조합", value=1, variable=combi_var, command=check)
combi1_rdo.grid(column = 1, row = 1, padx = 3, pady = 3, sticky = tk.W)
combi2_rdo=tk.Radiobutton(input1_frm, text="극단,사용,피로 하중조합", value=2, variable=combi_var, command=check)
combi2_rdo.grid(column = 1, row = 2, padx = 3, pady = 3, sticky = tk.W)

#-------------------------------------------------------------------------------
input2_frm = tk.Frame(input_frm, padx = 4, pady = 4, bd = 2, relief = tk.RIDGE)  # 프레임안에 또 프레임 넣기 Layout정리 땜에
input2_frm.pack()

#--첫째줄-------------------------------------------------------------------------

def FactorCalc(event):
    global fck_var
    global ne
    global eco 
    global ecu 
    global alpha 
    global beta 
    global nu 
    global beta1
    if fck_var.get() <= 40:
        ne = 2.00
        eco = 0.0020
        ecu = 0.0033
        alpha = 0.80
        beta = 0.40
        nu = 1.0
        beta1 = 0.80
    elif fck_var.get() <= 50:
        ne = 1.92
        eco = 0.0021
        ecu = 0.0032
        alpha = 0.78
        beta = 0.40
        nu = 0.97
        beta1 = 0.80
    elif fck_var.get() <= 60:
        ne = 1.50
        eco = 0.0022
        ecu = 0.0031
        alpha = 0.72
        beta = 0.38
        nu = 0.95
        beta1 = 0.76
    elif fck_var.get() <= 70:
        ne = 1.29
        eco = 0.0023
        ecu = 0.0030
        alpha = 0.67
        beta = 0.37
        nu = 0.91
        beta1 = 0.74
    elif fck_var.get() <= 80:
        ne = 1.22
        eco = 0.0024
        ecu = 0.0029
        alpha = 0.63
        beta = 0.36
        nu = 0.87
        beta1 = 0.72
    elif fck_var.get() <= 90:
        ne = 1.20
        eco = 0.0025
        ecu = 0.0028
        alpha = 0.59
        beta = 0.35
        nu = 0.84
        beta1 = 0.70
    ne_out_lbl.config(text= str(ne))
    eco_out_lbl.config(text= str(eco))    
    ecu_out_lbl.config(text= str(ecu))
    alpha_out_lbl.config(text= str(alpha))    
    beta_out_lbl.config(text= str(beta))
        
def Input1Write(event):
    text1="\nfck : "+ str(fck_var.get())+" MPa"
    input_box.insert(tk.END,text1)
    text2="\nfy  : "+ str(fy_var.get())+" MPa"
    input_box.insert(tk.END,text2)
    text3="\nfvy : "+ str(fvy_var.get())+" MPa"
    input_box.insert(tk.END,text3)
    text4="\nΦC : "+ str(pi_c)
    input_box.insert(tk.END,text4)
    text5="\nΦS : "+ str(pi_s)
    input_box.insert(tk.END,text5)
    text6="\nα : "+ str(alpha)
    input_box.insert(tk.END,text6)
    text7="\nβ : "+ str(beta)
    input_box.insert(tk.END,text7)
    text8="\nn : "+ str(ne)
    input_box.insert(tk.END,text8)
    text9="\neco : "+ str(eco)
    input_box.insert(tk.END,text9)
    text10="\necu : "+ str(ecu)
    input_box.insert(tk.END,text10)
    text11="\n\nfck:"+ str(fck_var.get())+"MPa, fy:"+ str(fy_var.get())+"MPa, fvy:"+ str(fvy_var.get())+"MPa"
    output_box.insert(tk.END,text11)
    text12="\n\nΦC:"+str(pi_c)+", ΦS:"+str(pi_s)+", α:"+ str(alpha)+", β:"+ str(beta)+", n:"+ str(ne)+", eco:"+ str(eco)+", ecu:"+ str(ecu)
    output_box.insert(tk.END,text12)

fck_lbl = ttk.Label(input2_frm, text = "fck : ") 
fck_lbl.grid(column = 1, row = 1, pady = 3, sticky = tk.E) 

fck_ent = ttk.Entry(input2_frm,width=10,justify=tk.RIGHT,textvariable=fck_var)
fck_ent.bind("<FocusOut>",FactorCalc)
fck_ent.grid(column = 2, row = 1, padx = 3, pady = 3, sticky = tk.W)

blank1_lbl = ttk.Label(input2_frm, text = "MPa,   ")
blank1_lbl.grid(column = 3, row = 1, pady = 3, sticky = tk.W) 

fy_lbl = ttk.Label(input2_frm, text = "fy : ") 
fy_lbl.grid(column = 4, row = 1, pady = 3, sticky = tk.E)

fy_ent = ttk.Entry(input2_frm,width=10,justify=tk.RIGHT,textvariable=fy_var) 
fy_ent.grid(column = 5, row = 1, padx = 3, pady = 3, sticky = tk.W)

blank2_lbl = ttk.Label(input2_frm, text = "MPa,   ") 
blank2_lbl.grid(column = 6, row = 1, pady = 3, sticky = tk.W)

fvy_lbl = ttk.Label(input2_frm, text = "fvy : ")
fvy_lbl.grid(column = 7, row = 1, pady = 3, sticky = tk.E)

fvy_ent = ttk.Entry(input2_frm,width=10, justify=tk.RIGHT,textvariable=fvy_var)
fvy_ent.bind("<FocusOut>",Input1Write)
fvy_ent.grid(column = 8, row = 1, padx = 3, pady = 3, sticky = tk.W)

blank3_lbl = ttk.Label(input2_frm, text = "MPa") 
blank3_lbl.grid(column = 9, row = 1, pady = 3, sticky = tk.W)

#--둘째줄------------------------------------------------------------------------
pi_c_lbl = ttk.Label(input2_frm, text = "ΦC : ") 
pi_c_lbl.grid(column = 1, row = 2, pady = 3, sticky = tk.E) 
pi_c_out_lbl = ttk.Label(input2_frm, text = "None") 
pi_c_out_lbl.grid(column = 2, row = 2, pady = 3, sticky = tk.W)

pi_s_lbl = ttk.Label(input2_frm, text = "ΦS : ") 
pi_s_lbl.grid(column = 3, row = 2, pady = 3, sticky = tk.E) 
pi_s_out_lbl = ttk.Label(input2_frm, text = "None") 
pi_s_out_lbl.grid(column = 4, row = 2, pady = 3, sticky = tk.W) 

alpha_lbl = ttk.Label(input2_frm, text = "α : ") 
alpha_lbl.grid(column = 5, row = 2, pady = 3, sticky = tk.E) 
alpha_out_lbl = ttk.Label(input2_frm, text = "None") 
alpha_out_lbl.grid(column = 6, row = 2, pady = 3, sticky = tk.W)

beta_lbl = ttk.Label(input2_frm, text = "β : ") 
beta_lbl.grid(column = 7, row = 2, pady = 3, sticky = tk.E) 
beta_out_lbl = ttk.Label(input2_frm, text = "None") 
beta_out_lbl.grid(column = 8, row = 2, pady = 3, sticky = tk.W) 

#--세째줄------------------------------------------------------------------------
ne_lbl = ttk.Label(input2_frm, text = "n : ") 
ne_lbl.grid(column = 1, row = 3, pady = 3, sticky = tk.E) 
ne_out_lbl = ttk.Label(input2_frm, text = "None") 
ne_out_lbl.grid(column = 2, row = 3, pady = 3, sticky = tk.W)

eco_lbl = ttk.Label(input2_frm, text = "εco : ") 
eco_lbl.grid(column = 3, row = 3, pady = 3, sticky = tk.E) 
eco_out_lbl = ttk.Label(input2_frm, text = "None") 
eco_out_lbl.grid(column = 4, row = 3, pady = 3, sticky = tk.W)

ecu_lbl = ttk.Label(input2_frm, text = "εcu : ") 
ecu_lbl.grid(column = 5, row = 3, pady = 3, sticky = tk.E) 
ecu_out_lbl = ttk.Label(input2_frm, text = "None") 
ecu_out_lbl.grid(column = 6, row = 3, pady = 3, sticky = tk.W)

#--넷째줄------------------------------------------------------------------------
def Input2Write(event):
    text1="\n폭   : "+ str(width_var.get())+" mm"
    input_box.insert(tk.END,text1)
    text2="\n높이 : "+ str(height_var.get())+" mm"
    input_box.insert(tk.END,text2)
    text3="\n피복 : "+ str(cover_var.get())+" mm"
    input_box.insert(tk.END,text3)
    text4="\n\n폭:"+ str(width_var.get())+"mm,  높이:"+ str(height_var.get())+"mm,  피복:"+ str(cover_var.get())+"mm"
    output_box.insert(tk.END,text4)
    
width_lbl = ttk.Label(input2_frm, text = "폭 : ") 
width_lbl.grid(column = 1, row = 4, pady = 3, sticky = tk.E) 

width_ent = ttk.Entry(input2_frm,width=10,justify=tk.RIGHT,textvariable=width_var)
width_ent.grid(column = 2, row = 4, padx = 3, pady = 3, sticky = tk.W)

blank4_lbl = ttk.Label(input2_frm, text = "mm,   ")
blank4_lbl.grid(column = 3, row = 4, pady = 3, sticky = tk.W) 

height_lbl = ttk.Label(input2_frm, text = "높이 : ") 
height_lbl.grid(column = 4, row = 4, pady = 3, sticky = tk.E) 


height_ent = ttk.Entry(input2_frm,width=10,justify=tk.RIGHT,textvariable=height_var)
height_ent.grid(column = 5, row = 4, padx = 3, pady = 3, sticky = tk.W)

blank5_lbl = ttk.Label(input2_frm, text = "mm,   ")
blank5_lbl.grid(column = 6, row = 4, pady = 3, sticky = tk.W)

cover_lbl = ttk.Label(input2_frm, text = "피복 : ") 
cover_lbl.grid(column = 7, row = 4, pady = 3, sticky = tk.E) 

cover_ent = ttk.Entry(input2_frm,width=10,justify=tk.RIGHT,textvariable=cover_var)
cover_ent.bind("<FocusOut>",Input2Write)
cover_ent.grid(column = 8, row = 4, padx = 3, pady = 3, sticky = tk.W)

blank6_lbl = ttk.Label(input2_frm, text = "mm")
blank6_lbl.grid(column = 9, row = 4, pady = 3, sticky = tk.W) 

#--다섯째줄------------------------------------------------------------------------
def Input3Write(event):
    text1="\nMu   : "+ str(Mu_var.get())+" kN.m"
    input_box.insert(tk.END,text1)
    text2="\nVu  : "+ str(Vu_var.get())+" kN"
    input_box.insert(tk.END,text2)
    text3="\nd  : "+ str(depth_var.get())+" mm"
    input_box.insert(tk.END,text3)
    text4="\n\nMu:"+ str(Mu_var.get())+"kN.m,  Vu:"+ str(Vu_var.get())+"kN,  d:"+ str(depth_var.get())+"mm"
    output_box.insert(tk.END,text4)
    text5="\n\nMd = As x ΦS x fy x (d - β x c) ------------------------ ① \nc = As x ΦS x fy / (α x ΦC x 0.85 x fck x b) ---------- ② \n\n①식과 ②식을 연립하여 필요 철근량을 구한다." 
    output_box.insert(tk.END,text5)
    a1 = beta.get()#*pi_s.get()**2*fy_var.get()**2/(alpha.get()*pi_c.get()*0.85*fck_var.get()*width_var.get())
    text6="\na  : "+ str(a1.get())      # 타입이 지정된 변수는 *.get()으로 저장된 값을 반환한다.
    output_box.insert(tk.END,text6)
    
Mu_lbl = ttk.Label(input2_frm, text = "Mu : ") 
Mu_lbl.grid(column = 1, row = 5, pady = 3, sticky = tk.E) 
Mu_ent = ttk.Entry(input2_frm,width=10,justify=tk.RIGHT,textvariable=Mu_var)
Mu_ent.grid(column = 2, row = 5, padx = 3, pady = 3, sticky = tk.W)

blank7_lbl = ttk.Label(input2_frm, text = "kN.m,   ")
blank7_lbl.grid(column = 3, row = 5, pady = 3, sticky = tk.W) 

Vu_lbl = ttk.Label(input2_frm, text = "Vu : ") 
Vu_lbl.grid(column = 4, row = 5, pady = 3, sticky = tk.E) 
Vu_ent = ttk.Entry(input2_frm,width=10,justify=tk.RIGHT,textvariable=Vu_var)
Vu_ent.grid(column = 5, row = 5, padx = 3, pady = 3, sticky = tk.W)

blank8_lbl = ttk.Label(input2_frm, text = "kN,   ")
blank8_lbl.grid(column = 6, row = 5, pady = 3, sticky = tk.W)

depth_lbl = ttk.Label(input2_frm, text = "d : ") 
depth_lbl.grid(column = 7, row = 5, pady = 3, sticky = tk.E) 
depth_ent = ttk.Entry(input2_frm,width=10,justify=tk.RIGHT,textvariable=depth_var)
depth_ent.bind("<FocusOut>",Input3Write)
depth_ent.grid(column = 8, row = 5, padx = 3, pady = 3, sticky = tk.W)

blank9_lbl = ttk.Label(input2_frm, text = "mm")
blank9_lbl.grid(column = 9, row = 5, pady = 3, sticky = tk.W) 

#--결과 줄------------------------------------------------------------------------------
ouput_check_frm = tk.Frame(input_frm, padx = 4, pady = 4)#, bd = 2, relief = tk.RIDGE)
ouput_check_frm.pack()

reqAs_lbl1 = ttk.Label(ouput_check_frm, text = "Md = As x ΦS x fy x (d - β x c) ------------------------ ① \nc = As x ΦS x fy / (α x ΦC x 0.85 x fck x b) ---------- ② \n①식과 ②식을 연립하여 필요 철근량을 구한다.") 
reqAs_lbl1.grid(column = 1, row = 1, pady = 3, sticky = tk.E)




#--결과 줄------------------------------------------------------------------------------
rebar_check_frm = tk.Frame(input_frm, padx = 4, pady = 4, bd = 2, relief = tk.RIDGE)
rebar_check_frm.pack()

'''
fck_var = tk.IntVar() # fck_var 라는 IntVar()는 Integer변수 선언
fy_var = tk.IntVar()
fvy_var = tk.IntVar()
width_var = tk.IntVar() 
height_var = tk.IntVar() 
cover_var = tk.IntVar() 
pi_c = tk.DoubleVar() # 콘크리트 재료계수
pi_s = tk.DoubleVar() # 철근 또는 PT의 재료계수
ne = tk.DoubleVar() # 상승 곡선부의 형상을 나타내는 지수
eco = tk.DoubleVar() # 최대응력에 처음 도달할 때의 변형률
ecu = tk.DoubleVar() # 극한변형률
alpha = tk.DoubleVar() # 압축합력의 크기계수
beta = tk.DoubleVar() # 직용점 위치계수
nu = tk.DoubleVar() # 극한한계상태에서 등가응력의 크기를 나타내는 계수
beta1 = tk.DoubleVar() # 등가직사각형 응력블록 계수, 중립축 깊이 구할때 사용
Mu_var = tk.DoubleVar() 
Vu_var = tk.DoubleVar() 
depth_var = tk.DoubleVar()
'''




#--버튼줄------------------------------------------------------------------------------
input_btn_frm = tk.Frame(input_frm, padx = 4, pady = 4)
input_btn_frm.pack()

def InputReadFile(event):  # 열기 클릭시 호출되는 함수 정의
    file=askopenfilename(title="파일열기",filetypes=(("텍스트파일","*.txt"),("모든파일","*.*")))
    # Main.title(os.path.basename(file)+"-메모장")
    input_box.delete(1.0,tk.END)
    f=open(file,"r")
    # read()는 파일내용을 모두 문자열로 리턴해준다.
    # 문자셋은 서로 일치 시켜야 열수 있다. 윈도우 메모장에서 ANSI로 저장하면 확인 가능
    # UTF-8로 저장되면 지금 현재 연습에선 열 수 없다.
    line=f.readlines()
    input_box.insert(1.0,f.read())
    f.close()

   
input_read_btn = ttk.Button(input_btn_frm, text = "입력파일 열기")
input_read_btn.bind("<Return>",InputReadFile)
input_read_btn.bind("<Button-1>",InputReadFile)
input_read_btn.pack(side = tk.LEFT)


def InputSaveFile(event):  # 저장 클릭시 호출되는 함수 정의
    # 쓰기모드로 열고 사용자가 확장자명을 지정하지 않으면 *.txt로 저징한다
    file=asksaveasfile(mode="w",defaultextension=".txt",filetype=(("텍스트파일","*.txt"),("모든파일","*.*")))
    # 그런데 파일이 없다면 무효화 처리해준다.
    if file is None:
        return
    # 저장을 위해 텍스트 위젯의 내용을 첨부터 끝까지 가져옴
    text_input=str(input_box.get(1.0,tk.END))
    file.write(text_input)  # 파일저장, file에 ts를 쓴다.
    file.close()

input_write_btn = ttk.Button(input_btn_frm, text = "입력파일 저장")
input_write_btn.bind("<Return>",InputSaveFile)
input_write_btn.bind("<Button-1>",InputSaveFile)
input_write_btn.pack(side = tk.LEFT)

#-------------------------------------------------------------------------------
scrol_w  = 48  # 스크롤텍스트박스의 폭
scrol_h  = 10  # 스크롤텍스트박스의 높이
input_box = scrolledtext.ScrolledText(input_frm, width = scrol_w, height = scrol_h, wrap = tk.WORD)
input_box.pack()

RCDesign_pwin.add(input_frm)

#===============================================================================

output_frm = tk.LabelFrame(RCDesign_pwin, text='결과 출력',padx = 4, pady = 4, bd = 2, relief = tk.RIDGE,labelanchor=tk.NW)  # 페인드윈도1안에 프레임배치

scrol_w  = 80  # 스크롤텍스트박스의 폭
scrol_h  = 20  # 스크롤텍스트박스의 높이
output_box = scrolledtext.ScrolledText(output_frm, width = scrol_w, height = scrol_h, wrap = tk.WORD)
output_box.pack()

RCDesign_pwin.add(output_frm) 



RCDesign.mainloop()  # 마우스 및 키보드 이벤트를 기다리면서 응용프로그램의 기본 루프를 시작한다.