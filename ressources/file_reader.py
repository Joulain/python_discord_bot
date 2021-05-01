
def file_reader(file):

	with open(file, "r") as f:
		return f.readline()[:-1]

TOKEN = file_reader('ressources/Token')


Unstart = file_reader('ressources/unstarting_module')