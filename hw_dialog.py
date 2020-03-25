from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class HWDialog(QDialog):

    def __init__(self, string_id, *args, **kwargs):
        super(HWDialog, self).__init__(*args, **kwargs)

        self.setWindowTitle(string_id)
        self.setGeometry(400, 400, 500, 300)
        main_lay = QGridLayout()

        self.maglock = QLineEdit(placeholderText="MagnetLock: name, pin; name, pin ...")
        self.simpleled = QLineEdit(placeholderText="SimpleLed: name, pin; name, pin ...")
        self.ardsensor = QLineEdit(
            placeholderText="ArdSensor: name, pin, param1, param2; name, pin, param1, param2 ...")
        self.timer = QLineEdit(placeholderText="Timer: name, name ...")
        self.ardsensors = QLineEdit(placeholderText="ArdSensors: name; pin1, pin2, pin3; params ")
        self.submit_button = QPushButton("submit")
        self.submit_button.clicked.connect(self.submitted)
        main_lay.addWidget(self.maglock)
        main_lay.addWidget(self.simpleled)
        main_lay.addWidget(self.ardsensor)
        main_lay.addWidget(self.timer)
        main_lay.addWidget(self.maglock)
        main_lay.addWidget(self.ardsensors)
        main_lay.addWidget(self.submit_button)
        self.setLayout(main_lay)

    # todo: use strategy for get_magnet_locks and get_simple_leds
    def get_magnet_locks(self):
        res = []
        for lock in self.maglock.text().strip().split(';'):
            res.append([x.strip() for x in lock.split(',')])
        return res

    def get_simple_leds(self):
        res = []
        for led in self.simpleled.text().strip().split(';'):
            res.append([x.strip() for x in led.split(',')])
        return res

    def get_ard_sensors(self):
        res = []
        # todo: make user friendly error msg
        try:
            for sen in self.ardsensor.text().strip().split(';'):
                params = ([x.strip() for x in sen.split(',')])              # expected: name, pin, LV, timeout
                res.append([params[0], params[1], params[2] + ', ' + params[3]])  # [["reed", "2", "HIGH, 400"],],
        except IndexError:
            self.ardsensor.clear()
        return res

    def get_timers(self):
        res = []
        timers = [x.strip() for x in self.timer.text().strip().split(',')]
        for timer in timers:
            res.append([timer, ])
        return res

    def get_array_ard_sensors(self):
        # # sensors, 7, 8, 9, LOW, 100 ->
        # ["sensors", ["3, 7, 6,", "LOW, 100"], ],
        res = []
        text = self.ardsensors.text().strip()
        if len(text) == 0:
            return res
        values = text.split(',')
        print()
        res.append(values[0])  # name
        pins = ""
        for i in values[1:-2]:
            pins += i + ', '
        params = values[-2] + ',' + values[-1]
        res.append([pins.strip(), params.strip(),])
        return res

    @pyqtSlot()
    def submitted(self):
        print(self.get_magnet_locks())
        print(self.get_simple_leds())
        print(self.get_ard_sensors())
        print(self.get_timers())
        print(self.get_array_ard_sensors())
        self.close()
