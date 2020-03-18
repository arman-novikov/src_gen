from data import *

def main_creator(data):
	ids = data.get_ids()
	f = s_open(join("src", "main.cpp"), data)
	content = ""
	for i in ids:
		content += f"#include \"{i}.h\"\n"
	content += f"""
void setup()
{{
  common_routine_init();\n
"""
	for i in ids:
		content += f"  {i}_init();\n"
	content += f"\n  *console << CIRCUIT_NAME << F(\": init done\") << endl;"
	content += "\n}\n"
	content += f"""
void loop()
{{
  common_routine();\n
"""
	for i in ids:
		content += f"  {i}_routine();\n"
	content += "}\n"	
	f.write(content)
