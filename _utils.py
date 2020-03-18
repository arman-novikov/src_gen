QUEST_NAME = "Props264"
EK_NUM = 1
IDS = ["candles", "leds",]
ERP_NUM = [1,4,-1,]
IP_END = 50
BOARD = "megaatmega2560" # uno megaatmega2560
#########################################
		#	ADVANCED	#
CONFIGS = [
	{
		"MagnetLock": [["upper_door", "5",],],
		#"SimpleLed":  [["illumination", "8"],],
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
# CONFIGS	= [] # uncomment it if no CONFIGS are needed
#########################################
from os import getcwd, mkdir
from os.path import join

GUARD = "#pragma once"
PROPS_NUM = len(ERP_NUM)


def get_board():
	return BOARD


def get_guard():
	return GUARD


def get_props_num():
	return PROPS_NUM


def get_questName():
	return QUEST_NAME


def get_ek():
	return EK_NUM


def get_config():
	return CONFIGS


def get_ids():
	return IDS


def get_IP_end():
	return IP_END


def get_erp_num():
	return ERP_NUM


def get_circuit_name():
	name = f"{QUEST_NAME}"
	for i in IDS:
		name += "_" + i.capitalize()
	return name


def get_work_dir():
	return join(getcwd(), get_circuit_name())


def work_dir_creator():	
	wd = get_work_dir()
	try:
		mkdir(wd)
		mkdir(join(wd, "src"))
		mkdir(join(wd, "lib"))
		mkdir(join(wd, "test"))
	except FileExistsError:
		print(f"directory already exists")


def s_open(f_name):
	path = join(get_work_dir(), f_name)
	try:
		return open(path, "x")
	except FileExistsError:
		print("file {f_name} already exists")
		exit()
