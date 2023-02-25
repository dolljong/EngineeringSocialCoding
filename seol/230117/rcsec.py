from PyQt5 import uic
from PyQt5.QtWidgets import *

class TableWidget(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("rcsec.ui",self)

        self.show()

if __name__ == "__main__":
    app = QApplication([])
    popup = TableWidget()
    popup.show()
    app.exec_()