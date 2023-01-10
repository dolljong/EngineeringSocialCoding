import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


#class MyApp(QWidget):
class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()

        self.menubar = self.menuBar()
        self.menubar.setNativeMenuBar(False)

        # file menu action
        self.new_action = QAction("New")
        self.quit_action = QAction("Quit")
        self.quit_action.triggered.connect(self.close)
        
        # calc menu actions
        self.calc_action = QAction("Calc")

        # help menu action
        self.doc_action = QAction("Documentation")
        self.release_action = QAction("Release Notes")
        self.license_action = QAction("View License")

        # file menu
        file_menu = self.menubar.addMenu("파일")
        file_menu.addAction(self.new_action)
        file_menu.addSeparator()
        file_menu.addAction(self.quit_action)
        
        # Calculate menu
        calc_menu = self.menubar.addMenu("Calc")
        calc_menu.addAction(self.calc_action)
        #calc_menu.addSeparator()
        #calc_menu.addAction(self.quit_action)

        # help menu
        help_menu = self.menubar.addMenu("도움말")
        help_menu.addAction(self.doc_action)
        help_menu.addAction(self.release_action)
        help_menu.addAction(self.license_action)
        
        calcAction = QAction(QIcon('calc.png'), 'Calc', self)
        calcAction.setStatusTip('Calculate Sections')
        self.toolbar = self.addToolBar('Calc')
        self.toolbar.addAction(calcAction)
        
        
        self.initUI()

    def initUI(self):
    
        exitAction = QAction(QIcon('exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)
         
        self.statusBar().showMessage('Ready')
        
        self.setWindowTitle('Statusbar')
        
        #self.setGeometry(300, 300, 300, 200)
        
        #self.show()
        
        #QMainWindow.setObjectName("MainWindow")
        #QMainWindow.resize(800, 600)
        #self.centralwidget = QtWidgets.QWidget(MainWindow)
        #self.centralwidget.setObjectName("centralwidget")
        
        tab1 = QWidget()
        tab2 = QWidget()

        tabs = QTabWidget()
        tabs.addTab(tab1, 'Tab1')
        tabs.addTab(tab2, 'Tab2')
        
        # vbox = QVBoxLayout()
        # vbox.addWidget(tabs)

        label1 = QLabel('Material', self)
        label1.setAlignment(Qt.AlignLeft)
        
        label = QLabel('Force & Rebar Area', self)
        label.setAlignment(Qt.AlignLeft)

        self.tableWidget1 = QTableWidget()
        self.tableWidget = QTableWidget()
        
        self.tableWidget1.setRowCount(1)
        self.tableWidget1.setColumnCount(4)
        self.tableWidget1.setHorizontalHeaderLabels(['fck(MPa)','fy(MPa)','Øc','Øs'])
        self.tableWidget1.verticalHeader().hide();
        self.tableWidget1.setFixedSize(660, 80)
        self.tableWidget1.resizeColumnsToContents()
        stylesheet = "::section{Background-color:rgb(245,245,245)}"
        self.tableWidget1.horizontalHeader().setStyleSheet(stylesheet)
        self.tableWidget1.verticalHeader().setStyleSheet(stylesheet)
        
        self.tableWidget.setRowCount(20)
        self.tableWidget.setColumnCount(14)
        self.tableWidget.setHorizontalHeaderLabels(['Name','Mu\n(kN.m)','Vu\n(kN)','Nu\n(kN)', 'Ms\n(kN.m)','H\n(mm)','B\n(mm)','Dc\n(mm)', 'As_Dia\n(mm)', 'As_Num\n(EA)','δ', 'Av_Dia\n(mm)','Av_Leg\n(EA)', 'Av_Space\n(mm)'])
        #self.tableWidget.resize(400,100)
        self.tableWidget.setFixedSize(1700,300)
        self.tableWidget.resizeColumnsToContents()
        #self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        #self.tableWidget.setItemDelegateForColumn(0, QStyledItemDelegate(displayAlignment=QtCore.Qt.AlignCenter))
        
        self.tableWidget.horizontalHeader().setStyleSheet(stylesheet)
        self.tableWidget.verticalHeader().setStyleSheet(stylesheet)
        
        #self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.tableWidget.setEditTriggers(QAbstractItemView.DoubleClicked)
        #self.tableWidget.setEditTriggers(QAbstractItemView.AllEditTriggers)

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        samplematdata=['35','400','0.65','0.7']
        for j in range(4):
            self.tableWidget1.setItem(0, j, QTableWidgetItem(samplematdata[j]))
        self.tableWidget1.horizontalHeaderItem(0).setToolTip("콘크리트설계강도")
        self.tableWidget1.horizontalHeaderItem(1).setToolTip("철근항복강도")
            
        sampledata=['Center','100','50','5','80','800','1000','80','25','8','1','16','2','400']
        for j in range(14):
            self.tableWidget.setItem(0, j, QTableWidgetItem(sampledata[j]))

        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        layout.addWidget(tabs)
        layout.addWidget(label1)
        layout.addWidget(self.tableWidget1)
        layout.addWidget(label)
        layout.addWidget(self.tableWidget)
        
        layout.setStretchFactor(label1,1)
        layout.setStretchFactor(self.tableWidget1,2)
        layout.setStretchFactor(label1,1)
        layout.setStretchFactor(self.tableWidget,5)
              
        #self.setLayout(layout)
        self.setCentralWidget(widget)

        self.setWindowTitle('QTableWidget')
        self.setGeometry(300, 100, 1024, 400)
        self.show()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())