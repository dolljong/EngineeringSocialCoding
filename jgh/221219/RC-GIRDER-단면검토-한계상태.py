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

RCDesign.title('RC거더 단면검토-한계상태설계법')  # 창 우상단 제목
RCDesign.geometry('1300x800+100+15')  # 크기+x좌표+y좌표

RCDesign_pwin=ttk.Panedwindow(RCDesign, orient=tk.HORIZONTAL)  # 페인드 윈도우 생성, 윈도내 의젯은 수평배열(VERTICAL하면 수직배열)
## 페인드윈도, 프레임,위젯등은 원칙적으로 수직배열이 원칙인듯 orient=tk.HORIZONTAL 요게 수평배열로 만드는듯
RCDesign_pwin.pack(fill=tk.BOTH, expand=True)  # 양쪽채우기, 확장가능


#===============================================================================
input_frm = tk.LabelFrame(RCDesign_pwin, text='자료 입력',padx = 4, pady = 4, bd = 2, relief = tk.RIDGE,labelanchor=tk.NW)  # 페인드윈도1안에 라벨프레임 추가배치, 페인드윈도내에서는 위 orient=HOR..에 의해 수평 배치

input1_frm = tk.Frame(input_frm, padx = 4, pady = 4, bd = 2, relief = tk.RIDGE)  # 프레임안에 또 프레임 넣기 Layout정리 땜에
input1_frm.pack()

member_var = str()

def TitleWrite(event):
    global member_var
    member_var = member_ent.get()
    text="검토부재 : "+str(member_var)  # text는 단순 옮겨 적기용이므로 global 변수 지정은 필요 없다?
    input_box.insert(tk.END,text)
    text1="■검토부재 : "+str(member_var)  # text는 단순 옮겨 적기용이므로 global 변수 지정은 필요 없다?
    output_box.insert(tk.END,text1)
    
member_lbl = ttk.Label(input1_frm, text = "검토부재 : ") 
member_lbl.grid(column = 0, row = 0, pady = 3, sticky = tk.E)
member_ent = ttk.Entry(input1_frm,width=49, justify=tk.RIGHT)
member_ent.bind("<FocusOut>",TitleWrite)
member_ent.grid(column = 1, row = 0, padx = 3, pady = 3, sticky = tk.W)


pi_c = float()
pi_s = float()

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
    text="\nΦc : "+str(pi_c)+"\nΦs : "+str(pi_s)
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
fck_var = float()
ne = float()
eco = float()
ecu = float()
alpha = float()
beta = float()
nu = float()
beta1 = float()
Es_var = 200000

def FactorCalc(event):
    global fck_var
    global ne
    global eco 
    global ecu 
    global alpha 
    global beta 
    global nu 
    global beta1
    fck_var = eval(fck_ent.get())
    if fck_var <= 40:
        ne = 2.00
        eco = 0.0020
        ecu = 0.0033
        alpha = 0.80
        beta = 0.40
        nu = 1.0
        beta1 = 0.80
    elif fck_var <= 50:
        ne = 1.92
        eco = 0.0021
        ecu = 0.0032
        alpha = 0.78
        beta = 0.40
        nu = 0.97
        beta1 = 0.80
    elif fck_var <= 60:
        ne = 1.50
        eco = 0.0022
        ecu = 0.0031
        alpha = 0.72
        beta = 0.38
        nu = 0.95
        beta1 = 0.76
    elif fck_var <= 70:
        ne = 1.29
        eco = 0.0023
        ecu = 0.0030
        alpha = 0.67
        beta = 0.37
        nu = 0.91
        beta1 = 0.74
    elif fck_var <= 80:
        ne = 1.22
        eco = 0.0024
        ecu = 0.0029
        alpha = 0.63
        beta = 0.36
        nu = 0.87
        beta1 = 0.72
    elif fck_var <= 90:
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

fy_var = float()
fvy_var = float()
        
def Input1Write(event):
    global fy_var
    global fvy_var
    fy_var = eval(fy_ent.get())
    fvy_var = eval(fvy_ent.get())
    if pi_c == 0.65:
        text6="\n\n(1)극한한계상태\n\n1.재료특성 및 단면제원(극한하중조합)"
        output_box.insert(tk.END,text6)
    else:
        text6="\n\n(1)극단한계상태\n\n1.재료특성 및 단면제원(극단하중조합)"
        output_box.insert(tk.END,text6)
    text1="\nfck : "+ str(fck_var)+" MPa"
    input_box.insert(tk.END,text1)
    text2="\nfy  : "+ str(fy_var)+" MPa"
    input_box.insert(tk.END,text2)
    text3="\nfvy : "+ str(fvy_var)+" MPa"
    input_box.insert(tk.END,text3)
    text4="\n\n fck:"+ str(fck_var)+"MPa, fy:"+ str(fy_var)+"MPa, fvy:"+ str(fvy_var)+"MPa"
    output_box.insert(tk.END,text4)
    text5="\n\n ΦC:"+str(pi_c)+", ΦS:"+str(pi_s)+", α:"+ str(alpha)+", β:"+ str(beta)+", n:"+ str(ne)+", eco:"+ str(eco)+", ecu:"+ str(ecu)
    output_box.insert(tk.END,text5)

fck_lbl = ttk.Label(input2_frm, text = "fck : ") 
fck_lbl.grid(column = 1, row = 1, pady = 3, sticky = tk.E) 

fck_ent = ttk.Entry(input2_frm,width=10,justify=tk.RIGHT)
fck_ent.bind("<FocusOut>",FactorCalc)
fck_ent.grid(column = 2, row = 1, padx = 3, pady = 3, sticky = tk.W)

blank1_lbl = ttk.Label(input2_frm, text = "MPa,   ")
blank1_lbl.grid(column = 3, row = 1, pady = 3, sticky = tk.W) 

fy_lbl = ttk.Label(input2_frm, text = "fy : ") 
fy_lbl.grid(column = 4, row = 1, pady = 3, sticky = tk.E)

fy_ent = ttk.Entry(input2_frm,width=10,justify=tk.RIGHT) 
fy_ent.grid(column = 5, row = 1, padx = 3, pady = 3, sticky = tk.W)

blank2_lbl = ttk.Label(input2_frm, text = "MPa,   ") 
blank2_lbl.grid(column = 6, row = 1, pady = 3, sticky = tk.W)

fvy_lbl = ttk.Label(input2_frm, text = "fvy : ")
fvy_lbl.grid(column = 7, row = 1, pady = 3, sticky = tk.E)

fvy_ent = ttk.Entry(input2_frm,width=10, justify=tk.RIGHT)
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
width_var = float() 
height_var = float()
cover_var = float() 

def Input2Write(event):
    global width_var 
    global height_var
    global cover_var
    width_var = eval(width_ent.get()) 
    height_var = eval(height_ent.get()) 
    cover_var = eval(cover_ent.get()) 
    text1="\n폭   : "+ str(width_var)+" mm"
    input_box.insert(tk.END,text1)
    text2="\n높이 : "+ str(height_var)+" mm"
    input_box.insert(tk.END,text2)
    text3="\n피복 : "+ str(cover_var)+" mm"
    input_box.insert(tk.END,text3)
    text4="\n\n 폭:"+ str(width_var)+"mm,  높이:"+ str(height_var)+"mm,  피복:"+ str(cover_var)+"mm"
    output_box.insert(tk.END,text4)
    
width_lbl = ttk.Label(input2_frm, text = "폭 : ") 
width_lbl.grid(column = 1, row = 4, pady = 3, sticky = tk.E) 

width_ent = ttk.Entry(input2_frm,width=10,justify=tk.RIGHT)
width_ent.grid(column = 2, row = 4, padx = 3, pady = 3, sticky = tk.W)

blank4_lbl = ttk.Label(input2_frm, text = "mm,   ")
blank4_lbl.grid(column = 3, row = 4, pady = 3, sticky = tk.W) 

height_lbl = ttk.Label(input2_frm, text = "높이 : ") 
height_lbl.grid(column = 4, row = 4, pady = 3, sticky = tk.E) 


height_ent = ttk.Entry(input2_frm,width=10,justify=tk.RIGHT)
height_ent.grid(column = 5, row = 4, padx = 3, pady = 3, sticky = tk.W)

blank5_lbl = ttk.Label(input2_frm, text = "mm,   ")
blank5_lbl.grid(column = 6, row = 4, pady = 3, sticky = tk.W)

cover_lbl = ttk.Label(input2_frm, text = "피복 : ") 
cover_lbl.grid(column = 7, row = 4, pady = 3, sticky = tk.E) 

cover_ent = ttk.Entry(input2_frm,width=10,justify=tk.RIGHT)
cover_ent.bind("<FocusOut>",Input2Write)
cover_ent.grid(column = 8, row = 4, padx = 3, pady = 3, sticky = tk.W)

blank6_lbl = ttk.Label(input2_frm, text = "mm")
blank6_lbl.grid(column = 9, row = 4, pady = 3, sticky = tk.W) 

#--철근 입력 줄------------------------------------------------------------------------------
rebar_check_frm = tk.Frame(input_frm, padx = 4, pady = 4, bd = 2, relief = tk.RIDGE)
rebar_check_frm.pack()

bar_grade1 = ()
bar_grade2 = ()

def RebarGrade1(event):
    global bar_grade1
    if fy_var <= 300:
        bar_grade1 = "D"
    elif fy_var <= 400:
        bar_grade1 = "H"
    elif fy_var <= 500:
        bar_grade1 = "S"
    elif fy_var <= 600:
        bar_grade1 = "U"
    rebar_grade1_lbl.config(text=str(bar_grade1))
    rebar_grade2_lbl.config(text=str(bar_grade1))
    rebar_grade3_lbl.config(text=str(bar_grade1))
    
def RebarGrade2(event):
    global bar_grade2
    if fvy_var <= 300:
        bar_grade2 = "D"
    elif fvy_var <= 400:
        bar_grade2 = "H"
    elif fvy_var <= 500:
        bar_grade2 = "S"
    elif fvy_var <= 600:
        bar_grade2 = "U"
    rebar_grade4_lbl.config(text=str(bar_grade2))    

bar_Area={10:71.33,13:126.7,16:198.6,19:286.5,22:387.1,25:506.7,29:642.4,32:794.2,35:956.6}

Dia1_var = float()
As_Dia1_var = float()
As_ea1_var = float()
As1_var = float()

def RebarAs1(event):
    global Dia1_var
    global As_Dia1_var
    global As_ea1_var
    global As1_var
    Dia1_var = eval(Dia1_ent.get())
    As_Dia1_var = bar_Area[Dia1_var]
    As_ea1_var = eval(As_ea1_ent.get())
    As1_var = As_Dia1_var*As_ea1_var
    As_use1_lbl.config(text="USE As1 = "+str(round(As1_var,3))+"㎟")

As_use_lbl = ttk.Label(rebar_check_frm, text = "USE As : ") 
As_use_lbl.grid(column = 1, row = 1, pady = 3, sticky = tk.E)
rebar_grade1_lbl = ttk.Label(rebar_check_frm, text = "H") 
rebar_grade1_lbl.grid(column = 2, row = 1, pady = 3, sticky = tk.E) 
Dia1_ent = ttk.Entry(rebar_check_frm,width=5,justify=tk.RIGHT)
Dia1_ent.bind("<FocusOut>",RebarGrade1)
Dia1_ent.grid(column = 3, row = 1, padx = 3, pady = 3, sticky = tk.W)
blank10_lbl = ttk.Label(rebar_check_frm, text = " X ")
blank10_lbl.grid(column = 4, row = 1, pady = 3, sticky = tk.W) 
As_ea1_ent = ttk.Entry(rebar_check_frm,width=5,justify=tk.RIGHT)
As_ea1_ent.bind("<FocusOut>",RebarAs1)
As_ea1_ent.grid(column = 5, row = 1, padx = 3, pady = 3, sticky = tk.W)
blank11_lbl = ttk.Label(rebar_check_frm, text = "EA = ")
blank11_lbl.grid(column = 6, row = 1, pady = 3, sticky = tk.W) 
As_use1_lbl = ttk.Label(rebar_check_frm, text = "USE As") 
As_use1_lbl.grid(column = 7, row = 1, pady = 3, sticky = tk.W)


Dia2_var = float()
As_Dia2_var = float()
As_ea2_var = float()
As2_var = float()

def RebarAs2(event):
    global Dia2_var
    global As_Dia2_var
    global As_ea2_var
    global As2_var
    if eval(Dia2_ent.get()) == 0:
        As2_var = 0
        As_use2_lbl.config(text="USE As2 = "+str(round(As2_var,3))+"㎟")
    else:
        Dia2_var = eval(Dia2_ent.get())
        As_Dia2_var = bar_Area[Dia2_var]
        As_ea2_var = eval(As_ea2_ent.get())
        As2_var = As_Dia2_var*As_ea2_var
        As_use2_lbl.config(text="USE As2 = "+str(round(As2_var,3))+"㎟")
    
rebar_grade2_lbl = ttk.Label(rebar_check_frm, text = "H") 
rebar_grade2_lbl.grid(column = 2, row = 2, pady = 3, sticky = tk.E) 
Dia2_ent = ttk.Entry(rebar_check_frm,width=5,justify=tk.RIGHT)
Dia2_ent.grid(column = 3, row = 2, padx = 3, pady = 3, sticky = tk.W)
blank12_lbl = ttk.Label(rebar_check_frm, text = " X ")
blank12_lbl.grid(column = 4, row = 2, pady = 3, sticky = tk.W) 
As_ea2_ent = ttk.Entry(rebar_check_frm,width=5,justify=tk.RIGHT)
As_ea2_ent.bind("<FocusOut>",RebarAs2)
As_ea2_ent.grid(column = 5, row = 2, padx = 3, pady = 3, sticky = tk.W)
blank13_lbl = ttk.Label(rebar_check_frm, text = "EA = ")
blank13_lbl.grid(column = 6, row = 2, pady = 3, sticky = tk.W) 
As_use2_lbl = ttk.Label(rebar_check_frm, text = "USE As") 
As_use2_lbl.grid(column = 7, row = 2, pady = 3, sticky = tk.W)


Dia3_var = float()
As_Dia3_var = float()
As_ea3_var = float()
As3_var = float()
As_total = float()

def RebarAs3(event):
    global Dia3_var
    global As_Dia3_var
    global As_ea3_var
    global As3_var
    global As_total
    if eval(Dia3_ent.get()) == 0:
        As3_var = 0
        As_use3_lbl.config(text="USE As3 = "+str(round(As3_var,3))+"㎟")
        As_total=As1_var+As2_var+As3_var
        As_total_lbl.config(text="Total = "+str(round(As_total,3))+"㎟")
    else:
        Dia3_var = eval(Dia3_ent.get())
        As_Dia3_var = bar_Area[Dia3_var]
        As_ea3_var = eval(As_ea3_ent.get())
        As3_var = As_Dia3_var*As_ea3_var
        As_use3_lbl.config(text="USE As3 = "+str(round(As3_var,3))+"㎟")
        As_total=As1_var+As2_var+As3_var
        As_total_lbl.config(text="Total = "+str(round(As_total,3))+"㎟")
        
rebar_grade3_lbl = ttk.Label(rebar_check_frm, text = "H") 
rebar_grade3_lbl.grid(column = 2, row = 3, pady = 3, sticky = tk.E) 
Dia3_ent = ttk.Entry(rebar_check_frm,width=5,justify=tk.RIGHT)
Dia3_ent.grid(column = 3, row = 3, padx = 3, pady = 3, sticky = tk.W)
blank14_lbl = ttk.Label(rebar_check_frm, text = " X ")
blank14_lbl.grid(column = 4, row = 3, pady = 3, sticky = tk.W) 
As_ea3_ent = ttk.Entry(rebar_check_frm,width=5,justify=tk.RIGHT)
As_ea3_ent.bind("<FocusOut>",RebarAs3)
As_ea3_ent.grid(column = 5, row = 3, padx = 3, pady = 3, sticky = tk.W)
blank15_lbl = ttk.Label(rebar_check_frm, text = "EA = ")
blank15_lbl.grid(column = 6, row = 3, pady = 3, sticky = tk.W) 
As_use3_lbl = ttk.Label(rebar_check_frm, text = "USE As") 
As_use3_lbl.grid(column = 7, row = 3, pady = 3, sticky = tk.W)

As_total_lbl = ttk.Label(rebar_check_frm, text = " USE Total As") 
As_total_lbl.grid(column = 8, row = 3, pady = 3, sticky = tk.E)


Dia4_var = float()
Av_Dia_var = float()
Av_ea_var = float()
Av_var = float()
Av_ctc_var = float()

def RebarAv(event):
    global Dia4_var
    global Av_Dia_var
    global Av_ea_var
    global Av_var
    global Av_ctc_var
    if eval(Dia4_ent.get()) == 0:
        Av_var = 0
        Av_use1_lbl.config(text="USE Av = "+str(round(Av_var,3))+"㎟")
    else:
        Dia4_var = eval(Dia4_ent.get())
        Av_Dia_var = bar_Area[Dia4_var]
        Av_ea_var = eval(Av_ea_ent.get())
        Av_var = Av_Dia_var*Av_ea_var
        Av_use1_lbl.config(text="USE Av = "+str(round(Av_var,3))+"㎟")
        Av_ctc_var = eval(Av_ctc_ent.get())

Av_use_lbl = ttk.Label(rebar_check_frm, text = "USE Av : ") 
Av_use_lbl.grid(column = 1, row = 4, pady = 3, sticky = tk.E)
rebar_grade4_lbl = ttk.Label(rebar_check_frm, text = "H") 
rebar_grade4_lbl.grid(column = 2, row = 4, pady = 3, sticky = tk.E) 
Dia4_ent = ttk.Entry(rebar_check_frm,width=5,justify=tk.RIGHT)
Dia4_ent.bind("<FocusOut>",RebarGrade2)
Dia4_ent.grid(column = 3, row = 4, padx = 3, pady = 3, sticky = tk.W)
blank16_lbl = ttk.Label(rebar_check_frm, text = " X ")
blank16_lbl.grid(column = 4, row = 4, pady = 3, sticky = tk.W) 
Av_ea_ent = ttk.Entry(rebar_check_frm,width=5,justify=tk.RIGHT)
Av_ea_ent.grid(column = 5, row = 4, padx = 3, pady = 3, sticky = tk.W)
blank17_lbl = ttk.Label(rebar_check_frm, text = "EA/m = ")
blank17_lbl.grid(column = 6, row = 4, pady = 3, sticky = tk.W) 
Av_use1_lbl = ttk.Label(rebar_check_frm, text = "USE Av") 
Av_use1_lbl.grid(column = 7, row = 4, pady = 3, sticky = tk.W)

blank18_lbl = ttk.Label(rebar_check_frm, text = "간격") 
blank18_lbl.grid(column = 3, row = 5, pady = 3, sticky = tk.E)
blank19_lbl = ttk.Label(rebar_check_frm, text = ":")
blank19_lbl.grid(column = 4, row = 5, pady = 3)
Av_ctc_ent = ttk.Entry(rebar_check_frm,width=5,justify=tk.RIGHT)
Av_ctc_ent.bind("<FocusOut>",RebarAv)
Av_ctc_ent.grid(column = 5, row = 5, padx = 3, pady = 3, sticky = tk.E)
blank20_lbl = ttk.Label(rebar_check_frm, text = "mm") 
blank20_lbl.grid(column = 6, row = 5, pady = 3, sticky = tk.W)

blank100_lbl = ttk.Label(input_frm, text = "※ 철근이 (2, 3단에)배치되지 않을 경우, 반드시 0 을 입력해야 함.(blank로 두면 안됨)")
blank100_lbl.pack()

#--외력 입력줄------------------------------------------------------------------------
force_input_frm = tk.Frame(input_frm, padx = 4, pady = 4, bd = 2, relief = tk.RIDGE)
force_input_frm.pack()

Mu_var = float()
Vu_var = float()
depth_var = float()
M0_var = float()
design_grade = str()
a_eq = float()
b_eq = float()
As_req = float()

def Input3Write(event):
    global Mu_var
    global Vu_var
    global depth_var
    global M0_var
    global design_grade
    global a_eq
    global b_eq
    global As_req
    Mu_var = eval(Mu_ent.get()) 
    Vu_var = eval(Vu_ent.get())
    M0_var = eval(M0_ent.get())
    design_grade = grade_ent.get()
    if As2_var == 0:
        depth_var = height_var-cover_var
    elif As3_var == 0:
        depth_var = height_var-(As1_var*cover_var+As2_var*(cover_var+100))/As_total
    else:
        depth_var = height_var-(As1_var*cover_var+As2_var*(cover_var+100)+As3_var*(cover_var+200))/As_total
    depth_ent.delete(0,99)
    depth_ent.insert(0,round(depth_var,3))
    text1="\nMu   : "+ str(Mu_var)+" kN.m"
    input_box.insert(tk.END,text1)
    text2="\nVu  : "+ str(Vu_var)+" kN"
    input_box.insert(tk.END,text2)
    text23="\nMo  : "+ str(M0_var)+" kN.m"
    input_box.insert(tk.END,text23)
    text24="\n최소설계등급  : "+ str(design_grade)
    input_box.insert(tk.END,text24)
    text3="\nd  : "+ str(round(depth_var,3))+" mm"
    input_box.insert(tk.END,text3)
    text4="\n\n Mu:"+ str(Mu_var)+"kN.m,  Vu:"+ str(Vu_var)+"kN,  d:"+ str(round(depth_var,3))+"mm"
    output_box.insert(tk.END,text4)
    text5="\n\n2.필요철근량 검토\n\n Md = As x ΦS x fy x (d - β x c) ------------------------ ① \n c = As x ΦS x fy / (α x ΦC x 0.85 x fck x b) ---------- ② \n\n ①식과 ②식을 연립하여 필요 철근량을 구한다." 
    output_box.insert(tk.END,text5)
    a_eq = beta*pi_s**2*fy_var**2/(alpha*pi_c*0.85*fck_var*width_var)
    b_eq = pi_s*fy_var*depth_var
    As_req = (b_eq-sqrt(b_eq**2-4*a_eq*Mu_var*1000000))/(2*a_eq)
    text6="\n\n As_req = "+str(round(As_req,3))+"㎟"
    reqAs2_lbl.config(text="As_req = "+str(round(As_req,3))+"㎟")
    output_box.insert(tk.END,text6)
    text10="\n1단주철근직경   : "+ str(Dia1_var)
    input_box.insert(tk.END,text10)
    text11="\n1단주철근갯수   : "+ str(As_ea1_var)
    input_box.insert(tk.END,text11)
    text12="\n2단주철근직경   : "+ str(Dia2_var)
    input_box.insert(tk.END,text12)
    text13="\n2단주철근갯수   : "+ str(As_ea2_var)
    input_box.insert(tk.END,text13)
    text14="\n3단주철근직경   : "+ str(Dia3_var)
    input_box.insert(tk.END,text14)
    text15="\n3단주철근갯수   : "+ str(As_ea3_var)
    input_box.insert(tk.END,text15)
    text16="\n전단철근직경   : "+ str(Dia4_var)
    input_box.insert(tk.END,text16)
    text17="\n전단철근다리수   : "+ str(Av_ea_var)
    input_box.insert(tk.END,text17)
    text18="\n전단철근간격   : "+ str(Av_ctc_var)
    input_box.insert(tk.END,text18)
    text19="\n\n  사용철근 1단 : "+str(bar_grade1)+" "+ str(Dia1_var)+" x "+str(As_ea1_var)+"ea = "+str(round(As1_var,3))+"㎟"
    output_box.insert(tk.END,text19)
    text20="\n             2단 : "+str(bar_grade1)+" "+ str(Dia2_var)+" x "+str(As_ea2_var)+"ea = "+str(round(As2_var,3))+"㎟"
    output_box.insert(tk.END,text20)
    text21="\n             3단 : "+str(bar_grade1)+" "+ str(Dia3_var)+" x "+str(As_ea3_var)+"ea = "+str(round(As3_var,3))+"㎟,   As_total = "+str(round(As_total,3))+"㎟"
    output_box.insert(tk.END,text21)
    text22="\n\n  사용전단철근 : "+str(bar_grade2)+" "+ str(Dia4_var)+" x "+str(Av_ea_var)+"ea/m,   간격 : "+str(Av_ctc_var)+"mm \n\n"
    output_box.insert(tk.END,text22)

Mu_lbl = ttk.Label(force_input_frm, text = "Mu : ") 
Mu_lbl.grid(column = 1, row = 1, pady = 3, sticky = tk.E) 
Mu_ent = ttk.Entry(force_input_frm,width=10,justify=tk.RIGHT)
Mu_ent.grid(column = 2, row = 1, padx = 3, pady = 3, sticky = tk.W)

blank7_lbl = ttk.Label(force_input_frm, text = "kN.m,   ")
blank7_lbl.grid(column = 3, row = 1, pady = 3, sticky = tk.W) 

Vu_lbl = ttk.Label(force_input_frm, text = "Vu : ") 
Vu_lbl.grid(column = 4, row = 1, pady = 3, sticky = tk.E) 
Vu_ent = ttk.Entry(force_input_frm,width=10,justify=tk.RIGHT)
Vu_ent.grid(column = 5, row = 1, padx = 3, pady = 3, sticky = tk.W)

blank8_lbl = ttk.Label(force_input_frm, text = "kN,   ")
blank8_lbl.grid(column = 6, row = 1, pady = 3, sticky = tk.W)

M0_lbl = ttk.Label(force_input_frm, text = "Mo : ") 
M0_lbl.grid(column = 1, row = 2, pady = 3, sticky = tk.E) 
M0_ent = ttk.Entry(force_input_frm,width=10,justify=tk.RIGHT)
M0_ent.grid(column = 2, row = 2, padx = 3, pady = 3, sticky = tk.W)

blank10_lbl = ttk.Label(force_input_frm, text = "kN.m,   ")
blank10_lbl.grid(column = 3, row = 2, pady = 3, sticky = tk.W) 

design_grade
grade_lbl = ttk.Label(force_input_frm, text = "설계등급 : ") 
grade_lbl.grid(column = 4, row = 2, pady = 3, sticky = tk.E) 
grade_ent = ttk.Entry(force_input_frm,width=10,justify=tk.RIGHT)
grade_ent.bind("<FocusOut>",Input3Write)
grade_ent.grid(column = 5, row = 2, padx = 3, pady = 3, sticky = tk.W)

depth_lbl = ttk.Label(force_input_frm, text = "d : ") 
depth_lbl.grid(column = 7, row = 2, pady = 3, sticky = tk.E) 
depth_ent = ttk.Entry(force_input_frm,width=10,justify=tk.RIGHT)
depth_ent.grid(column = 8, row = 2, padx = 3, pady = 3, sticky = tk.W)

blank9_lbl = ttk.Label(force_input_frm, text = "mm")
blank9_lbl.grid(column = 9, row = 2, pady = 3, sticky = tk.W) 

blank81_lbl = ttk.Label(force_input_frm, text = "Mo는")
blank81_lbl.grid(column = 1, row = 3, pady = 3, sticky = tk.E)

blank82_lbl = ttk.Label(force_input_frm, text = " 사용조합1")
blank82_lbl.grid(column = 2, row = 3, pady = 3, sticky = tk.W)

#--결과 줄------------------------------------------------------------------------------
ouput_check_frm = tk.Frame(input_frm, padx = 4, pady = 4)#, bd = 2, relief = tk.RIDGE)
ouput_check_frm.pack()

reqAs1_lbl = ttk.Label(ouput_check_frm, text = "Md = As x ΦS x fy x (d - β x c) ------------------------ ① \nc = As x ΦS x fy / (α x ΦC x 0.85 x fck x b) ---------- ② \n①식과 ②식을 연립하여 필요 철근량을 구한다.") 
reqAs1_lbl.grid(column = 1, row = 1, pady = 3, sticky = tk.E)

reqAs2_lbl = ttk.Label(ouput_check_frm, text = "As_req = ") 
reqAs2_lbl.grid(column = 1, row = 2, pady = 3, sticky = tk.W)


#--버튼줄------------------------------------------------------------------------------
input_btn_frm = tk.Frame(input_frm, padx = 4, pady = 4)
input_btn_frm.pack()

def InputReadFile(event):  # 열기 클릭시 호출되는 함수 정의
    global member_var
    global pi_c
    global pi_s
    global fck_var
    global fy_var
    global fvy_var
    global ne
    global eco 
    global ecu 
    global alpha 
    global beta 
    global width_var
    global height_var
    global cover_var
    global Dia1_var
    global As_ea1_var
    global Dia2_var
    global As_ea2_var
    global Dia3_var
    global As_ea3_var
    global depth_total
    global Dia4_var
    global Av_ea_var
    global Av_ctc_var
    global Mu_var
    global Vu_var
    global depth_var
    global M0_var
    global design_grade
    file=askopenfilename(title="파일열기",filetypes=(("텍스트파일","*.txt"),("모든파일","*.*")))
    # Main.title(os.path.basename(file)+"-메모장")
    input_box.delete(1.0,tk.END)
    f=open(file,"r")
    # read()는 파일내용을 모두 문자열로 리턴해준다.
    # 문자셋은 서로 일치 시켜야 열수 있다. 윈도우 메모장에서 ANSI로 저장하면 확인 가능
    # UTF-8로 저장되면 지금 현재 연습에선 열 수 없다.
    input_box.insert(1.0,f.read()) # 왜 이라인과 아래라인은 공존 하지 못할까?
    f=open(file,"r") # f.read()이 파일을 사용한 관계로 다시 열어서 f.readlines()를 구동시킬수 있도록 함
    line=f.readlines()
    f.close()
    sentence=[]
    for input_data in line:
        split_data=input_data.split()
        sentence.append(split_data)
    transe_data=sentence
    member_var=transe_data[0][2]
    member_ent.delete(0,99)
    member_ent.insert(0,member_var)
    pi_c=transe_data[1][2]
    pi_s=transe_data[2][2]
    fck_var=transe_data[3][2]
    fck_ent.delete(0,99)
    fck_ent.insert(0,fck_var)
    fy_var=transe_data[4][2]
    fy_ent.delete(0,99)
    fy_ent.insert(0,fy_var)
    fvy_var=transe_data[5][2]
    fvy_ent.delete(0,99)
    fvy_ent.insert(0,fvy_var)
    width_var=transe_data[6][2]
    width_ent.delete(0,99)
    width_ent.insert(0,width_var)
    height_var=transe_data[7][2]
    height_ent.delete(0,99)
    height_ent.insert(0,height_var)
    cover_var=transe_data[8][2]
    cover_ent.delete(0,99)
    cover_ent.insert(0,cover_var)
    Dia1_var=transe_data[14][2]
    Dia1_ent.delete(0,99)
    Dia1_ent.insert(0,Dia1_var)
    As_ea1_var=transe_data[15][2]
    As_ea1_ent.delete(0,99)
    As_ea1_ent.insert(0,As_ea1_var)
    Dia2_var=transe_data[16][2]
    Dia2_ent.delete(0,99)
    Dia2_ent.insert(0,Dia2_var)
    As_ea2_var=transe_data[17][2]
    As_ea2_ent.delete(0,99)
    As_ea2_ent.insert(0,As_ea2_var)
    Dia3_var=transe_data[18][2]
    Dia3_ent.delete(0,99)
    Dia3_ent.insert(0,Dia3_var)
    As_ea3_var=transe_data[19][2]
    As_ea3_ent.delete(0,99)
    As_ea3_ent.insert(0,As_ea3_var)
    Dia4_var=transe_data[20][2]
    Dia4_ent.delete(0,99)
    Dia4_ent.insert(0,Dia4_var)
    Av_ea_var=transe_data[21][2]
    Av_ea_ent.delete(0,99)
    Av_ea_ent.insert(0,Av_ea_var)
    Av_ctc_var=transe_data[22][2]
    Av_ctc_ent.delete(0,99)
    Av_ctc_ent.insert(0,Av_ctc_var)
    Mu_var=transe_data[9][2]
    Mu_ent.delete(0,99)
    Mu_ent.insert(0,Mu_var)
    Vu_var=transe_data[10][2]
    Vu_ent.delete(0,99)
    Vu_ent.insert(0,Vu_var)
    M0_var=transe_data[11][2]
    M0_ent.delete(0,99)
    M0_ent.insert(0,M0_var)
    design_grade=transe_data[12][2]
    grade_ent.delete(0,99)
    grade_ent.insert(0,design_grade)
    depth_var=transe_data[13][2]
    depth_ent.delete(0,99)
    depth_ent.insert(0,M0_var)
    
input_read_btn = ttk.Button(input_btn_frm, text = "입력파일 열기")
input_read_btn.bind("<Return>",InputReadFile)
input_read_btn.bind("<Button-1>",InputReadFile)
input_read_btn.pack(side = tk.LEFT)


def InputArrangedFile(event):  # 열기 클릭시 호출되는 함수 정의
    input_box.delete(1.0,tk.END)
    TitleWrite(event)
    check()
    FactorCalc(event)
    Input1Write(event)
    Input2Write(event)
    RebarGrade1(event)
    RebarGrade2(event)
    RebarAs1(event)
    RebarAs2(event)
    RebarAs3(event)
    RebarAv(event)
    Input3Write(event)
    
input_arrange_btn = ttk.Button(input_btn_frm, text = "입력파일 정리 및 중간계산")
input_arrange_btn.bind("<Return>",InputArrangedFile)
input_arrange_btn.bind("<Button-1>",InputArrangedFile)
input_arrange_btn.pack(side = tk.LEFT)


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
scrol_h  = 8  # 스크롤텍스트박스의 높이
input_box = scrolledtext.ScrolledText(input_frm, width = scrol_w, height = scrol_h, wrap = tk.WORD)
input_box.pack()

RCDesign_pwin.add(input_frm)

#===============================================================================
output_frm = tk.LabelFrame(RCDesign_pwin, text='결과 출력',padx = 4, pady = 4, bd = 2, relief = tk.RIDGE,labelanchor=tk.NW)  # 페인드윈도1안에 프레임배치

check_btn_frm = tk.Frame(output_frm, padx = 4, pady = 4)
check_btn_frm.pack()

#-------------------------------------------------------------------------------
def RebarChange():
    global width_var
    global height_var
    global cover_var
    global Dia1_var
    global As_Dia1_var
    global As_ea1_var
    global As1_var
    global Dia2_var
    global As_Dia2_var
    global As_ea2_var
    global As2_var
    global Dia3_var
    global As_Dia3_var
    global As_ea3_var
    global As3_var
    global As_total
    global depth_total
    global Av_Dia_var
    global Av_ea_var
    global Av_var
    global Av_ctc_var
    width_var = eval(width_ent.get()) 
    height_var = eval(height_ent.get()) 
    cover_var = eval(cover_ent.get()) 
    Dia1_var = eval(Dia1_ent.get())
    As_Dia1_var = bar_Area[Dia1_var]
    As_ea1_var = eval(As_ea1_ent.get())
    As1_var = As_Dia1_var*As_ea1_var
    if eval(Dia2_ent.get()) == 0:
        As2_var = 0
    else:
        Dia2_var = eval(Dia2_ent.get())
        As_Dia2_var = bar_Area[Dia2_var]
        As_ea2_var = eval(As_ea2_ent.get())
        As2_var = As_Dia2_var*As_ea2_var
    if eval(Dia3_ent.get()) == 0:
        As3_var = 0
        As_total=As1_var+As2_var+As3_var
    else:
        Dia3_var = eval(Dia3_ent.get())
        As_Dia3_var = bar_Area[Dia3_var]
        As_ea3_var = eval(As_ea3_ent.get())
        As3_var = As_Dia3_var*As_ea3_var
        As_total=As1_var+As2_var+As3_var
    if As2_var == 0:
        depth_var = height_var-cover_var
    elif As3_var == 0:
        depth_var = height_var-(As1_var*cover_var+As2_var*(cover_var+100))/As_total
    else:
        depth_var = height_var-(As1_var*cover_var+As2_var*(cover_var+100)+As3_var*(cover_var+200))/As_total
    if eval(Dia4_ent.get()) == 0:
        Av_var = 0
    else:
        Dia4_var = eval(Dia4_ent.get())
        Av_Dia_var = bar_Area[Dia4_var]
        Av_ea_var = eval(Av_ea_ent.get())
        Av_var = Av_Dia_var*Av_ea_var
        Av_ctc_var = eval(Av_ctc_ent.get())

As_min1 = float()
As_min2 = float()
As_min3 = float()
As_min = float()

def CheckAsMin(event):
    global As_min1
    global As_min2
    global As_min3
    global As_min
    check_box.delete(1.0,tk.END)
    RebarChange()
    As_min1 = 0.25*sqrt(fck_var)/fy_var*width_var*depth_var
    text1="\n3.최소철근량 검토\n\n As_min1 = ( 0.25 x √(fck) / fy ) x b x d"
    check_box.insert(tk.END,text1)
    output_box.insert(tk.END,text1)
    text2="\n           = ( 0.25 x √("+str(fck_var)+") / "+str(fy_var)+") x "+str(width_var)+" x "+str(round(depth_var,3))+" = "+str(round(As_min1,3))+"㎟"
    check_box.insert(tk.END,text2)
    output_box.insert(tk.END,text2)
    As_min2 = 1.4/fy_var*width_var*depth_var
    text3="\n As_min2 = ( 1.4 / fy ) x b x d"
    check_box.insert(tk.END,text3)
    output_box.insert(tk.END,text3)
    text4="\n           = ( 1.4 / "+str(fy_var)+") x "+str(width_var)+" x "+str(round(depth_var,3))+" = "+str(round(As_min2,3))+"㎟"
    check_box.insert(tk.END,text4)
    output_box.insert(tk.END,text4)
    As_min3 = 4/3*As_req
    text5="\n As_min3 = 4/3 x As_req = "+str(round(As_min3,3))+"㎟"
    check_box.insert(tk.END,text5)
    output_box.insert(tk.END,text5)
#    As_min4 = 1.2*As_req
#    text6="As_min4 = 1.2 x As_req = "+str(As_min4)
#    check_box.insert(tk.END,text6)
    As_min = min(max(As_min1,As_min2), As_min3)
    if As_total > As_min:
        text7="\n\n As_use > As_min = "+str(round(As_total,3))+"㎟  >  "+str(round(As_min,3))+"㎟  --> OK!"
        check_box.insert(tk.END,text7)
        output_box.insert(tk.END,text7)
    else:
        text7="\n\n As_use < As_min = "+str(round(As_total,3))+"㎟  <  "+str(round(As_min,3))+"㎟  --> NG!!!!!!"
        check_box.insert(tk.END,text7)
        output_box.insert(tk.END,text7)
check_Asmin_btn = ttk.Button(check_btn_frm, text = "3.최소철근량 검토")
check_Asmin_btn.bind("<Return>",CheckAsMin)
check_Asmin_btn.bind("<Button-1>",CheckAsMin)
check_Asmin_btn.pack(side = tk.LEFT)

#-------------------------------------------------------------------------------
As_max = float()

def CheckAsMax(event):
    global As_max
    check_box.delete(1.0,tk.END)
    RebarChange()
    As_max = 0.04*width_var*depth_var
    text1="\n\n4.최대철근량 검토\n\n As_max = 0.04 x b x d"
    check_box.insert(tk.END,text1)
    output_box.insert(tk.END,text1)
    text2="\n         = 0.004 x "+str(width_var)+" x "+str(round(depth_var,3))+" = "+str(round(As_max,3))+"㎟"
    check_box.insert(tk.END,text2)
    output_box.insert(tk.END,text2)
    if As_max > As_total:
        text3="\n As_max > As_use = "+str(round(As_max,3))+"㎟  >  "+str(round(As_total,3))+"㎟ --> OK!"
        check_box.insert(tk.END,text3)
        output_box.insert(tk.END,text3)
    else:
        text3="\n As_max < As_use = "+str(round(As_max,3))+"㎟  <  "+str(round(As_total,3))+"㎟ --> NG!!!!!!"
        check_box.insert(tk.END,text3)
        output_box.insert(tk.END,text3)
check_Asmax_btn = ttk.Button(check_btn_frm, text = "4.최대철근량 검토")
check_Asmax_btn.bind("<Return>",CheckAsMax)
check_Asmax_btn.bind("<Button-1>",CheckAsMax)
check_Asmax_btn.pack(side = tk.LEFT)

#-------------------------------------------------------------------------------
C_max = float()
C_var = float()

def CheckCMax(event):
    global C_max
    global C_var
    check_box.delete(1.0,tk.END)
    RebarChange()
    C_max = (1.0*ecu/0.0033-0.6)*depth_var
    text1="\n\n5.중립축 깊이 검토\n\n C_max = (δ x εcu / 0.0033-0.6) x d"
    check_box.insert(tk.END,text1)
    output_box.insert(tk.END,text1)
    text2="\n         = (1.0 x "+str(ecu)+" / 0.003 - 0.6) x "+str(round(depth_var,3))+" = "+str(round(C_max,3))+" mm"
    check_box.insert(tk.END,text2)
    output_box.insert(tk.END,text2)
    C_var = As_total*pi_s*fy_var/(alpha*pi_c*0.85*fck_var*width_var)
    text3="\n\n C = (As x Φs x fy)/(α x Φc x 0.85 x fck x b)"
    check_box.insert(tk.END,text3)
    output_box.insert(tk.END,text3)
    text4="\n   = ("+str(round(As_total,3))+" x "+str(pi_s)+" x "+str(fy_var)+") / ("+str(alpha)+" x "+str(pi_c)+" x 0.85 x "+str(fck_var)+" x "+str(width_var)+") = "+str(round(C_var,3))+" mm"
    check_box.insert(tk.END,text4)
    output_box.insert(tk.END,text4)
    if C_max > C_var:
        text5="\n\n 최대중립축 깊이 > 중립축의 깊이 = "+str(round(C_max,3))+"mm  >  "+str(round(C_var,3))+"mm --> OK!"
        check_box.insert(tk.END,text5)
        output_box.insert(tk.END,text5)
    else:
        text5="\n\n 최대중립축 깊이 < 중립축의 깊이 = "+str(round(C_max,3))+"mm  >  "+str(round(C_var,3))+"mm --> NG!!!!!!"
        check_box.insert(tk.END,text5)
        output_box.insert(tk.END,text5)
check_Cmax_btn = ttk.Button(check_btn_frm, text = "5.최대중립축 검토")
check_Cmax_btn.bind("<Return>",CheckCMax)
check_Cmax_btn.bind("<Button-1>",CheckCMax)
check_Cmax_btn.pack(side = tk.LEFT)

#-------------------------------------------------------------------------------
e_s = float()
e_yd = float()
Es_var = 200000

def CheckBarStrain(event):
    global e_s
    global e_yd
    global Es_var
    check_box.delete(1.0,tk.END)
    RebarChange()
    e_s = (depth_var-C_var)/C_var*ecu
    text1="\n\n6.인장철근 변형률 검토\n\n εs = (d-c)/c x εcu"
    check_box.insert(tk.END,text1)
    output_box.insert(tk.END,text1)
    text2="\n    = ("+str(depth_var)+" - "+str(round(C_var,3))+") / "+str(round(C_var,3))+" x "+str(ecu)+" = "+str(round(e_s,3))
    check_box.insert(tk.END,text2)
    output_box.insert(tk.END,text2)
    text3="\n\n εyd = (Φs x fy)/Es"
    check_box.insert(tk.END,text3)
    output_box.insert(tk.END,text3)
    e_yd = pi_s*fy_var/Es_var
    text4="\n     = ("+str(pi_s)+" x "+str(fy_var)+") / "+str(Es_var)+" = "+str(round(e_yd,3))
    check_box.insert(tk.END,text4)
    output_box.insert(tk.END,text4)
    if e_s > e_yd:
        text5="\n\n εs = "+str(round(e_s,3))+"  >   εyd = "+str(round(e_yd,3))+" ----> OK!"
        check_box.insert(tk.END,text5)
        output_box.insert(tk.END,text5)
    else:
        text5="\n\n εs = "+str(round(e_s,3))+"  <   εyd = "+str(round(e_yd,3))+" ----> NG!!!!!!"
        check_box.insert(tk.END,text5)
        output_box.insert(tk.END,text5)
check_BarStrain_btn = ttk.Button(check_btn_frm, text = "6.철근변형률 검토")
check_BarStrain_btn.bind("<Return>",CheckBarStrain)
check_BarStrain_btn.bind("<Button-1>",CheckBarStrain)
check_BarStrain_btn.pack(side = tk.LEFT)

#-------------------------------------------------------------------------------
Md_var = float()

def CheckBending(event):
    global Md_var
    check_box.delete(1.0,tk.END)
    RebarChange()
    Md_var = As_total*pi_s*fy_var*(depth_var-beta*C_var)
    text1="\n\n7.휨에 대한 검토\n\n Md = As x Φs x fy x (d-β*c)"
    check_box.insert(tk.END,text1)
    output_box.insert(tk.END,text1)
    text2="\n    = ("+str(round(As_total,3))+" x "+str(pi_s)+" x "+str(fy_var)+" x ("+str(round(depth_var,3))+"-"+str(beta)+"x"+str(round(C_var,3))+")"
    check_box.insert(tk.END,text2)
    output_box.insert(tk.END,text2)
    text3="\n    = "+str(round(Md_var,3))+" N·mm  = "+str(round(Md_var/1000000,3))+" kN·m"
    check_box.insert(tk.END,text3)
    output_box.insert(tk.END,text3)
    if Md_var > (Mu_var*1000000):
        text4="\n\n Md = "+str(round(Md_var/1000000,3))+" kN·m   >   Mu = "+str(Mu_var)+" kN·m  (S.F "+str(round(Md_var/(Mu_var*1000000),3))+") ----> OK!"
        check_box.insert(tk.END,text4)
        output_box.insert(tk.END,text4)
    else:
        text4="\n\n Md = "+str(round(Md_var/1000000,3))+" kN·m   <   Mu = "+str(Mu_var)+" kN·m  (S.F "+str(round(Md_var/(Mu_var*1000000),3))+") ----> NG!!!!!!"
        check_box.insert(tk.END,text4)
        output_box.insert(tk.END,text4)
check_bending_btn = ttk.Button(check_btn_frm, text = "7.모멘트 검토")
check_bending_btn.bind("<Return>",CheckBending)
check_bending_btn.bind("<Button-1>",CheckBending)
check_bending_btn.pack(side = tk.LEFT)

#-------------------------------------------------------------------------------
k_var = float()
low_var = float()
fn_var = float()
Vcd_var = float()
fctk_var = float()
fcm_var = float()
Vcdmin_var = float()
s1max_var = float()
s2max_var = float()
low_v_var = float()
low_vmin_var = float()
Vsd_var = float()
nu_var=float()  # 콘크리트 압축강도 유효계수
Vdmax_var = float()

def CheckShear(event):
    global k_var
    global low_var
    global fn_var
    global Vcd_var
    global fctk_var
    global fcm_var
    global Vcdmin_var
    global s1max_var
    global s2max_var
    global low_v_var
    global low_vmin_var
    global Vsd_var
    global nu_var
    global Vdmax_var
    check_box.delete(1.0,tk.END)
    RebarChange()
    text1 = "\n\n8.전단에 대한 검토\n\n ① 전단철근이 없는 설계전단강도"
    check_box.insert(tk.END,text1)
    output_box.insert(tk.END,text1)
    k_var = 1+sqrt(200/depth_var)
    if k_var < 2.0:
        text2="\n\n k = 1+√(200 / d) = 1.0 + √(200/"+str(round(depth_var,3))+") = "+str(round(k_var,3))+" < 2.0 -----> OK!"
        check_box.insert(tk.END,text2)
        output_box.insert(tk.END,text2)
    else:
        text2="\n\m k = 1+√(200 / d) = 1.0 + √(200/"+str(depth_var)+") = "+str(round(k_var,3))+" > 2.0 -----> NG!!!!"
        check_box.insert(tk.END,text2)
        output_box.insert(tk.END,text2)
    low_var = As_total/(width_var*depth_var)
    if low_var < 0.02:
        text3="\n\n ρ = As / (b x d) = "+str(round(As_total,3))+" / ("+str(width_var)+"x"+str(round(depth_var,3))+") = "+str(round(low_var,3))+" < 0.020 -----> OK!"
        check_box.insert(tk.END,text3)
        output_box.insert(tk.END,text3)
    else:
        text3="\n\n ρ = As / (b x d) = "+str(round(As_total,3))+" / ("+str(width_var)+"x"+str(round(depth_var,3))+") = "+str(round(low_var,3))+" > 0.020 -----> NG!!!!"
        check_box.insert(tk.END,text3)
        output_box.insert(tk.END,text3)
    fn = 0  # 순수휨으로 가정
    text4 = "\n\n fn = Nu/Ac = 0.000  <  "+str(round(0.2*pi_c*fck_var,3))+" = 0.2 x Φc x fck  -----> OK!"
    check_box.insert(tk.END,text4)
    output_box.insert(tk.END,text4)
    Vcd_var = (0.85*pi_c*k_var*(low_var*fck_var)**(1/3)+0.15*fn)*width_var*depth_var
    text5 = "\n\n Vcd = [0.85 x Φc x k x (p x fck)^⅓ + 0.15 x fn] x b x d"
    check_box.insert(tk.END,text5)
    output_box.insert(tk.END,text5)
    text6 = "\n      = [0.85 x "+str(pi_c)+" x "+str(round(k_var,3))+" x ("+str(round(low_var,3))+" x "+str(fck_var)+")^⅓ + 0.15 x "+str(round(fn_var,3))+"] x "+str(width_var)+" x "+str(round(depth_var,3))
    check_box.insert(tk.END,text6)
    output_box.insert(tk.END,text6)
    text7 = "\n      = "+str(round(Vcd_var,3))+"N = "+str(round(Vcd_var/1000,3))+"kN"
    check_box.insert(tk.END,text7)
    output_box.insert(tk.END,text7)
    if fck_var <= 40:
        fcm_var = fck_var+4
    elif fck_var >= 60:
        fcm_var = fck_var+6
    else:
        fcm_var = fck_var+((fck_var-40)/10+4)
    fctk_var = 0.3*fcm_var**(2/3)*0.7
    Vcdmin_var = (0.4*pi_c*fctk_var+0.15*fn_var)*width_var*depth_var
    text8 = "\n\n Vcd_min = [0.4 x Φc x fctk + 0.15 x fn] x b x d"
    check_box.insert(tk.END,text8)
    output_box.insert(tk.END,text8)
    text9 = "\n          = [0.4 x "+str(pi_c)+" x "+str(round(fctk_var,3))+" + 0.15 x "+str(round(fn_var,3))+"] x "+str(width_var)+" x "+str(round(depth_var,3))
    check_box.insert(tk.END,text9)
    output_box.insert(tk.END,text9)
    text10 = "\n          = "+str(round(Vcdmin_var,3))+"N  =  "+str(round(Vcdmin_var/1000,3))+"kN"
    check_box.insert(tk.END,text10)
    output_box.insert(tk.END,text10)
    if max(Vcd_var/1000,Vcdmin_var/1000) > Vu_var:
        text11 = "\n\n  Vcd = "+str(round(max(Vcd_var/1000,Vcdmin_var/1000),3))+"  >   Vu = "+str(Vu_var)+"kN ----> 전단철근 불필요"
        check_box.insert(tk.END,text11)
        output_box.insert(tk.END,text11)
    else:
        text11 = "\n\n  Vcd = "+str(round(max(Vcd_var/1000,Vcdmin_var/1000),3))+"  <   Vu = "+str(Vu_var)+"kN ----> 전단철근 필요"
        check_box.insert(tk.END,text11)
        output_box.insert(tk.END,text11)
        text12 = "\n\n ② 전단철근이 배치된 설계전단강도"
        check_box.insert(tk.END,text12)
        output_box.insert(tk.END,text12)
        text13 = "\n\n (1) 전단철근 간격검토"
        check_box.insert(tk.END,text13)
        output_box.insert(tk.END,text13)
        text14 = "\n\n   - 전단철근 간격(s) : "+str(Av_ctc_var)+"mm"
        check_box.insert(tk.END,text14)
        output_box.insert(tk.END,text14)
        text15 = "\n\n   - 종방향 전단철근 간격검토"
        check_box.insert(tk.END,text15)
        output_box.insert(tk.END,text15)
        text16 = "\n\n     s1max = 0.75 x d x (1 + cot α)"
        check_box.insert(tk.END,text16)
        output_box.insert(tk.END,text16)
        s1max_var = 0.75*depth_var*(1+0)
        if s1max_var > Av_ctc_var:
            text17 = "\n           = 0.75 x "+str(round(depth_var))+" x (1 + cot90°) = "+str(round(s1max_var,3))+"mm  >  "+str(Av_ctc_var)+"mm   ---> OK!"
            check_box.insert(tk.END,text17)
            output_box.insert(tk.END,text17)
        else:
            text17 = "\n           = 0.75 x "+str(round(depth_var))+" x (1 + cot90°) = "+str(round(s1max_var,3))+"mm  <  "+str(Av_ctc_var)+"mm   ---> NG!!!!"
            check_box.insert(tk.END,text17)
            output_box.insert(tk.END,text17)
        text18 = "\n\n (2) 최소 전단철근비 검토"
        check_box.insert(tk.END,text18)
        output_box.insert(tk.END,text18)
        text19 = "\n\n   - Av_use = "+str(bar_grade2)+str(Dia4_var)+" x "+str(Av_ea_var)+" ea/m = "+str(round(Av_var,3))+"㎟"
        check_box.insert(tk.END,text19)
        output_box.insert(tk.END,text19)
        low_v_var = Av_var/(Av_ctc_var*width_var*1)
        text20= "\n\n    - ρv = Av / (s x b x sin α)"
        check_box.insert(tk.END,text20)
        output_box.insert(tk.END,text20)
        text21= "\n            = "+str(round(Av_var,3))+" / ("+str(Av_ctc_var)+" x "+str(round(width_var))+" x sin90°) = "+str(round(low_v_var,5))
        check_box.insert(tk.END,text21)
        output_box.insert(tk.END,text21)
        low_vmin_var=(0.08*sqrt(fck_var))/fy_var
        text22= "\n\n    - ρv_min = (0.08 x √(fck) / fy"
        check_box.insert(tk.END,text22)
        output_box.insert(tk.END,text22)
        text23= "\n            = (0.08 x √("+str(round(fck_var,3))+") / "+str(round(fy_var,3))+" = "+str(round(low_vmin_var,5))
        check_box.insert(tk.END,text23)
        output_box.insert(tk.END,text23)
        if low_v_var > low_vmin_var:
            text24="\n\n      ρv = "+str(round(low_v_var,5))+"  >  ρv_min = "+str(round(low_vmin_var,5))+" ------->  OK!"
            check_box.insert(tk.END,text24)
            output_box.insert(tk.END,text24)
        else:
            text24="\n\n      ρv = "+str(round(low_v_var,5))+"  <  ρv_min = "+str(round(low_vmin_var,5))+" ------->  NG!!!!"
            check_box.insert(tk.END,text24)
            output_box.insert(tk.END,text24)
        text25 = "\n\n (3) 설계 전단강도 검토"
        check_box.insert(tk.END,text25)
        output_box.insert(tk.END,text25)
        Vsd_var=pi_s*fvy_var*Av_var*0.9*depth_var/Av_ctc_var*1.0  # cot45는 1.0임 
        text26= "\n\n    - Vsd = Φs x fvy x Av x z / s x cotθ" # z는 단면 내부 팔길이, 근사적으로 0.9d 값을 사용
        check_box.insert(tk.END,text26)
        output_box.insert(tk.END,text26)
        text27= "\n          = "+str(pi_s)+" x "+str(fvy_var)+" x "+str(round(Av_var,3))+" x "+str(round(0.9*depth_var,3))+" / "+str(Av_ctc_var)+" x cot45°"
        check_box.insert(tk.END,text27)
        output_box.insert(tk.END,text27)
        text28 = "\n      = "+str(round(Vsd_var,3))+"N = "+str(round(Vsd_var/1000,3))+"kN"
        check_box.insert(tk.END,text28)
        output_box.insert(tk.END,text28)
        nu_var = 0.6*(1-fck_var/250)
        Vdmax_var=nu_var*pi_c*fck_var*width_var*0.9*depth_var/(1+1)  # cot45, tan45는 1
        text29= "\n\n    - Vd_max = ν x Φc x fck x b x z / (cotθ+tanθ)" # z는 단면 내부 팔길이, 근사적으로 0.9d 값을 사용
        check_box.insert(tk.END,text29)
        output_box.insert(tk.END,text29)
        text30= "\n          = "+str(round(nu_var,3))+" x "+str(pi_c)+" x "+str(fck_var)+" x "+str(width_var)+" x "+str(round(0.9*depth_var,3))+" / (cot45° + tan45°)"
        check_box.insert(tk.END,text30)
        output_box.insert(tk.END,text30)
        text31 = "\n      = "+str(round(Vdmax_var,3))+"N = "+str(round(Vdmax_var/1000,3))+"kN"
        check_box.insert(tk.END,text31)
        output_box.insert(tk.END,text31)
        if Vsd_var < Vdmax_var:
            text32 = "\n\n   Vsd = "+str(round(Vsd_var/1000,3))+"kN   <   Vd_max = "+str(round(Vdmax_var/1000,3))+"kN  ----->  OK!"
            check_box.insert(tk.END,text32)
            output_box.insert(tk.END,text32)
        else:
            text32 = "\n\n   Vsd = "+str(round(Vsd_var/1000,3))+"kN   >   Vd_max = "+str(round(Vdmax_var/1000,3))+"kN  ----->  NG!!!"
            check_box.insert(tk.END,text32)
            output_box.insert(tk.END,text32)
        if Vsd_var > Vu_var*1000:
            text33 = "\n\n   Vsd = "+str(round(Vsd_var/1000,3))+"kN   >   Vu = "+str(Vu_var)+"kN  ----->  OK!"
            check_box.insert(tk.END,text33)
            output_box.insert(tk.END,text33)
        else:
            text33 = "\n\n   Vsd = "+str(round(Vsd_var/1000,3))+"kN   <   Vu = "+str(Vu_var)+"kN  ----->  NG!!!"
            check_box.insert(tk.END,text33)
            output_box.insert(tk.END,text33)
            
check_shear_btn = ttk.Button(check_btn_frm, text = "8.전단 검토")
check_shear_btn.bind("<Return>",CheckShear)
check_shear_btn.bind("<Button-1>",CheckShear)
check_shear_btn.pack(side = tk.LEFT)

#-------------------------------------------------------------------------------
combi1_var = str()
limit_crack = float()
h1_var = float() # 단면기준깊이
k1_var = float() # 축력이 응력분포에 미치는 영향계수
fct_var = float() # 콘크리트 인장강도는 평균인장강도를 취한다(재령28일 이후로 가정)
fs_var = float() # 첫균열 발생 직후에 허용하는 철근의 인장응력
kc_var = float() # 균열발생 직전의 단면 내 응력분포 상태계수
k_var = float() # 간접하중영향에 의해 부등 분포하는 응력의 영향을 반영하는 계수
Act_var = float() # 콘크리트의 유효인장단면적 (첫 균열 발생 직전 상태에서 계산된 콘크리트의 인장 영역 단면적)
Ec_var = float() # 콘크리트 탄성계수
n_var = int() # 탄성계수비
x_var = float() # 중립축 거리(압축연단에서)
As_min10 = float() # 균열제어를 위한 최소철근량
DiaMax_var = float() # 최대직경
ctcMax_var = float() # 최대간격

def CheckUse(event):
    global combi1_var
    global limit_crack
    global h1_var  # 단면기준깊이
    global k1_var  # 축력이 응력분포에 미치는 영향계수
    global fct_var  # 콘크리트 인장강도는 평균인장강도를 취한다(재령28일 이후로 가정)
    global fs_var  # 첫균열 발생 직후에 허용하는 철근의 인장응력
    global kc_var  # 균열발생 직전의 단면 내 응력분포 상태계수
    global k_var # 간접하중영향에 의해 부등 분포하는 응력의 영향을 반영하는 계수
    global Act_var # 콘크리트의 유효인장단면적 (첫 균열 발생 직전 상태에서 계산된 콘크리트의 인장 영역 단면적)
    global Ec_var # 콘크리트 탄성계수
    global n_var  # 탄성계수비
    global x_var  # 중립축 거리(압축연단에서)
    global As_min10 # 균열제어를 위한 최소철근량
    global DiaMax_var # 최대직경
    global ctcMax_var # 최대간격
    check_box.delete(1.0,tk.END)
    RebarChange()
    if design_grade == "B":
        combi1_var = "사용하중조합-Ⅰ"
        limit_crack = 0.2
        text1 = "\n\n(2)사용한계상태\n 노출환경에 따른 적용설계등급 : "+str(design_grade)+"\n 균열폭 한계상태 하중조합 : "+str(combi1_var)+"\n 한계균열폭 : "+str(limit_crack)+" mm"
        check_box.insert(tk.END,text1)
        output_box.insert(tk.END,text1)
    elif design_grade == "C":
        combi1_var = "사용하중조합-Ⅲ/Ⅳ"
        limit_crack = 0.2
        text1 = "\n\n(2)사용한계상태\n 노출환경에 따른 적용설계등급 : "+str(design_grade)+"\n 균열폭 한계상태 하중조합 : "+str(combi1_var)+"\n 한계균열폭 : "+str(limit_crack)+" mm"
        check_box.insert(tk.END,text1)
        output_box.insert(tk.END,text1)
    elif design_grade == "D":
        combi1_var = "사용하중조합-Ⅲ/Ⅳ"
        limit_crack = 0.3
        text1 = "\n\n(2)사용한계상태\n 노출환경에 따른 적용설계등급 : "+str(design_grade)+"\n 균열폭 한계상태 하중조합 : "+str(combi1_var)+"\n 한계균열폭 : "+str(limit_crack)+" mm"
        check_box.insert(tk.END,text1)
        output_box.insert(tk.END,text1)
    elif design_grade == "E":
        combi1_var = "사용한계상태 하중조합-Ⅴ"
        limit_crack = 0.3
        text1 = "\n\n(2)사용한계상태\n\n 노출환경에 따른 적용설계등급 : "+str(design_grade)+"\n 균열폭 한계상태 하중조합 : "+str(combi1_var)+"\n 한계균열폭 : "+str(limit_crack)+" mm"
        check_box.insert(tk.END,text1)
        output_box.insert(tk.END,text1)
    text2 = "\n\n 1. 균열제어를 위한 최소철근량 검토"
    check_box.insert(tk.END,text2)
    output_box.insert(tk.END,text2)
    if height_var < 1000:
        h1_var = height_var
    else:
        h1_var = 1000
    k1_var = 1.5  # 작용 축력을 압축으로 가정
    fct_var = fctk_var/0.7
    Ec_var = 0.077*2450**1.5*fcm_var**(1/3)
    n_var = int(Es_var/Ec_var)
    x_var = (-1*n_var*As_total+sqrt((n_var*As_total)**2+4*width_var/2*n_var*As_total*depth_var))/(2*width_var/2)
    fs_var = M0_var*1000000/(As_total*(depth_var-x_var/3))
    kc_var = 0.4*(1-fn_var/(k1_var*height_var/h1_var*fct_var))
    if width_var < 300:
        k_var = 1.0
    elif width_var > 800:
        k_var = 0.65
    else:
        k_var = 1-0.35/500*(width_var-300)
    Act_var = width_var*min(2.5*(height_var-depth_var),(height_var-x_var)/3,height_var/2)
    text300 = "\n x = "+str(round(x_var,3))+"  As = "+str(round(As_total,3))+"  d = "+str(round(depth_var,3))+"  fcm = "+str(round(fcm_var,3))+"  n = "+str(round(n_var,3))+"  b = "+str(round(width_var,3))+"  d = "+str(round(depth_var,3))
    check_box.insert(tk.END,text300)
    text3 = "\n\n   - kc = 균열발생 직전의 단면 내 응력분포 상태를 반영하는 계수 = "+str(round(kc_var,3))
    check_box.insert(tk.END,text3)
    output_box.insert(tk.END,text3)
    text4 = "\n   - k = 간접하중영향에 의해 부등 분포하는 응력의 영향을 반영하는 계수 = "+str(round(k_var,3))
    check_box.insert(tk.END,text4)
    output_box.insert(tk.END,text4)
    text5 = "\n   - Act = 콘크리트의 유효 인장 단면적 = "+str(round(Act_var,3))+" ㎟ "
    check_box.insert(tk.END,text5)
    output_box.insert(tk.END,text5)
    text6 = "\n   - fct = 첫 균열이 발생할 때 유효한 콘크리트 인장강도 = "+str(round(fct_var,3))+" MPa"
    check_box.insert(tk.END,text6)
    output_box.insert(tk.END,text6)
    text7 = "\n   - fs = 첫 균열 발생 직후에 허용하는 철근의 인장강도( = Mo/(As*(d-(x/3))) = "+str(round(fs_var,3))+" MPa"
    check_box.insert(tk.END,text7)
    output_box.insert(tk.END,text7)
    As_min10 = kc_var*k_var*Act_var*fct_var/fs_var
    text8 = "\n   - As_min = 균열제어를 위한 최소철근량"
    check_box.insert(tk.END,text8)
    output_box.insert(tk.END,text8)
    text9 = "\n   -        = kc x k x Act x fct/fs"
    check_box.insert(tk.END,text9)
    output_box.insert(tk.END,text9)
    text10 = "\n   -        = "+str(round(kc_var,3))+" x "+str(round(k_var,3))+" x "+str(round(Act_var,3))+" x "+str(round(fct_var,3))+"/"+str(round(fs_var,3))+" = "+str(round(As_min10,3))+" ㎟"
    check_box.insert(tk.END,text10)
    output_box.insert(tk.END,text10)
    if As_total > As_min10:
        text11 = "\n\n   As_use = "+str(round(As_total,3))+" ㎟  >  As_min = "+str(round(As_min10,3))+" ㎟  ------> OK!"
        check_box.insert(tk.END,text11)
        output_box.insert(tk.END,text11)
    else:
        text11 = "\n\n   As_use = "+str(round(As_total,3))+" ㎟  <  As_min = "+str(round(As_min10,3))+" ㎟  ------> NG!!!"
        check_box.insert(tk.END,text11)
        output_box.insert(tk.END,text11)
    text12 = "\n\n 2. 간접균열제어 (철근콘크리트 기준)"
    check_box.insert(tk.END,text12)
    output_box.insert(tk.END,text12)
    text13 = "\n\n   - 균열제어를 위해 철근의 발생응력에 따라 최대 철근지름과\n     최대 철근간격기준을 준수한다.(도.설.기 5-125)"
    check_box.insert(tk.END,text13)
    output_box.insert(tk.END,text13)
    text14 = "\n   - 최소철근량 조건을 만족하고,\n     배치된 철근이 최대 철근지름과 최대 철근간격 중 하나를 만족한다면\n     균열폭이 허용 한계값 이내에 있다고 간주할 수 있다.\n     이 때 철근응력은 균열단면을 기준으로 계산하여야 한다."
    check_box.insert(tk.END,text14)
    output_box.insert(tk.END,text14)
    if fs_var < 160:
        DiaMax_var = 32
    elif fs_var < 200:
        DiaMax_var = 25
    elif fs_var < 240:
        DiaMax_var = 16
    elif fs_var < 280:
        DiaMax_var = 14
    elif fs_var < 320:
        DiaMax_var = 10
    elif fs_var < 360:
        DiaMax_var = 8
    text15 = "\n\n    - fs = 철근응력 = Mo/(As*(d-(x/3)) = "+str(round(fs_var,3))+" MPa"
    check_box.insert(tk.END,text15)
    output_box.insert(tk.END,text15)
    if fs_var < 160:
        ctcMax_var = 300
    elif fs_var < 200:
        ctcMax_var = 250
    elif fs_var < 240:
        ctcMax_var = 200
    elif fs_var < 280:
        ctcMax_var = 150
    elif fs_var < 320:
        ctcMax_var = 100
    elif fs_var < 360:
        ctcMax_var = 50
    if DiaMax_var > Dia1_var:
        text16 = "\n\n   최대 철근지름(mm) = "+str(round(DiaMax_var,0))+" mm   >   사용 철근지름(mm) = "+str(round(Dia1_var,0))+" mm  ------> OK!"
        check_box.insert(tk.END,text16)
        output_box.insert(tk.END,text16)
    else:
        text16 = "\n\n   최대 철근지름(mm) = "+str(round(DiaMax_var,0))+" mm   <   사용 철근지름(mm) = "+str(round(Dia1_var,0))+" mm  ------> NG!!!"
        check_box.insert(tk.END,text16)
        output_box.insert(tk.END,text16)
    if ctcMax_var > ((width_var-200)/(As_ea1_var-1)):
        text17 = "\n\n   최대 철근간격(mm) = "+str(round(ctcMax_var,0))+" mm   >   사용 철근간격(mm) = "+str(round(((width_var-200)/(As_ea1_var-1)),0))+" mm  ------> OK!"
        check_box.insert(tk.END,text17)
        output_box.insert(tk.END,text17)
    else:
        text17 = "\n\n   최대 철근간격(mm) = "+str(round(ctcMax_var,0))+" mm   <   사용 철근간격(mm) = "+str(round(((width_var-200)/(As_ea1_var-1)),-1))+" mm  ------> NG!!!"
        check_box.insert(tk.END,text17)
        output_box.insert(tk.END,text17)
        
check_use_btn = ttk.Button(check_btn_frm, text = "9.사용한계상태")
check_use_btn.bind("<Return>",CheckUse)
check_use_btn.bind("<Button-1>",CheckUse)
check_use_btn.pack(side = tk.LEFT)

scrol_w  = 90  # 스크롤텍스트박스의 폭
scrol_h  = 12  # 스크롤텍스트박스의 높이
check_box = scrolledtext.ScrolledText(output_frm, width = scrol_w, height = scrol_h, wrap = tk.WORD)
check_box.pack()

blank50_lbl = ttk.Label(output_frm, text = "  ") 
blank50_lbl.pack()

result_btn_frm = tk.Frame(output_frm, padx = 4, pady = 4)
result_btn_frm.pack()

def OutputArrangedFile(event):  # 열기 클릭시 호출되는 함수 정의
    input_box.delete(1.0,tk.END)
    output_box.delete(1.0,tk.END)
    TitleWrite(event)
    check()
    FactorCalc(event)
    Input1Write(event)
    Input2Write(event)
    RebarGrade1(event)
    RebarGrade2(event)
    RebarAs1(event)
    RebarAs2(event)
    RebarAs3(event)
    RebarAv(event)
    Input3Write(event)
    CheckAsMin(event)
    CheckAsMax(event)
    CheckCMax(event)
    CheckBarStrain(event)
    CheckBending(event)
    CheckShear(event)
    CheckUse(event)
    
output_arrange_btn = ttk.Button(result_btn_frm, text = "결과파일 정리")
output_arrange_btn.bind("<Return>",OutputArrangedFile)
output_arrange_btn.bind("<Button-1>",OutputArrangedFile)
output_arrange_btn.pack(side = tk.LEFT)

def OutputSaveFile(event):  # 저장 클릭시 호출되는 함수 정의
    # 쓰기모드로 열고 사용자가 확장자명을 지정하지 않으면 *.txt로 저징한다
    file=asksaveasfile(mode="w",defaultextension=".txt",filetype=(("텍스트파일","*.txt"),("모든파일","*.*")))
    # 그런데 파일이 없다면 무효화 처리해준다.
    if file is None:
        return
    # 저장을 위해 텍스트 위젯의 내용을 첨부터 끝까지 가져옴
    text_output=str(output_box.get(1.0,tk.END))
    file.write(text_output)  # 파일저장, file에 ts를 쓴다.
    file.close()

output_write_btn = ttk.Button(result_btn_frm, text = "결과파일 저장")
output_write_btn.bind("<Return>",OutputSaveFile)
output_write_btn.bind("<Button-1>",OutputSaveFile)
output_write_btn.pack(side = tk.LEFT)
    
blank51_lbl = ttk.Label(output_frm, text = "  ") 
blank51_lbl.pack()

scrol_w  = 90  # 스크롤텍스트박스의 폭
scrol_h  = 30  # 스크롤텍스트박스의 높이
output_box = scrolledtext.ScrolledText(output_frm, width = scrol_w, height = scrol_h, wrap = tk.WORD)
output_box.pack()

RCDesign_pwin.add(output_frm) 



RCDesign.mainloop()  # 마우스 및 키보드 이벤트를 기다리면서 응용프로그램의 기본 루프를 시작한다.