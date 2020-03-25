from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class HWDialog(QDialog):

    def __init__(self, string_id, *args, **kwargs):
        super(HWDialog, self).__init__(*args, **kwargs)

        self.setWindowTitle(string_id)
        self.setGeometry(400, 400, 500, 300)
        main_lay = QGridLayout()

        maglock = QLineEdit(placeholderText="MagnetLock: name, pin; name, pin...")
        simpleled = QLineEdit(placeholderText="SimpleLed: name, pin; name, pin...")
        ardsensor = QLineEdit(placeholderText="ArdSensor: name, pin, params; name, pin, params...")
        timer = QLineEdit(placeholderText="Timer: name, name ...")
        ardsensors = QLineEdit(placeholderText="ArdSensors: name; pin1, pin2, pin3; params ")
        submit_button = QPushButton("submit")
        submit_button.clicked.connect(self.submitted)
        main_lay.addWidget(maglock)
        main_lay.addWidget(simpleled)
        main_lay.addWidget(ardsensor)
        main_lay.addWidget(timer)
        main_lay.addWidget(maglock)
        main_lay.addWidget(ardsensors)
        main_lay.addWidget(submit_button)
        self.setLayout(main_lay)

    @pyqtSlot()
    def submitted(self):
        self.close()
