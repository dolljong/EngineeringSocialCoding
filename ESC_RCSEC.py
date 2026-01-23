import sys
import json
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from sec_back_ver031 import Sec_back
from sec_front_ver031 import (get_moment_text, get_shear_text, get_service_text, get_full_calc_text,
                              wsinit, momentexcelout, shearexcelout, serviceexcelout)
import xlwings as xw


class CalcViewerDialog(QDialog):
    """계산과정을 보여주는 뷰어 다이얼로그"""
    def __init__(self, parent=None, calc_data=None, section_name=""):
        super().__init__(parent)
        self.calc_data = calc_data
        self.section_name = section_name
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f'계산과정 - {self.section_name}')
        self.setGeometry(100, 100, 800, 700)

        layout = QVBoxLayout(self)

        # 탭 위젯
        tabs = QTabWidget()

        # 전체 계산과정 탭
        self.full_text = QTextEdit()
        self.full_text.setReadOnly(True)
        self.full_text.setFont(QFont('Consolas', 10))
        tabs.addTab(self.full_text, '전체')

        # 휨모멘트 탭
        self.moment_text = QTextEdit()
        self.moment_text.setReadOnly(True)
        self.moment_text.setFont(QFont('Consolas', 10))
        tabs.addTab(self.moment_text, '휨모멘트')

        # 전단력 탭
        self.shear_text = QTextEdit()
        self.shear_text.setReadOnly(True)
        self.shear_text.setFont(QFont('Consolas', 10))
        tabs.addTab(self.shear_text, '전단력')

        # 사용성 탭
        self.service_text = QTextEdit()
        self.service_text.setReadOnly(True)
        self.service_text.setFont(QFont('Consolas', 10))
        tabs.addTab(self.service_text, '사용성')

        layout.addWidget(tabs)

        # 버튼 영역
        btn_layout = QHBoxLayout()

        copy_btn = QPushButton('복사')
        copy_btn.clicked.connect(self.copy_to_clipboard)
        btn_layout.addWidget(copy_btn)

        save_btn = QPushButton('텍스트 저장')
        save_btn.clicked.connect(self.save_to_file)
        btn_layout.addWidget(save_btn)

        btn_layout.addStretch()

        close_btn = QPushButton('닫기')
        close_btn.clicked.connect(self.close)
        btn_layout.addWidget(close_btn)

        layout.addLayout(btn_layout)

        # 계산 데이터가 있으면 표시
        if self.calc_data:
            self.display_calc(self.calc_data)

    def display_calc(self, calc):
        """계산 결과를 표시"""
        self.full_text.setText(get_full_calc_text(calc))
        self.moment_text.setText(get_moment_text(calc))
        self.shear_text.setText(get_shear_text(calc))
        self.service_text.setText(get_service_text(calc))

    def copy_to_clipboard(self):
        """현재 탭의 내용을 클립보드에 복사"""
        clipboard = QApplication.clipboard()
        clipboard.setText(self.full_text.toPlainText())
        QMessageBox.information(self, '복사 완료', '계산과정이 클립보드에 복사되었습니다.')

    def save_to_file(self):
        """텍스트 파일로 저장"""
        filename, _ = QFileDialog.getSaveFileName(
            self, '저장', f'{self.section_name}_계산서.txt', 'Text Files (*.txt)'
        )
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.full_text.toPlainText())
            QMessageBox.information(self, '저장 완료', f'파일이 저장되었습니다:\n{filename}')


class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight


class CopyPasteTableWidget(QTableWidget):
    """복사/붙여넣기 기능이 추가된 QTableWidget"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def keyPressEvent(self, event):
        if event.matches(QtGui.QKeySequence.Copy):
            self.copy_selection()
        elif event.matches(QtGui.QKeySequence.Paste):
            self.paste_clipboard()
        elif event.matches(QtGui.QKeySequence.Cut):
            self.cut_selection()
        elif event.key() == Qt.Key_Delete:
            self.delete_selection()
        else:
            super().keyPressEvent(event)

    def copy_selection(self):
        """선택된 셀들을 클립보드에 복사 (탭으로 구분, Excel 호환)"""
        selection = self.selectedRanges()
        if not selection:
            return

        # 선택 영역의 범위 계산
        min_row = min(r.topRow() for r in selection)
        max_row = max(r.bottomRow() for r in selection)
        min_col = min(r.leftColumn() for r in selection)
        max_col = max(r.rightColumn() for r in selection)

        # 선택된 셀들의 텍스트를 수집
        rows = []
        for row in range(min_row, max_row + 1):
            row_data = []
            for col in range(min_col, max_col + 1):
                item = self.item(row, col)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append('')
            rows.append('\t'.join(row_data))

        # 클립보드에 복사
        clipboard = QApplication.clipboard()
        clipboard.setText('\n'.join(rows))

    def cut_selection(self):
        """선택된 셀들을 잘라내기 (복사 후 삭제)"""
        self.copy_selection()
        self.delete_selection()

    def delete_selection(self):
        """선택된 셀들의 내용 삭제"""
        for item in self.selectedItems():
            item.setText('')

    def paste_clipboard(self):
        """클립보드의 내용을 현재 셀부터 붙여넣기"""
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        if not text:
            return

        # 현재 선택된 셀 위치
        selection = self.selectedRanges()
        if not selection:
            current_row = self.currentRow()
            current_col = self.currentColumn()
        else:
            current_row = selection[0].topRow()
            current_col = selection[0].leftColumn()

        if current_row < 0 or current_col < 0:
            return

        # 클립보드 텍스트를 행/열로 분리
        rows = text.split('\n')
        for i, row_text in enumerate(rows):
            if current_row + i >= self.rowCount():
                break
            cols = row_text.split('\t')
            for j, cell_text in enumerate(cols):
                if current_col + j >= self.columnCount():
                    break
                # 셀에 값 설정
                item = self.item(current_row + i, current_col + j)
                if item is None:
                    item = QTableWidgetItem()
                    self.setItem(current_row + i, current_col + j, item)
                item.setText(cell_text.strip())


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
        self.open_action = QAction("Open")
        self.open_action.triggered.connect(self.load_file)
        self.save_action = QAction("Save")
        self.save_action.triggered.connect(self.save_file)
        self.quit_action = QAction("Quit")
        self.quit_action.triggered.connect(self.close)
        
        # calc menu actions
        self.calc_action = QAction("Calc")
        self.calc_action.triggered.connect(self.calculate)

        # view menu actions
        self.view_action = QAction("View Calc")
        self.view_action.triggered.connect(self.view_calc)
        self.export_action = QAction("Export to Excel")
        self.export_action.triggered.connect(self.export_to_excel)

        # help menu action
        self.doc_action = QAction("Documentation")
        self.release_action = QAction("Release Notes")
        self.license_action = QAction("View License")

        # file menu
        file_menu = self.menubar.addMenu("파일")
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addSeparator()
        file_menu.addAction(self.quit_action)
        
        # Calculate menu
        calc_menu = self.menubar.addMenu("Calc")
        calc_menu.addAction(self.calc_action)

        # View menu
        view_menu = self.menubar.addMenu("View")
        view_menu.addAction(self.view_action)
        view_menu.addSeparator()
        view_menu.addAction(self.export_action)

        # help menu
        help_menu = self.menubar.addMenu("도움말")
        help_menu.addAction(self.doc_action)
        help_menu.addAction(self.release_action)
        help_menu.addAction(self.license_action)
        
        calcAction = QAction(QIcon('calc.png'), 'Calc', self)
        calcAction.setStatusTip('Calculate Sections')
        calcAction.triggered.connect(self.calculate)

        viewAction = QAction(QIcon('view.png'), 'View', self)
        viewAction.setStatusTip('View Calculation Details')
        viewAction.triggered.connect(self.view_calc)

        exportAction = QAction(QIcon('excel.png'), 'Excel', self)
        exportAction.setStatusTip('Export to Excel')
        exportAction.triggered.connect(self.export_to_excel)

        self.toolbar = self.addToolBar('Tools')
        self.toolbar.addAction(calcAction)
        self.toolbar.addAction(viewAction)
        self.toolbar.addAction(exportAction)
        
        
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

        self.tableWidget1 = CopyPasteTableWidget()
        self.tableWidget = CopyPasteTableWidget()
        
        
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
        self.tableWidget.setColumnCount(18)
        self.tableWidget.setHorizontalHeaderLabels(['Name','Mu\n(kN.m)','Vu\n(kN)','Nu\n(kN)', 'Ms\n(kN.m)','H\n(mm)','B\n(mm)','Dc\n(mm)', 'As_Dia\n(mm)', 'As_Num\n(EA)',
                                                    'δ', 'Av_Dia\n(mm)','Av_Leg\n(EA)', 'Av_Space\n(mm)','As_req\n(mm2)','As_used\n(mm2)','As_used\n/As_req',''])
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
        for icol in range(17):  # 0-16까지 (As_used, As_used/As_req 포함)
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

    def calculate(self):
        """테이블 데이터를 읽어 Sec_back으로 계산 수행"""
        try:
            # 재료 데이터 읽기 (tableWidget1)
            fck = float(self.tableWidget1.item(0, 0).text())
            fy = float(self.tableWidget1.item(0, 1).text())
            Oc = float(self.tableWidget1.item(0, 2).text())
            Os = float(self.tableWidget1.item(0, 3).text())

            datalist = [fck, fy]
            datalist1 = [Oc, Os]

            # 각 행에 대해 계산 수행
            for row in range(self.tableWidget.rowCount()):
                # 첫 번째 열(Name)이 비어있으면 건너뛰기
                name_item = self.tableWidget.item(row, 0)
                if name_item is None or name_item.text().strip() == '':
                    continue

                # 데이터 읽기 (빈 셀은 0으로 처리)
                def get_value(row, col, default=0):
                    item = self.tableWidget.item(row, col)
                    if item is None or item.text().strip() == '':
                        return default
                    try:
                        return float(item.text())
                    except ValueError:
                        return default

                # 부재력 데이터
                Mu = get_value(row, 1)
                Vu = get_value(row, 2)
                Nu = get_value(row, 3)
                Ms = get_value(row, 4)

                # 단면 데이터
                H = get_value(row, 5)
                B = get_value(row, 6)
                Dc = get_value(row, 7)

                # 휨철근 데이터 (1단만 GUI에서 입력)
                As_Dia = get_value(row, 8, 13)
                As_Num = get_value(row, 9)

                # 모멘트 재분배율
                delta = get_value(row, 10, 1)

                # 전단철근 데이터
                Av_Dia = get_value(row, 11, 10)
                Av_Leg = get_value(row, 12, 2)
                Av_Space = get_value(row, 13, 300)

                # 유효성 검사
                if H <= 0 or B <= 0:
                    continue

                # 백엔드 파라미터 구성
                datalist2 = [H, B]
                # 휨철근: 1단만 사용, 2단/3단은 0
                datalist3 = [int(As_Dia), int(As_Num), Dc, 0, 0, 0, 0, 0, 0]
                # 전단철근: sg=3(자동), seta=0, αv=90도
                datalist4 = [int(Av_Dia), int(Av_Leg), Av_Space, 3, 0, 90]
                # 부재력: Ms1=Ms5=Ms, crid=1
                datalist5 = [Mu, Vu, Nu, Ms, Ms, 1]

                # Sec_back 객체 생성 및 계산
                sec = Sec_back(datalist, datalist1, datalist2, datalist3, datalist4, datalist5)
                sec.δ = delta
                sec.calmoment()
                sec.calshear()

                # 결과 표시
                As_req = sec.Asreq
                As_used = sec.Asuse
                if As_req > 0:
                    ratio = As_used / As_req
                else:
                    ratio = 0

                self.tableWidget.setItem(row, 14, QTableWidgetItem(f'{As_req:.1f}'))
                self.tableWidget.setItem(row, 15, QTableWidgetItem(f'{As_used:.1f}'))
                self.tableWidget.setItem(row, 16, QTableWidgetItem(f'{ratio:.2f}'))

            self.statusBar().showMessage('계산 완료')

        except Exception as e:
            self.statusBar().showMessage(f'계산 오류: {str(e)}')
            print(f'Error: {e}')

    def view_calc(self):
        """선택한 행의 계산과정을 뷰어로 표시"""
        try:
            # 선택된 행 확인
            selected_rows = self.tableWidget.selectionModel().selectedRows()
            if not selected_rows:
                # 선택된 행이 없으면 현재 행 사용
                current_row = self.tableWidget.currentRow()
                if current_row < 0:
                    QMessageBox.warning(self, '경고', '계산과정을 볼 행을 선택하세요.')
                    return
                row = current_row
            else:
                row = selected_rows[0].row()

            # 해당 행에 데이터가 있는지 확인
            name_item = self.tableWidget.item(row, 0)
            if name_item is None or name_item.text().strip() == '':
                QMessageBox.warning(self, '경고', '선택한 행에 데이터가 없습니다.')
                return

            section_name = name_item.text()

            # 재료 데이터 읽기
            fck = float(self.tableWidget1.item(0, 0).text())
            fy = float(self.tableWidget1.item(0, 1).text())
            Oc = float(self.tableWidget1.item(0, 2).text())
            Os = float(self.tableWidget1.item(0, 3).text())

            datalist = [fck, fy]
            datalist1 = [Oc, Os]

            # 데이터 읽기 함수
            def get_value(row, col, default=0):
                item = self.tableWidget.item(row, col)
                if item is None or item.text().strip() == '':
                    return default
                try:
                    return float(item.text())
                except ValueError:
                    return default

            # 부재력 데이터
            Mu = get_value(row, 1)
            Vu = get_value(row, 2)
            Nu = get_value(row, 3)
            Ms = get_value(row, 4)

            # 단면 데이터
            H = get_value(row, 5)
            B = get_value(row, 6)
            Dc = get_value(row, 7)

            # 휨철근 데이터
            As_Dia = get_value(row, 8, 13)
            As_Num = get_value(row, 9)

            # 모멘트 재분배율
            delta = get_value(row, 10, 1)

            # 전단철근 데이터
            Av_Dia = get_value(row, 11, 10)
            Av_Leg = get_value(row, 12, 2)
            Av_Space = get_value(row, 13, 300)

            # 유효성 검사
            if H <= 0 or B <= 0:
                QMessageBox.warning(self, '경고', '단면 치수가 유효하지 않습니다.')
                return

            # 백엔드 파라미터 구성
            datalist2 = [H, B]
            datalist3 = [int(As_Dia), int(As_Num), Dc, 0, 0, 0, 0, 0, 0]
            datalist4 = [int(Av_Dia), int(Av_Leg), Av_Space, 3, 0, 90]
            datalist5 = [Mu, Vu, Nu, Ms, Ms, 1]

            # Sec_back 객체 생성 및 계산
            sec = Sec_back(datalist, datalist1, datalist2, datalist3, datalist4, datalist5)
            sec.δ = delta
            sec.calmoment()
            sec.calshear()
            sec.calservice()

            # 뷰어 다이얼로그 표시
            viewer = CalcViewerDialog(self, sec, section_name)
            viewer.exec_()

        except Exception as e:
            QMessageBox.critical(self, '오류', f'계산과정 표시 오류: {str(e)}')
            print(f'Error: {e}')

    def export_to_excel(self):
        """계산결과를 Excel로 내보내기 (xlwings + sec_front_ver031 함수 사용)"""
        try:
            # 파일 저장 경로 선택
            filename, _ = QFileDialog.getSaveFileName(
                self, '저장', 'RC_Section_Calc.xlsx', 'Excel Files (*.xlsx)'
            )
            if not filename:
                return

            # xlwings로 새 워크북 생성
            wb = xw.Book()

            # 재료 데이터 읽기
            fck = float(self.tableWidget1.item(0, 0).text())
            fy = float(self.tableWidget1.item(0, 1).text())
            Oc = float(self.tableWidget1.item(0, 2).text())
            Os = float(self.tableWidget1.item(0, 3).text())

            datalist = [fck, fy]
            datalist1 = [Oc, Os]

            lastsheetname = wb.sheets[0].name
            first_section = True

            for row in range(self.tableWidget.rowCount()):
                name_item = self.tableWidget.item(row, 0)
                if name_item is None or name_item.text().strip() == '':
                    continue

                section_name = name_item.text()

                def get_value(row, col, default=0):
                    item = self.tableWidget.item(row, col)
                    if item is None or item.text().strip() == '':
                        return default
                    try:
                        return float(item.text())
                    except ValueError:
                        return default

                Mu = get_value(row, 1)
                Vu = get_value(row, 2)
                Nu = get_value(row, 3)
                Ms = get_value(row, 4)
                H = get_value(row, 5)
                B = get_value(row, 6)
                Dc = get_value(row, 7)
                As_Dia = get_value(row, 8, 13)
                As_Num = get_value(row, 9)
                delta = get_value(row, 10, 1)
                Av_Dia = get_value(row, 11, 10)
                Av_Leg = get_value(row, 12, 2)
                Av_Space = get_value(row, 13, 300)

                if H <= 0 or B <= 0:
                    continue

                datalist2 = [H, B]
                datalist3 = [int(As_Dia), int(As_Num), Dc, 0, 0, 0, 0, 0, 0]
                datalist4 = [int(Av_Dia), int(Av_Leg), Av_Space, 3, 0, 90]
                datalist5 = [Mu, Vu, Nu, Ms, Ms, 1]

                # Sec_back 객체 생성 및 계산
                sec = Sec_back(datalist, datalist1, datalist2, datalist3, datalist4, datalist5)
                sec.δ = delta
                sec.calmoment()
                sec.calshear()
                sec.calservice()

                # 새 시트 생성 (시트명은 30자 제한)
                sheet_name = section_name[:30]
                wsout = wb.sheets.add(sheet_name, after=lastsheetname)

                # sec_front_ver031의 함수들 사용
                wsinit(wsout)
                momentexcelout(sec, wsout)
                shearexcelout(sec, wsout)
                serviceexcelout(sec, wsout)

                lastsheetname = sheet_name
                first_section = False

            # 기본 시트 삭제 (데이터가 있는 경우)
            if not first_section:
                try:
                    wb.sheets[0].delete()
                except:
                    pass

            # 파일 저장 및 닫기
            wb.save(filename)
            wb.close()

            QMessageBox.information(self, '저장 완료', f'Excel 파일이 저장되었습니다:\n{filename}')
            self.statusBar().showMessage(f'Excel 저장 완료: {filename}')

        except Exception as e:
            QMessageBox.critical(self, '오류', f'Excel 저장 오류: {str(e)}')
            print(f'Error: {e}')

    def save_file(self):
        """입력 데이터를 .rcsec 파일로 저장"""
        try:
            filename, _ = QFileDialog.getSaveFileName(
                self, '저장', '', 'RC Section Files (*.rcsec)'
            )
            if not filename:
                return

            if not filename.endswith('.rcsec'):
                filename += '.rcsec'

            # 재료 데이터 수집
            material = {
                "fck": float(self.tableWidget1.item(0, 0).text()) if self.tableWidget1.item(0, 0) else 35,
                "fy": float(self.tableWidget1.item(0, 1).text()) if self.tableWidget1.item(0, 1) else 400,
                "Oc": float(self.tableWidget1.item(0, 2).text()) if self.tableWidget1.item(0, 2) else 0.65,
                "Os": float(self.tableWidget1.item(0, 3).text()) if self.tableWidget1.item(0, 3) else 0.7
            }

            # 부재 데이터 수집
            sections = []
            for row in range(self.tableWidget.rowCount()):
                name_item = self.tableWidget.item(row, 0)
                if name_item is None or name_item.text().strip() == '':
                    continue

                def get_value(row, col, default=0):
                    item = self.tableWidget.item(row, col)
                    if item is None or item.text().strip() == '':
                        return default
                    try:
                        return float(item.text())
                    except ValueError:
                        return default

                section = {
                    "name": name_item.text(),
                    "forces": {
                        "Mu": get_value(row, 1),
                        "Vu": get_value(row, 2),
                        "Nu": get_value(row, 3),
                        "Ms": get_value(row, 4)
                    },
                    "geometry": {
                        "H": get_value(row, 5),
                        "B": get_value(row, 6),
                        "Dc": get_value(row, 7)
                    },
                    "flexure_rebar": {
                        "dia": get_value(row, 8, 13),
                        "num": get_value(row, 9)
                    },
                    "delta": get_value(row, 10, 1),
                    "shear_rebar": {
                        "dia": get_value(row, 11, 10),
                        "leg": get_value(row, 12, 2),
                        "space": get_value(row, 13, 300)
                    }
                }
                sections.append(section)

            # JSON 구조 생성
            data = {
                "version": "1.0",
                "material": material,
                "sections": sections
            }

            # 파일 저장
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            QMessageBox.information(self, '저장 완료', f'파일이 저장되었습니다:\n{filename}')
            self.statusBar().showMessage(f'저장 완료: {filename}')

        except Exception as e:
            QMessageBox.critical(self, '오류', f'파일 저장 오류: {str(e)}')
            print(f'Error: {e}')

    def load_file(self):
        """".rcsec 파일에서 데이터 불러오기"""
        try:
            filename, _ = QFileDialog.getOpenFileName(
                self, '열기', '', 'RC Section Files (*.rcsec)'
            )
            if not filename:
                return

            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 버전 체크 (향후 확장 대비)
            version = data.get("version", "1.0")

            # 재료 데이터 로드
            material = data.get("material", {})
            self.tableWidget1.setItem(0, 0, QTableWidgetItem(str(material.get("fck", 35))))
            self.tableWidget1.setItem(0, 1, QTableWidgetItem(str(material.get("fy", 400))))
            self.tableWidget1.setItem(0, 2, QTableWidgetItem(str(material.get("Oc", 0.65))))
            self.tableWidget1.setItem(0, 3, QTableWidgetItem(str(material.get("Os", 0.7))))

            # 기존 테이블 데이터 클리어
            for row in range(self.tableWidget.rowCount()):
                for col in range(self.tableWidget.columnCount()):
                    self.tableWidget.setItem(row, col, QTableWidgetItem(''))

            # 부재 데이터 로드
            sections = data.get("sections", [])
            for row, section in enumerate(sections):
                if row >= self.tableWidget.rowCount():
                    break

                self.tableWidget.setItem(row, 0, QTableWidgetItem(section.get("name", "")))

                forces = section.get("forces", {})
                self.tableWidget.setItem(row, 1, QTableWidgetItem(str(forces.get("Mu", 0))))
                self.tableWidget.setItem(row, 2, QTableWidgetItem(str(forces.get("Vu", 0))))
                self.tableWidget.setItem(row, 3, QTableWidgetItem(str(forces.get("Nu", 0))))
                self.tableWidget.setItem(row, 4, QTableWidgetItem(str(forces.get("Ms", 0))))

                geometry = section.get("geometry", {})
                self.tableWidget.setItem(row, 5, QTableWidgetItem(str(geometry.get("H", 0))))
                self.tableWidget.setItem(row, 6, QTableWidgetItem(str(geometry.get("B", 0))))
                self.tableWidget.setItem(row, 7, QTableWidgetItem(str(geometry.get("Dc", 0))))

                flexure = section.get("flexure_rebar", {})
                self.tableWidget.setItem(row, 8, QTableWidgetItem(str(int(flexure.get("dia", 13)))))
                self.tableWidget.setItem(row, 9, QTableWidgetItem(str(flexure.get("num", 0))))

                self.tableWidget.setItem(row, 10, QTableWidgetItem(str(section.get("delta", 1))))

                shear = section.get("shear_rebar", {})
                self.tableWidget.setItem(row, 11, QTableWidgetItem(str(int(shear.get("dia", 10)))))
                self.tableWidget.setItem(row, 12, QTableWidgetItem(str(shear.get("leg", 2))))
                self.tableWidget.setItem(row, 13, QTableWidgetItem(str(shear.get("space", 300))))

            QMessageBox.information(self, '불러오기 완료', f'파일을 불러왔습니다:\n{filename}')
            self.statusBar().showMessage(f'불러오기 완료: {filename}')

        except json.JSONDecodeError as e:
            QMessageBox.critical(self, '오류', f'파일 형식 오류: {str(e)}')
        except Exception as e:
            QMessageBox.critical(self, '오류', f'파일 불러오기 오류: {str(e)}')
            print(f'Error: {e}')

class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())