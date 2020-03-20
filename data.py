from os import getcwd, mkdir
from os.path import join

class Data:
	def __init__(self):
		self.QUEST_NAME = "Props264"
		self.EK_NUM = 1
		self.IDS = ["candles", "leds", ]
		self.ERP_NUM = [1, 4, -1, ]
		self.IP_END = 50
		self.BOARD = "megaatmega2560"
		self.GUARD = "#pragma once"
		self.CONFIGS = [
			{
				"MagnetLock": [["upper_door", "5",],],
				"SimpleLed":  [["illumination", "8"],],
				"ArdSensor":  [["reed", "2", "HIGH, 400"],],
				"Timer":	  [["music_publisher"],],
			},

			{
				"MagnetLock": [["exit_door", "A0",], ["snicth", "A1"]],
				"SimpleLed":  [["upper_led", "9"], ["snitch_led", "4"]],
				"ArdSensors": ["sensors", ["3, 7, 6,", "LOW, 100"],],
				"Timer":	  [["reseter"],],
			},
		]

	def get_board(self):
		return self.BOARD

	def get_guard(self):
		return self.GUARD

	def get_props_num(self):
		return len(self.IDS)

	def get_quest_name(self):
		return self.QUEST_NAME

	def get_ek(self):
		return self.EK_NUM

	def get_config(self):
		return self.CONFIGS

	def get_ids(self):
		return self.IDS

	def get_IP_end(self):
		return self.IP_END

	def get_erp_num(self):
		return self.ERP_NUM

	def get_circuit_name(self):
		name = f"{self.QUEST_NAME}"
		for i in self.IDS:
			name += "_" + i.capitalize()
		return name

	def get_work_dir(self):
		return join(getcwd(), self.get_circuit_name())


def work_dir_creator(data):	
	wd = data.get_work_dir()
	mkdir(wd)
	mkdir(join(wd, "src"))
	mkdir(join(wd, "lib"))
	mkdir(join(wd, "test"))


def s_open(f_name, data):
	path = join(data.get_work_dir(), f_name)
	try:
		return open(path, "x")
	except FileExistsError:
		print("file {f_name} already exists")
		exit()
