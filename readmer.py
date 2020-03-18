from data import s_open

def readme_creator(data):
	ids = data.get_ids()
	f = s_open("README.md", data)
	content = ""
	for i in ids:
		content += f"{i}:\n\n"
	f.write(content)