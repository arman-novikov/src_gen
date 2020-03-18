from _utils import *

def ini_creator():
	f = s_open("platformio.ini")	
	content = f"""[env:my_env]
platform = atmelavr
board = {get_board()}
framework = arduino

ip_addr = 192.168.10.{get_IP_end()}
host = 192.168.10.1
login = root
password = 1

monitor_speed = 115200
; upload_port = COM4

; extra_scripts = w5500_remote.py
"""
	f.write(content)