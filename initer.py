from data import *

def ini_creator(data):
	f = s_open("platformio.ini", data)	
	content = f"""[env:my_env]
platform = atmelavr
board = {data.get_board()}
framework = arduino

ip_addr = 192.168.10.49
host = 192.168.10.1
login = root
password = 1

monitor_speed = 115200
; upload_port = COM4

; extra_scripts = w5500_remote.py
"""
	f.write(content)
