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
        central_wid = QWidget(self)
        self.setCentralWidget(central_wid)
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.defaultWidgetsLay = QGridLayout()
        self.defaultWidgetsLay.setAlignment(Qt.AlignTop)
        self.defaultInpsKeys = ["quest name", "EK number", "string ids", "numbers in erp", "IP addr last byte"]
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
        central_wid.setLayout(self.defaultWidgetsLay)
        self.show()

    @pyqtSlot()
    def generate_btn_click(self):
        if self.default_inputs_check() is False:
            return
        self.data.CONFIGS = []  # no gui support yet
        try:
            build(self.data)
        except FileExistsError:
            self.error_msg("dir error", "directory already exists")
            return
        QMessageBox.about(self, "Status", "ok")

    @pyqtSlot()
    def megaRadioButtonclick(self):
        self.data.BOARD = "megaatmega2560"
        self.unoRadioButton.setChecked(False)

    @pyqtSlot()
    def unoRadioButtonclick(self):
        self.data.BOARD = "uno"
        self.megaRadioButton.setChecked(False)

    def default_inputs_check(self):
        self.data.QUEST_NAME = self.defaultInps['quest name'].text()
        if len(self.data.QUEST_NAME) == 0:
            self.error_msg("quest name", "quest name is empty")
            return False

        self.data.IDS = self.defaultInps['string ids'].text().split(' ')
        try:
            self.data.EK_NUM = int(self.defaultInps["EK number"].text())
        except (ValueError, TypeError):
            self.error_msg("EK number", "1 decimal value is expected")
            return False
        try:
            self.data.ERP_NUM = [
                int(i) for i in self.defaultInps['numbers in erp'].text().split(' ')
            ]
        except (ValueError, TypeError):
            self.error_msg("numbers in erp", "use decimal numbers splitted with spaces")
            return False
        try:
            self.data.IP_END = int(self.defaultInps['IP addr last byte'].text())
        except (ValueError, TypeError):
            self.error_msg("IP addr last byte", "1 decimal value is expected")
            return False
        if self.unoRadioButton.isChecked():
            self.data.BOARD = "uno"
        return True

    @staticmethod
    def error_msg(topic, details="check your input"):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(topic)
        msg.setInformativeText(details)
        msg.setWindowTitle(topic)
        msg.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())