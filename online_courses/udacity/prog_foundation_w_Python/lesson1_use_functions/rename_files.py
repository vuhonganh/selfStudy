import os

def rename_files():
	#(1) get file names from the folder
	list_files = os.listdir("/home/anhvh/workspace/selfStudy/online_courses/udacity/prog_foundation_w_Python/lesson1_use_functions/prank")
	#print(list_files)
	
	curPath = os.getcwd()
	os.chdir("/home/anhvh/workspace/selfStudy/online_courses/udacity/prog_foundation_w_Python/lesson1_use_functions/prank")
	#(2) rename files 
	for file_name in list_files:
		os.rename(file_name, file_name.translate(None, "0123456789"))

	os.chdir(curPath)


rename_files()