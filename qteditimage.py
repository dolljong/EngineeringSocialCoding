import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit
from PyQt5.QtGui import QTextCursor, QFont

class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1200, 800)

        mainLayout = QVBoxLayout()

        self.textEditor = QTextEdit()
        mainLayout.addWidget(self.textEditor)

        document = self.textEditor.document()
        cursor = QTextCursor(document)

        p1 = cursor.position() # returns int
        #self.textEditor.setStyleSheet('color:black;font-size:45px;')
        
        self.textEditor.setAcceptRichText(True)
        #self.textEditor.setFontPointSize(50)
        #fontvar = QFont("Fantasy",100,QFont.Bold)
        #self.textEditor.setCurrentFont(fontvar)
        
        #self.textEditor.setStyleSheet('color:red;font-size:45px;')
        #self.textEditor.setText('한줄 입력창입니다.')
        self.textEditor.setFontPointSize(30.0)
        #cursor.insertText('암거 구조계산서\n')
        self.textEditor.insertPlainText('암거 구조계산서\n')
        self.textEditor.setFontPointSize(11.0)
        self.textEditor.insertPlainText('1.설계기준\n')
        
        cursor.insertImage('calc.png')
        cursor.insertText('\n')
        #cursor.insertImage('simple_text.svg')
        #cursor.insertImage('2.svg')
        cursor.insertImage('wave-defs.svg')

        self.setLayout(mainLayout)
        
        #self.textEditor.setStyleSheet('color:black;font-size:20px;')
        self.textEditor.setFontPointSize(11.0)
        self.textEditor.insertPlainText('\n[표 1-1] 계산 결과 요약\n')
        
        headers = ["Number", "Name", "Surname"]
        rows = [["1", "Maik", "Mustermann"],
        ["2", "Tom", "Jerry"],
        ["3", "Jonny", "Brown"]]
        cursor = self.textEditor.textCursor()
        cursor.insertTable(len(rows) + 1, len(headers))
        for header in headers:
            cursor.insertText(header)
            cursor.movePosition(QTextCursor.NextCell)
            
        for row in rows:
            for value in row:
                cursor.insertText(str(value))
                cursor.movePosition(QTextCursor.NextCell)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = AppDemo()
    demo.show()
    sys.exit(app.exec_())