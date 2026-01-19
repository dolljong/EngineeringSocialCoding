import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight

class ComboBoxDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(ComboBoxDelegate, self).__init__(parent)
        self.items = ['13', '16', '19', '22', '25', '29', '32', '35']

    def createEditor(self, parent, option, index):
        editor = QComboBox(parent)
        editor.addItems(self.items)
        editor.setEditable(True)
        editor.lineEdit().setAlignment(Qt.AlignCenter)
        editor.setStyleSheet("QComboBox { text-align: center; }")
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole)
        if value:
            editor.setCurrentText(str(value))

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def paint(self, painter, option, index):
        if not self.parent().indexWidget(index):
            self.parent().setIndexWidget(
                index,
                self.createEditor(self.parent().viewport(), option, index)
            )
        super(ComboBoxDelegate, self).paint(painter, option, index)

class CustomHeaderView(QHeaderView):
    def __init__(self, orientation, parent=None):
        super(CustomHeaderView, self).__init__(orientation, parent)
        self.setSectionsClickable(True)
        self.setSortIndicatorShown(True)

    def sectionSizeHint(self, logicalIndex):
        size = super(CustomHeaderView, self).sectionSizeHint(logicalIndex)
        if self.orientation() == Qt.Horizontal:
            return max(size, self.fontMetrics().width(self.model().headerData(logicalIndex, Qt.Horizontal, Qt.DisplayRole)) + 20)
        return size

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
        tabs.addTab(tab1, 'RC section')
        tabs.addTab(tab2, 'Tab2')
        
        # vbox = QVBoxLayout()
        # vbox.addWidget(tabs)

        label1 = QLabel('Material', self)
        label1.setAlignment(Qt.AlignLeft)
        
        label = QLabel('Force & Rebar Area', self)
        label.setAlignment(Qt.AlignLeft)

        self.hbox = QHBoxLayout()

        self.cbforces = QCheckBox('Show forces', self)
        self.cbforces.toggle()
        self.cbforces.stateChanged.connect(self.showforce)

        self.cbsecinfo = QCheckBox('Show sec info', self)
        self.cbsecinfo.toggle()
        self.cbsecinfo.stateChanged.connect(self.showsecinfo)

        self.cbbandrebar = QCheckBox('Show band rebar', self)
        self.cbbandrebar.toggle()
        self.cbbandrebar.stateChanged.connect(self.showbandrebar)

        self.cbshearrebar = QCheckBox('Show band rebar', self)
        self.cbshearrebar.toggle()
        self.cbshearrebar.stateChanged.connect(self.showshearrebar)

        self.hbox.addWidget(self.cbforces)
        self.hbox.addWidget(self.cbsecinfo)
        self.hbox.addWidget(self.cbbandrebar)
        self.hbox.addWidget(self.cbshearrebar)
        self.hbox.addStretch()

        self.tableWidget1 = QTableWidget()
        self.tableWidget = QTableWidget()
        
        
        self.tableWidget1.setRowCount(1)
        self.tableWidget1.setColumnCount(5)
        self.tableWidget1.setHorizontalHeaderLabels(['fck(MPa)','fy(MPa)','Øc','Øs',''])
        self.tableWidget1.verticalHeader().hide()
        header1 = CustomHeaderView(Qt.Horizontal, self.tableWidget1)
        self.tableWidget1.setHorizontalHeader(header1)
        self.tableWidget1.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget1.horizontalHeader().setStretchLastSection(True)

        self.tableWidget1.setFixedSize(660, 110)
        self.tableWidget1.resizeColumnsToContents()
        stylesheet = "::section{Background-color:rgb(245,245,245)}"
        self.tableWidget1.horizontalHeader().setStyleSheet(stylesheet)
        self.tableWidget1.verticalHeader().setStyleSheet(stylesheet)
        self.tableWidget1.horizontalHeader().setStretchLastSection(True)
        self.tableWidget1.setColumnWidth(0, 80)
        self.tableWidget1.setColumnWidth(1, 80)
        self.tableWidget1.setColumnWidth(2, 80)
        self.tableWidget1.setColumnWidth(3, 80)
        delegate = AlignDelegate(self.tableWidget)
        for icol in range(0,4):
            self.tableWidget1.setItemDelegateForColumn(icol, delegate)
        
        self.tableWidget.setRowCount(20)
        self.tableWidget.setColumnCount(15)
        self.tableWidget.setHorizontalHeaderLabels(['Name','Mu\n(kN.m)','Vu\n(kN)','Nu\n(kN)', 'Ms\n(kN.m)','H\n(mm)','B\n(mm)','Dc\n(mm)', 'As_Dia\n(mm)', 'As_Num\n(EA)','δ', 'Av_Dia\n(mm)','Av_Leg\n(EA)', 'Av_Space\n(mm)',''])
        header = CustomHeaderView(Qt.Horizontal, self.tableWidget)
        self.tableWidget.setHorizontalHeader(header)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.setFixedSize(1700,300)

        self.tableWidget.resizeColumnsToContents()

        self.tableWidget.setColumnWidth(0, 200)
        # self.tableWidget.setColumnWidth(1, 80)
        # self.tableWidget.setColumnWidth(2, 80)
        # self.tableWidget.setColumnWidth(3, 80)
        # self.tableWidget.setColumnWidth(4, 80)
        # self.tableWidget.setColumnWidth(5, 80)
        # self.tableWidget.setColumnWidth(6, 80)
        # self.tableWidget.setColumnWidth(7, 80)
        # self.tableWidget.setColumnWidth(8, 80)
        # self.tableWidget.setColumnWidth(9, 80)
        # self.tableWidget.setColumnWidth(10, 80)
        # self.tableWidget.setColumnWidth(11, 80)
        # self.tableWidget.setColumnWidth(12, 80)
        # self.tableWidget.setColumnWidth(13, 80)
        delegate = AlignDelegate(self.tableWidget)
        for icol in range(1,14):
            self.tableWidget.setItemDelegateForColumn(icol, delegate)



        #self.tableWidget.resize(400,100)
        
        #self.tableWidget.resizeColumnsToContents()
        #self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        #self.tableWidget.setItemDelegateForColumn(0, QStyledItemDelegate(displayAlignment=QtCore.Qt.AlignCenter))
        
        self.tableWidget.horizontalHeader().setStyleSheet(stylesheet)
        self.tableWidget.verticalHeader().setStyleSheet(stylesheet)
        
        combo_delegate = ComboBoxDelegate(self.tableWidget)
        self.tableWidget.setItemDelegateForColumn(8, combo_delegate)  # 8은 As_Dia 열의 인덱스

        align_delegate = AlignDelegate(self.tableWidget)
        for icol in range(15):
            if icol != 8:  # As_Dia 열(8번)을 제외한 모든 열에 AlignDelegate 적용
                self.tableWidget.setItemDelegateForColumn(icol, align_delegate)

        for row in range(self.tableWidget.rowCount()):
            self.tableWidget.setItem(row, 8, QTableWidgetItem('13')) 

        for row in range(self.tableWidget.rowCount()):
            self.tableWidget.openPersistentEditor(self.tableWidget.item(row, 8))                

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
        layout.addLayout(self.hbox)

        layout.addWidget(self.tableWidget)
        layout.addStretch(1)

        # layout.setAlignment(Qt.AlignTop)

        self.setCentralWidget(widget)

        self.setWindowTitle('QTableWidget')
        self.setGeometry(300, 100, 1024, 400)
        self.show()

    def showforce(self,state):
        if state == Qt.Checked:
            boolhideforce = False
        else:
            boolhideforce = True
        self.tableWidget.setColumnHidden(1, boolhideforce)
        self.tableWidget.setColumnHidden(2, boolhideforce)
        self.tableWidget.setColumnHidden(3, boolhideforce)
        self.tableWidget.setColumnHidden(4, boolhideforce)

    def showsecinfo(self,state):
        if state == Qt.Checked:
            boolhidesec = False
        else:
            boolhidesec = True
        self.tableWidget.setColumnHidden(5, boolhidesec)
        self.tableWidget.setColumnHidden(6, boolhidesec)
        self.tableWidget.setColumnHidden(7, boolhidesec)

    def showbandrebar(self,state):
        if state == Qt.Checked:
            boolhideband = False
        else:
            boolhideband = True
        self.tableWidget.setColumnHidden(8, boolhideband)
        self.tableWidget.setColumnHidden(9, boolhideband)

    def showshearrebar(self,state):
        if state == Qt.Checked:
            boolhideshear = False
        else:
            boolhideshear = True
        self.tableWidget.setColumnHidden(10, boolhideshear)
        self.tableWidget.setColumnHidden(11, boolhideshear)
        self.tableWidget.setColumnHidden(12, boolhideshear)
        self.tableWidget.setColumnHidden(13, boolhideshear)

class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())