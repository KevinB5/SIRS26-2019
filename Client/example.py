import hashlib, sys
from datetime import datetime


if __name__ == "__main__":
	
	if(len(sys.argv) < 1):
		print ("\nUSAGE:\t  <BIN_TO_HASH> \n")
		sys.exit(1)

	else:
		
		'''
		bin = bytes(sys.argv[1], "utf-8")

		f = open(bin, "rb")
		lines = f.read()
		
		splitLines = lines.split()
		vulns = []

		for i in range(len(splitLines)):
			if( splitLines[i] == b"Vulnerability:"):
				vulns.append(str(splitLines[i+1], "utf-8"))

		print("VULNS:", vulns)
		'''


		# current date and time
		now = datetime.now()

		print("NOW:", str(now), "\n\n")
		timestamp = datetime.timestamp(now)
		print("timestamp =", timestamp)







