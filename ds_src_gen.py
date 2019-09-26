QUEST_NAME = "Props264"
EK_NUM = 1
IDS = ["candles", "leds",]
ERP_NUM = [1,4,-1,]
IP_END = 51
#########################################
		#	ADVANCED	#
CONFIGS	= []
CONFIGS = [
	{
		"MagnetLock": [["upper_door", "5",],],
		"SimpleLed":  [["illumination", "8"],],
		"ArdSensor":  [["reed", "2", "HIGH, 400"],],
		"Timer":	  [["music_publisher"],],
	},

	{
		"MagnetLock": [["exit_door", "A0",], ["snicth", "A1"]],
		"SimpleLed":  [["upper_led", "9"], ["snitch_led", "4"]],
		"ArdSensors": ["sensors", ["3, 7, 6,", "HIGH, 400"],],
		"Timer":	  [["reseter"],],
	},
]
#########################################
from os import getcwd, mkdir
from os.path import join

GUARD = "#pragma once"
PROPS_NUM = len(ERP_NUM)

def get_circuit_name():
	name = f"{QUEST_NAME}_EK{EK_NUM}"
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


def pin_declarator(prop_num):
	PIN_DEC = "  constexpr uint8_t {}_PIN = {};\n"
	PINS_DEC = "  constexpr uint8_t {}_PINS${}@ = {{\n    {}  \n  }};\n"
	res = ""
	prop_dict = {}
	try:
		prop_dict = CONFIGS[prop_num]
	except IndexError:
		return res

	try:
		maglocks = prop_dict["MagnetLock"]
		for i in maglocks:
			res += PIN_DEC.format(i[0].upper(), i[1])
	except KeyError:
		pass

	try:
		leds = prop_dict["SimpleLed"]
		for i in leds:
			res += PIN_DEC.format(i[0].upper(), i[1])
	except KeyError:
		pass

	try:
		ardsen = prop_dict["ArdSensor"]
		for i in ardsen:
			res += PIN_DEC.format(i[0].upper(), i[1])
	except KeyError:
		pass

	try:
		ardsens = prop_dict["ArdSensors"]
		pins = ardsens[1][0]
		pins_num = pins.count(",")
		name = ardsens[0].upper()
		count_name = name + "_PINS_COUNT"
		res += f"  constexpr uint8_t {count_name} = {pins_num};\n"
		res += PINS_DEC.format(name, count_name, pins)
	except KeyError:
		pass
	return res.replace("$", "[").replace("@","]").replace("\'","")


def config_creator():
	f = s_open(join("src","config.h"))
	content = f"""{GUARD}
#include <Arduino.h>\n
constexpr char CIRCUIT_NAME[] = \"{get_circuit_name()}\";
constexpr byte IP_ENDING = {str(IP_END)};
constexpr bool UPLOAD_BOOT_INFO = true;\n
"""
	for i in range(PROPS_NUM):
		try:
			CONFS = pin_declarator(i);
			content += f"namespace {IDS[i]}_ns {{\n{CONFS}\n}}\n\n"
		except IndexError:
			pass
	f.write(content)


def common_creator():
	f = s_open(join("src","common.h"))
	content = f"""{GUARD}
#include <ds_console.h>
#include <ds_mqtt_manager.h>
#include <ds_wdt.h>
#include <ds_bootloader.h>
#include \"config.h\"

enum {{{[i.upper() + "_STATE_POS" for i in IDS]}}};
"""	
	content += f"""
constexpr size_t PROPS_NUM = {PROPS_NUM}U;
constexpr int props_num_in_ERP$PROPS_NUM@ = {{{[str(i) for i in ERP_NUM]}}};
"""	
	content = content.replace("-1", "ds_MQTT::NOT_SHOW")
	
	strids = ""
	for i in range(1, PROPS_NUM+1):
		try:
			strids += f"\nconstexpr char PROP_{str(i)}_STRID$@  = \"{IDS[i-1]}\";"
		except IndexError:
			pass
	
	content += strids
	names = []
	for i in range(1, PROPS_NUM+1):
		try:
			void = IDS[i-1]
			names.append(f"PROP_{str(i)}_STRID")
		except IndexError:
			names.append("nullptr")
	content += f"""
const char *propsNames$PROPS_NUM@ = {{{[i for i in names]}}};
"""
	cbs = []
	for i in IDS:
		cbs.append([f"{i}_onActivate", f"{i}_onFinish"])

	counter = -1
	for i in cbs:
		counter += 1
		content += f"""
void {i[0]}();
void {i[1]}();
prop_CBs_t  {IDS[counter]}_cbs = {{{i[0]}, {i[1]}, ds_MQTT::reset}};
"""
	content += "\nprops_CBs_t props_cbs$PROPS_NUM@ = {"
	for i in range(PROPS_NUM):
		try:
			content += f"&{IDS[i]}_cbs, " 
		except IndexError:
			content += "nullptr, "
	content += "};\n\n"

	states = []
	for i in range(PROPS_NUM):
		try:
			states.append(f"{IDS[i]}_state")
		except IndexError:
			pass
	for i in states:
		content += f"prop_state_t {i} = {{0}};\n"

	content += "props_states_t props_states$PROPS_NUM@ = {"
	for i in range(PROPS_NUM):
		try:
			content += states[i] + ", "
		except IndexError:
			content += "nullptr, "
	content += "};\n\n"

	for i in ["'","[", "]",]:
		content = content.replace(i, "")	

	content += """
Console *console;

void on_er_start()
{
  console->println(F("ER: Start"));
}

typedef  MQTT_manager<
  PROPS_NUM, CIRCUIT_NAME,
  propsNames, props_num_in_ERP,
  on_er_start, ds_MQTT::reset, props_cbs
> mqtt_manager_t;

mqtt_manager_t *mqtt_manager;

void common_routine_init()
{
  if (UPLOAD_BOOT_INFO)
    bootloader_init(IP_ENDING);

  console = new Console(CIRCUIT_NAME);
  mqtt_manager = new mqtt_manager_t(console, IP_ENDING);
  Serial.begin(115200);
  resetServer_init();  
}

void common_routine()
{
  mqtt_manager->routine(props_states);
  console->check();
  wdTimer_check();
  resetServer_check(console);
}
"""
	content = content.replace("$", "[").replace("@","]")
	f.write(content)


def obj_declarator(prop_num):
	OBJ = "{} *{};\n"
	OBJS = "{} *{}${}@;\n"
	res = ""
	prop_dict = {}
	try:
		prop_dict = CONFIGS[prop_num]
	except IndexError:
		return res
	try:
		maglocks = prop_dict["MagnetLock"]
		for i in maglocks:
			res += OBJ.format("MagnetLock", i[0])
	except KeyError:
		pass

	try:
		leds = prop_dict["SimpleLed"]
		for i in leds:
			res += OBJ.format("SimpleLed", i[0])
	except KeyError:
		pass

	try:
		ardsen = prop_dict["ArdSensor"]
		for i in ardsen:
			res += OBJ.format("ArdSensor", i[0])
	except KeyError:
		pass	

	try:
		ardsens = prop_dict["ArdSensors"]
		pins = ardsens[1][0]
		name = ardsens[0]
		pins_num = f"{IDS[prop_num]}_ns::{name.upper()}_PINS_COUNT"
		res += OBJS.format("ArdSensor", ardsens[0], pins_num)
	except KeyError:
		pass

	try:
		timer = prop_dict["Timer"]
		for i in timer:
			res += OBJ.format("Timer", i[0])
	except KeyError:
		pass

	return res.replace("$", "[").replace("@","]")


def obj_initor(prop_num):
	OBJ = "  {} = new {}({});\n"
	OBJS = """  for (size_t i = 0; i < {}; ++i) {{
    {}$i@ = new {}({});
  }}
"""
	NS = "{}_ns::{}_PIN{}"
	res = ""
	prop_dict = {}

	try:
		prop_dict = CONFIGS[prop_num]
	except IndexError:
		return res

	try:
		maglocks = prop_dict["MagnetLock"]
		for i in range(len(maglocks)):
			name = maglocks[i][0]
			res += OBJ.format(name, "MagnetLock", NS.format(IDS[prop_num], name.upper(), ""))
	except KeyError:
		pass

	try:
		leds = prop_dict["SimpleLed"]
		for i in range(len(leds)):
			name = leds[i][0]
			res += OBJ.format(name, "SimpleLed",
				NS.format(IDS[prop_num], name.upper(), ""))
	except KeyError:
		pass

	try:
		ardsen = prop_dict["ArdSensor"]
		for i in range(len(leds)):
			name = ardsen[i][0]
			res += OBJ.format(name, "ArdSensor", NS.format(IDS[prop_num], name.upper(), ""))
	except KeyError:
		pass	

	try:
		ardsens = prop_dict["ArdSensors"]
		name = ardsens[0]
		res += OBJS.format(NS.format(IDS[i], name.upper(), "S_COUNT"),
			name, "ArdSensor",
			NS.format(IDS[prop_num], name.upper(), "S$i@, ") + ardsens[1][1])
	except KeyError:
		pass

	try:
		timer = prop_dict["Timer"]
		for i in timer:
			res += OBJ.format(i[0], "Timer", "")
	except KeyError:
		pass

	return res.replace("$", "[").replace("@","]")

def props_creator():
	for i in range(PROPS_NUM):
		try:
			name = IDS[i]
		except IndexError:
			continue

		f = s_open(join("src", f"{name}.h"))
		content = f"""{GUARD}
#include "common.h"
#include <ds_basic.h>

enum {{
  {name.upper()}_STAGE_NONE,
  {name.upper()}_STAGE_GAME,
  {name.upper()}_STAGE_DONE }} {name}_stage;\n\n"""		
		content += obj_declarator(i)
		content += f"""
void {name}_onActivate()
{{
  console->println(F(\"{name}: onActivated\"));
  {name}_stage = {name.upper()}_STAGE_GAME;  
  strcpy(props_states${name.upper()}_STATE_POS@, MQTT_STRSTATUS_ENABLED);
}}

void {name}_onFinish()
{{
  console->println(F(\"{name}: onFinish\"));
  {name}_stage = {name.upper()}_STAGE_DONE;  
  strcpy(props_states${name.upper()}_STATE_POS@, MQTT_STRSTATUS_FINISHED);
}}

void {name}_init()
{{\n"""
		content += obj_initor(i)
		content += f"""
  {name}_stage = {name.upper()}_STAGE_NONE;  
  strcpy(props_states${name.upper()}_STATE_POS@, MQTT_STRSTATUS_READY);
}}

void {name}_routine()
{{
	
}}
"""
		content = content.replace("$", "[").replace("@","]")
		#print(content)
		f.write(content)



def main_creator():
	f = s_open(join("src", "main.cpp"))
	content = ""
	for i in IDS:
		content += f"#include \"{i}.h\"\n"
	content += f"""
void setup()
{{
  common_routine_init();\n
"""
	for i in IDS:
		content += f"  {i}_init();\n"
	content += f"\n  *console << CIRCUIT_NAME << F(\": init done\") << endl;"
	content += "\n}\n"
	content += f"""
void loop()
{{
  common_routine();\n
"""
	for i in IDS:
		content += f"  {i}_routine();\n"
	content += "}\n"	
	f.write(content)


def ini_creator():
	f = s_open("platformio.ini")	
	content = f"""[env:my_env]
platform = atmelavr
board = uno
framework = arduino

ip_addr = 192.168.10.{IP_END}
host = 192.168.10.1
login = root
password = 1

monitor_speed = 115200
; upload_port = COM4

; extra_scripts = w5500_remote.py
"""
	f.write(content)


def script_creator():
	f = s_open("w5500_remote.py")
	content = """import requests
import paramiko
import time

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

Import("env", "projenv")

config = configparser.ConfigParser()
config.read("platformio.ini")

ip_addr = config.get("env:my_env", "ip_addr")
host = config.get("env:my_env", "host")
username = config.get("env:my_env", "login")
password = config.get("env:my_env", "password")

# SFTP
port = 22
transport = paramiko.Transport((host, port))
transport.connect(username = username, password = password)
sftp = paramiko.SFTPClient.from_transport(transport)

# SSH
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=host, username=username, password=password, port=port)


def upload(source, target, env):

    firmware_dir = env['PIOENV']
    firmware_name = env['PROGNAME'] + '.bin'
    firmware_path = '.pio/build/' +  firmware_dir + '/' + firmware_name

    print "uploading firmware to router ip:" + host

    filepath = '/root/' + firmware_name
    localpath = firmware_path
    print localpath
    print sftp.put(localpath, filepath)
    sftp.close()

    print "uploaded file is in " + filepath

    print "Resetting arduino..."
    # arduino reset
    channel = ssh.get_transport().open_session()
    channel.get_pty()
    channel.settimeout(5.0)
    channel.exec_command('curl ' + ip_addr + ':44444') 
    print channel.recv(1024)

    channel.close

    time.sleep(1)

    # TFTP Download
    print "Firmware upgrade..."
    channel = ssh.get_transport().open_session()
    channel.get_pty()
    channel.settimeout(30.0)
    channel.exec_command('atftp --option "mode octet" -p -l ' + firmware_name + ' ' + ip_addr)
    print channel.recv(1024)
    print channel.recv(1024)
    print channel.recv(1024)
    print channel.recv(1024)

    channel.close
    # Closing all conections
    ssh.close()

    #print "TFTP connection to " + ipaddr

    #firmware_dir = env['PROJECTBUILD_DIR'] + '/' + env['PIOENV']
    #firmware_dir = env['PIOENV']
    #firmware_name = env['PROGNAME'] + '.bin'

    #env.Execute()
    
    #client = tftpy.TftpClient(ipaddr, 69)
    #client.upload(firmware_name, '.pioenvs\\my_env')

    #env.Execute("ping google.ru")  
    print "uploaded"  

    # env.Execute("pwd")
    #env.Execute("telnet " + ip_addr)

env.Replace(
    UPLOADCMD = upload
)

env.AddPostAction(
    "$BUILD_DIR/${{PROGNAME}}.elf",
    env.VerboseAction(" ".join([
        "$OBJCOPY", "-O", "binary",
        "$BUILD_DIR/${{PROGNAME}}.elf", "$BUILD_DIR/${{PROGNAME}}.bin"
    ]), "Creating $BUILD_DIR/${{PROGNAME}}.bin")
)
"""
	f.write(content)

def readme_creator():
	f = s_open("README.md")
	content = ""
	for i in IDS:
		content += f"{i}:\n\n"
	f.write(content)


work_dir_creator()
config_creator()
common_creator()
props_creator();
main_creator();
ini_creator()
script_creator()
readme_creator()