import sys


if __name__ == "__main__":

	if(len(sys.argv) < 2):
		print ("\nUSAGE:\t  <FILE_TO_SEARCH_FOR_VULNERABILITIES> \n")
		sys.exit(1)
		  
	else:
		  
		bin = bytes(sys.argv[1], "utf-8")
		print("FILE GIVEN:", bin)
		  
		f = open(bin, "r")
		lines = f.read()
		
		print("gets" in lines)
		  
		  
		  
		  
		  
