from data import *

def common_creator(data):
	ids = data.get_ids();
	props_num = data.get_props_num()
	erp_num = data.get_erp_num()
	f = s_open(join("src","common.h"), data)
	content = f"""{data.get_guard()}
#include \"config.h\"
#include <ds_bootloader.h>
#include <ds_wdt.h>
#include <ds_mqtt_manager.h>

enum {{{[i.upper() + "_STATE_POS" for i in ids]}}};
"""	
	content += f"""
constexpr size_t PROPS_NUM = {props_num}U;
constexpr int props_num_in_ERP$PROPS_NUM@ = {{{[str(i) for i in erp_num]}}};
"""	
	content = content.replace("-1", "ds_MQTT::NOT_SHOW")
	
	strids = ""
	for i in range(1, props_num+1):
		try:
			strids += f"\nconstexpr char PROP_{str(i)}_STRID$@  = \"{ids[i-1]}\";"
		except IndexError:
			pass
	
	content += strids
	names = []
	for i in range(1, props_num+1):
		try:
			void = ids[i-1]
			names.append(f"PROP_{str(i)}_STRID")
		except IndexError:
			names.append("nullptr")
	content += f"""
const char *propsNames$PROPS_NUM@ = {{{[i for i in names]}}};
"""
	cbs = []
	for i in ids:
		cbs.append([f"{i}_onActivate", f"{i}_onFinish"])

	counter = -1
	for i in cbs:
		counter += 1
		content += f"""
void {i[0]}();
void {i[1]}();
prop_CBs_t  {ids[counter]}_cbs = {{{i[0]}, {i[1]}, ds_MQTT::reset}};
"""
	content += "\nprops_CBs_t props_cbs$PROPS_NUM@ = {"
	for i in range(props_num):
		try:
			content += f"&{ids[i]}_cbs, " 
		except IndexError:
			content += "nullptr, "
	content += "};\n\n"

	states = []
	for i in range(props_num):
		try:
			states.append(f"{ids[i]}_state")
		except IndexError:
			pass
	for i in states:
		content += f"prop_state_t {i} = {{0}};\n"

	content += "props_states_t props_states$PROPS_NUM@ = {"
	for i in range(props_num):
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