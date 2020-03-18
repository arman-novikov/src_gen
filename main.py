import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from builder import *

QUEST_NAME = "QUEST"
EK_NUM = 1
IDS = []
ERP_NUM = []
IP_END = 50
BOARD = "board"  # uno megaatmega2560
GUARD = "#pragma once"
CONFIGS = []


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Indestroom source generator'
        self.left = 300
        self.top = 300
        self.width = 400
        self.height = 300
        self.inp_height = 30
        self.initUI()
        self.data = Data()

    def initUI(self):
        centralWid = QWidget(self)
        self.setCentralWidget(centralWid)
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.defaultWidgetsLay = QGridLayout()
        self.defaultWidgetsLay.setAlignment(Qt.AlignTop)
        self.defaultInpsKeys = ["quest name", "EK number", "string id", "numbers in erp", "IP addr last byte"]
        self.defaultInps = {}

        i = 0
        for key in self.defaultInpsKeys:
            self.defaultInps[key] = QLineEdit(self, placeholderText=key)
            # self.defaultInps[key].move(20, 20 + self.inp_height * (i*1.5))
            self.defaultInps[key].resize(280, self.inp_height)
            self.defaultWidgetsLay.addWidget(self.defaultInps[key])
            i += 1

        self.hw_gen_mod = QCheckBox("generate hardware sources")
        self.defaultWidgetsLay.addWidget(self.hw_gen_mod)

        self.generate_btn = QPushButton('generate', self)
        self.generate_btn.move(self.width - 150, self.height - 50)

        self.radioLay = QHBoxLayout()
        self.megaRadioButton = QRadioButton("MEGA")
        self.megaRadioButton.setChecked(True)
        self.megaRadioButton.clicked.connect(self.megaRadioButtonclick)
        self.unoRadioButton = QRadioButton("UNO")
        self.unoRadioButton.clicked.connect(self.unoRadioButtonclick)
        self.radioLay.addWidget(self.megaRadioButton)
        self.radioLay.addWidget(self.unoRadioButton)
        self.defaultWidgetsLay.addLayout(self.radioLay, len(self.defaultInpsKeys) + 1, 0)

        self.generate_btn.clicked.connect(self.generate_btn_click)
        centralWid.setLayout(self.defaultWidgetsLay)
        self.show()

    @pyqtSlot()
    def generate_btn_click(self):
        try:
            self.data.QUEST_NAME = self.quest_name_inp.text()
            self.data.EK_NUM = int(self.ek_inp.text())
            #self.data.IDS =
            #self.data.ERP_NUM =
            #self.data.BOARD =
        except:
            print("generate_btn_click except")
            exit(-22)
        print(QUEST_NAME, EK_NUM)

    @pyqtSlot()
    def megaRadioButtonclick(self):
        self.data.BOARD = "megaatmega2560"
        self.unoRadioButton.setChecked(False)

    @pyqtSlot()
    def unoRadioButtonclick(self):
        self.data.BOARD = "uno"
        self.megaRadioButton.setChecked(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())