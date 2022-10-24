#
import tkinter as tk  # tkinter 모듈을 프로그램의 네임 스페이스로 가져 오지만 이름을 tk로 바꾼다.
from tkinter import ttk
from math import *
from tkinter.font import Font  # tkinter.font 모듈을 임포트하고 Font 클래스 생성자를 사용 '글꼴 객체'를 만듬
from tkinter.filedialog import *
from tkinter import scrolledtext
# from tkinter import messagebox as msg
# import pymysql  # DB활용을 위한... 실패!!!!!!!!!!!!!!!!!!
# import os  # 파일 이름을 가져오기 위해 os모듈을 임포트
# import subprocess  # 외부파일 실행용
# import datetime  # 날짜+시간탑재

EXAM = tk.Tk()  # 생성자를 호출해 Tk클래스의 인스턴스를 생성한다. RCDesign이라는 메인창을 정의

EXAM.title('test')  # 창 우상단 제목
EXAM.geometry('600x200+100+30')  # 크기+x좌표+y좌표

# i_var=tk.DoubleVar()
# j_var=tk.DoubleVar()
# result_var=tk.DoubleVar()
i_var=tk.StringVar()
j_var=tk.StringVar()
result_var=tk.StringVar()
result_var=()

def Calc(event):
     print(i_var.get())
     output_ent.delete(0,'end')
     output_ent.insert(1,int(i_var.get()) + int(j_var.get()))
     #i_var = exam1_ent.
     #exam_lbl.config(text="result : " + str(i_var.get() + j_var.get()))
     exam_lbl.config(text="result : " + str(int(i_var.get()) + int(j_var.get())))
     #exam1_lbl.config(text="result : " + str(result_var.get()))
     #print("test")

exam1_ent = ttk.Entry(EXAM,width=10,justify=tk.RIGHT,textvariable=i_var)
exam1_ent.grid(column = 1, row = 1, padx = 3, pady = 3, sticky = tk.W)

exam2_ent = ttk.Entry(EXAM,width=10,justify=tk.RIGHT,textvariable=j_var)
exam2_ent.bind("<Return>",Calc)
exam2_ent.grid(column = 2, row = 1, padx = 3, pady = 3, sticky = tk.W)

exam_lbl = ttk.Label(EXAM, text = "result : ") 
exam_lbl.grid(column = 1, row = 2, pady = 3, sticky = tk.E)

output_ent = ttk.Entry(EXAM,width=20,justify=tk.RIGHT,textvariable=result_var)
output_ent.grid(column = 1, row = 3, padx = 3, pady = 3, sticky = tk.W)

exam1_lbl = ttk.Label(EXAM, text = "result : ") 
exam1_lbl.grid(column = 1, row = 4, pady = 3, sticky = tk.E)

bt = ttk.Button(None, text='Show result')
bt.grid()
bt.bind("<Button-1>",Calc)


EXAM.mainloop()  # 마우스 및 키보드 이벤트를 기다리면서 응용프로그램의 기본 루프를 시작한다.