def file_reader(file):

	with open(file, "r") as f:
		return f.read()[:-1]

TOKEN = file_reader('ressources/Token')


UNSTART = file_reader('ressources/unstarting_module').split("\n")