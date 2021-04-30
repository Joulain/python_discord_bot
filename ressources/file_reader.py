
def file_reader(file):

	with open(file, "r") as f:
		return f.readline()[:-1]

TOKEN = file_reader('ressources/Token')
