from _utils import *

def obj_declarator(prop_num):
	OBJ = "{} *{};\n"
	OBJS = "{} *{}${}@;\n"
	res = ""
	prop_dict = {}
	try:
		prop_dict = get_config()[prop_num]
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
		prop_dict = get_config()[prop_num]
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
		for i in range(len(ardsen)):
			name = ardsen[i][0]
			params = ardsen[i][2]
			res += OBJ.format(name, "ArdSensor", NS.format(IDS[prop_num], name.upper(), ", " + params))
	except KeyError:
		pass	

	try:
		ardsens = prop_dict["ArdSensors"]
		name = ardsens[0]
		res += OBJS.format(NS.format(IDS[prop_num], name.upper(), "S_COUNT"),
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


def routines_creator(prop_num):
	ROUTINE = "  {}->routine();\n"
	name = IDS[prop_num]
	res = f"  if ({name}_stage != {name.upper()}_STAGE_GAME)\n    return;\n\n"
	timers = []
	try:
		timers = get_config()[prop_num]["Timer"]
	except (KeyError, IndexError):
		return ""

	for i in timers:
		res += ROUTINE.format(i);

	return res.replace("]","").replace("[","").replace("\'","");


def props_creator():
	props_num = get_props_num()
	ids = get_ids()
	for i in range(props_num):
		try:
			name = ids[i]
		except IndexError:
			continue

		f = s_open(join("src", f"{name}.h"))
		content = f"""{get_guard()}
#include <ds_basic.h>
#include "common.h"

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
{{\n"""
		content += routines_creator(i)
		content += "}"

		content = content.replace("$", "[").replace("@","]")
		f.write(content)
