import os

def file_writer(folder, subfolder, file, text):
	path = "past/" + folder
	if not os.path.exists(path):
		os.mkdir(path)
	path = path + "/" + subfolder
	if not os.path.exists(path):
		os.mkdir(path)
	path = path + "/" + file
	with open(path, "a") as f:
		f.write(text)

def full_writer(texte):
	with open("live", "a") as f:
		f.write(texte)

