import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from math import *
import subprocess  # 외부파일 실행용
from PyQt5.QtWebEngineWidgets import *

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("Kanghee_QT_03.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.fontSize = 10
        """
        ---------------------------------------------
        이 부분에 시그널을 입력해야 합니다.
        시그널이 작동할 때 실행될 기능은 보통 이 클래스의 멤버함수로 작성합니다.
        ---------------------------------------------
        """
        #문법 : 위젯.이벤트.연결(연결할 함수)
        #MemoTxtEdt를 다루기위한 이벤트들과 버튼기능연결
        self.new_MemoTxtEdt_btn.clicked.connect(self.new_MemoTxtEdt_btn_Function)
        self.open_MemoTxtEdt_btn.clicked.connect(self.open_MemoTxtEdt_btn_Function)
        self.save_MemoTxtEdt_btn.clicked.connect(self.save_MemoTxtEdt_btn_Function)
        self.add_MemoTxtEdt_btn.clicked.connect(self.add_MemoTxtEdt_btn_Function)
        self.FontRed_MemoTxtEdt_btn.clicked.connect(self.FontRed_MemoTxtEdt_btn_Function)
        self.FontUp_MemoTxtEdt_btn.clicked.connect(self.FontUp_MemoTxtEdt_btn_Function)
        self.FontDn_MemoTxtEdt_btn.clicked.connect(self.FontDn_MemoTxtEdt_btn_Function)

        #LnCalcEdt를 다루기위한 이벤트들과 기능연결
        self.LnCalcEdt.textChanged.connect(self.LnCalcEdt_change_Function)
        self.LnCalcEdt.returnPressed.connect(self.LnCalcEdt_enterkey_Function)

        #업무용 단추들이 눌려졋을때 기능연결
        self.FileManager_Run_btn.clicked.connect(self.FileManager_Run_btn_Function)
        self.FileFind_Run_btn.clicked.connect(self.FileFind_Run_btn_Function)
        self.Capture_Run_btn.clicked.connect(self.Capture_Run_btn_Function)
        self.RcWork_Run_btn.clicked.connect(self.RcWork_Run_btn_Function)
        self.PdfManager_Run_btn.clicked.connect(self.PdfManager_Run_btn_Function)
        self.ExlManager_Run_btn.clicked.connect(self.ExlManager_Run_btn_Function)
        
        #프로그램이 실행되면 DateTimeEdit의 값이 현재 날짜/시간으로 설정되게 하기
        self.currentDateTime = QDateTime.currentDateTime()
        self.dateTimeEdit.setDateTime(self.currentDateTime)

        #WebEngineView의 시그널 및 버튼들에 기능을 연결
        # self.webEngineView.loadStarted.connect(self.printLoadStart)
        # self.webEngineView.loadProgress.connect(self.printLoading)
        # self.webEngineView.loadFinished.connect(self.printLoadFinished)
        self.webEngineView.urlChanged.connect(self.urlChangedFunction)        
        self.go_LnUrlEdt_btn.clicked.connect(self.go_LnUrlEdt_btn_Function)
        self.LnUrlEdt.returnPressed.connect(self.go_LnUrlEdt_btn_Function)
        self.back_LnUrlEdt_btn.clicked.connect(self.back_LnUrlEdt_btn_Function)
        self.forward_LnUrlEdt_btn.clicked.connect(self.forward_LnUrlEdt_btn_Function)
        self.reload_LnUrlEdt_btn.clicked.connect(self.reload_LnUrlEdt_btn_Function)
        self.stop_LnUrlEdt_btn.clicked.connect(self.stop_LnUrlEdt_btn_Function)
        self.korea_LnUrlEdt_btn.clicked.connect(self.korea_LnUrlEdt_btn_Function)
        self.naver_LnUrlEdt_btn.clicked.connect(self.naver_LnUrlEdt_btn_Function)
        self.dic_LnUrlEdt_btn.clicked.connect(self.dic_LnUrlEdt_btn_Function)
        self.papago_LnUrlEdt_btn.clicked.connect(self.papago_LnUrlEdt_btn_Function)
        
    #WebEngineView의 시그널에 연결된 함수들 및 관련 버튼을 눌렀을 때 실행될 함수들
    # def printLoadStart(self) : print("Start Loading")
    # def printLoading(self) : print("Loading")
    # def printLoadFinished(self) : print("Load Finished")
    def urlChangedFunction(self) :
        self.LnUrlEdt.setText(self.webEngineView.url().toString())
    #     print("Url Changed")
    def go_LnUrlEdt_btn_Function(self) :
        self.webEngineView.load(QUrl(self.LnUrlEdt.text()))
    def back_LnUrlEdt_btn_Function(self) :
        self.webEngineView.back()
    def forward_LnUrlEdt_btn_Function(self) :
        self.webEngineView.forward()
    def reload_LnUrlEdt_btn_Function(self) :
        self.webEngineView.reload()
    def stop_LnUrlEdt_btn_Function(self) :
        self.webEngineView.stop()
    def korea_LnUrlEdt_btn_Function(self) :
        self.LnUrlEdt.setText('http://mbox07.korea.com/main.crd#module%3Djson.mail.MailList%26page%3D1%26nPage%3D1%26folder%3DINBOX')
        self.webEngineView.load(QUrl(self.LnUrlEdt.text()))
    def naver_LnUrlEdt_btn_Function(self) :
        self.LnUrlEdt.setText('https://www.naver.com')
        self.webEngineView.load(QUrl(self.LnUrlEdt.text()))
    def dic_LnUrlEdt_btn_Function(self) :
        self.LnUrlEdt.setText('https://dict.naver.com/')
        self.webEngineView.load(QUrl(self.LnUrlEdt.text()))
    def papago_LnUrlEdt_btn_Function(self) :
        self.LnUrlEdt.setText('https://papago.naver.com/')
        self.webEngineView.load(QUrl(self.LnUrlEdt.text()))
        
    #MemoTxtEdt관련 btn이 눌리면 작동할 함수들
    def new_MemoTxtEdt_btn_Function(self) :
        self.MemoTxtEdt.clear()
    def open_MemoTxtEdt_btn_Function(self) :
        FileOpen = QFileDialog.getOpenFileName(self, 'Open file', '' ,'txt File(*.txt);; PY File (*.py);; html File (*.html *.htm);; All File (*.*)')
        f=open(FileOpen[0],'r') #, encoding='UTF8')
        Memo01=f.read()
        self.MemoTxtEdt.setText(Memo01)
        f.close()
    def save_MemoTxtEdt_btn_Function(self) :
        FileSave = QFileDialog.getSaveFileName(self, 'Save file', '' ,'txt File(*.txt);; PY File (*.py);; html File (*.html);; All File (*.*)')
        Memo01=self.MemoTxtEdt.toPlainText()
        f=open(FileSave[0],'w') #, encoding='UTF8')
        f.write(Memo01)
        f.close()
    def add_MemoTxtEdt_btn_Function(self) :
        FileSave = QFileDialog.getSaveFileName(self, 'Save file', '' ,'txt File(*.txt);; All File (*.*)')
        Memo01="\n"+self.MemoTxtEdt.toPlainText()
        f=open(FileSave[0],'a') #, encoding='UTF8')
        f.write(Memo01)
        f.close()
    def FontRed_MemoTxtEdt_btn_Function(self) :
        colorvar=QColor(255,0,0)
        self.MemoTxtEdt.setTextColor(colorvar)
    def FontUp_MemoTxtEdt_btn_Function(self) :
        self.fontSize=self.fontSize+1
        self.MemoTxtEdt.setFontPointSize(self.fontSize)
    def FontDn_MemoTxtEdt_btn_Function(self) :
        self.fontSize=self.fontSize-1
        self.MemoTxtEdt.setFontPointSize(self.fontSize)

    #LnCalcEdt의 글자를 입력할때 lnedt_lbl 의 글자가 바뀌는 함수
    def LnCalcEdt_change_Function(self) :
        self.LnCalc_lbl.setText(self.LnCalcEdt.text())
    #LnCalcEdt의 글자를 입력하고 엔터키 칠때 결과 출력하는 함수
    def LnCalcEdt_enterkey_Function(self) :
        self.LnCalcResult_lbl.setText('= '+str(eval(self.LnCalcEdt.text())))  # eval()함수는 문장을 그대로 수식연산이 가능함
        es1=self.LnCalcEdt.text()+"="+str(round(eval(self.LnCalcEdt.text()),3))  # es는 단순 옮겨 적기용이므로 global 변수 지정은 필요 없다?
        es2="\n"+self.LnCalcEdt.text()+"="+str(round(eval(self.LnCalcEdt.text()),3))  # es는 단순 옮겨 적기용이므로 global 변수 지정은 필요 없다?
        self.LnCalc_lbl.setText(es1)
        self.MemoTxtEdt.append(es2)

    #업무용 btn이 눌리면 작동할 함수들
    def FileManager_Run_btn_Function(self) :
        subprocess.run('C:/Program Files (x86)/flyExplorer/flyExplorer')
    def FileFind_Run_btn_Function(self) :
        subprocess.run('F:/02주인방/03작은풀그림/Everything-1.4.1.935.x64/Everything')
    def Capture_Run_btn_Function(self) :
        subprocess.run('cap98')
    def RcWork_Run_btn_Function(self) :
        subprocess.run('RC-GIRDER-단면검토-한계상태-VER02')
    def PdfManager_Run_btn_Function(self) :
        subprocess.run('PDF관리_PyQt')
    def ExlManager_Run_btn_Function(self) :
        subprocess.run('C:/Program Files/Microsoft Office/root/Office16/EXCEL')


if __name__ == "__main__" :
    app = QApplication(sys.argv)  #QApplication : 프로그램을 실행시켜주는 클래스
    myWindow = WindowClass()      #WindowClass의 인스턴스 생성
    myWindow.show()  #프로그램 화면을 보여주는 코드
    app.exec_()      #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드