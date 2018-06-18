from os import listdir
from os.path import isdir

def recursive_list_files(dirname,endsWith=None):
	files = []
	for f in listdir(dirname):
		if isdir(dirname+'/'+f):
			files += recursive_list_files(dirname+'/'+f,endsWith)
		else:
			if endsWith:
				for e in endsWith:
					if f.endswith(e):
						files.append(dirname+'/'+f)
			else:
				files.append(dirname+'/'+f)
				
	return files