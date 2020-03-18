from _utils import get_ids, s_open

def readme_creator():
	ids = get_ids()
	f = s_open("README.md")
	content = ""
	for i in ids:
		content += f"{i}:\n\n"
	f.write(content)