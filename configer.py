from data import *

def pin_declarator(string_id, data):
	PIN_DEC = "  constexpr uint8_t {}_PIN = {};\n"
	PINS_DEC = "  constexpr uint8_t {}_PINS${}@ = {{\n    {}  \n  }};\n"
	res = ""
	prop_dict = {}
	try:
		prop_dict = data.get_config()[string_id]
	except KeyError:
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


def config_creator(data):
	f = s_open(join("src","config.h"), data)
	content = f"""{data.get_guard()}
#include <Arduino.h>\n
constexpr char CIRCUIT_NAME[] = \"{data.get_circuit_name()}\";
constexpr byte IP_ENDING = {str(data.get_IP_end())};
constexpr bool UPLOAD_BOOT_INFO = true;\n
"""
	for string_id in data.get_ids():
		try:
			CONFS = pin_declarator(string_id, data);
			content += f"namespace {string_id}_ns {{\n{CONFS}\n}}\n\n"
		except IndexError:
			pass
	f.write(content)
