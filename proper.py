from data import *

def obj_declarator(string_id, data):
	OBJ = "{} *{};\n"
	OBJS = "{} *{}${}@;\n"
	res = ""
	ids = data.get_ids()
	prop_dict = {}
	try:
		prop_dict = data.get_config()[string_id]
	except KeyError:
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
		pins_num = f"{string_id}_ns::{name.upper()}_PINS_COUNT"
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


def obj_initor(string_id, data):
	OBJ = "  {} = new {}({});\n"
	OBJS = """  for (size_t i = 0; i < {}; ++i) {{
    {}$i@ = new {}({});
  }}
"""
	NS = "{}_ns::{}_PIN{}"
	res = ""

	try:
		prop_dict = data.get_config()[string_id]
	except KeyError:
		return res

	try:
		maglocks = prop_dict["MagnetLock"]
		for i in range(len(maglocks)):
			name = maglocks[i][0]
			res += OBJ.format(name, "MagnetLock", NS.format(string_id, name.upper(), ""))
	except KeyError:
		pass

	try:
		leds = prop_dict["SimpleLed"]
		for i in range(len(leds)):
			name = leds[i][0]
			res += OBJ.format(name, "SimpleLed",
				NS.format(string_id, name.upper(), ""))
	except KeyError:
		pass

	try:
		ardsen = prop_dict["ArdSensor"]
		for i in range(len(ardsen)):
			name = ardsen[i][0]
			params = ardsen[i][2]
			res += OBJ.format(name, "ArdSensor", NS.format(string_id, name.upper(), ", " + params))
	except KeyError:
		pass	

	try:
		ardsens = prop_dict["ArdSensors"]
		name = ardsens[0]
		res += OBJS.format(NS.format(string_id, name.upper(), "S_COUNT"),
			name, "ArdSensor",
			NS.format(string_id, name.upper(), "S$i@, ") + ardsens[1][1])
	except KeyError:
		pass

	try:
		timer = prop_dict["Timer"]
		for i in timer:
			res += OBJ.format(i[0], "Timer", "")
	except KeyError:
		pass

	return res.replace("$", "[").replace("@","]")


def routines_creator(string_id, data):
	routine_call = "  {}->routine();\n"
	try:
		timers = data.get_config()[string_id]["Timer"]
	except (KeyError, IndexError):
		return ""
	res = ""
	for i in timers:
		res += routine_call.format(i)
	res += '\n'

	res += f"  if ({string_id}_stage != {string_id.upper()}_STAGE_GAME)\n    return;\n\n"

	return res.replace("]", "").replace("[", "").replace("\'", "")


def props_creator(data):
	for name in data.get_ids():
		f = s_open(join("src", f"{name}.h"), data)
		content = f"""{data.get_guard()}
#include <ds_basic.h>
#include "common.h"

enum {{
  {name.upper()}_STAGE_NONE,
  {name.upper()}_STAGE_GAME,
  {name.upper()}_STAGE_DONE }} {name}_stage;\n\n"""		
		content += obj_declarator(name, data)
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
		content += obj_initor(name, data)
		content += f"""
  {name}_stage = {name.upper()}_STAGE_NONE;  
  strcpy(props_states${name.upper()}_STATE_POS@, MQTT_STRSTATUS_READY);
}}

void {name}_routine()
{{\n"""
		content += routines_creator(name, data)
		content += "}"

		content = content.replace("$", "[").replace("@","]")
		f.write(content)
