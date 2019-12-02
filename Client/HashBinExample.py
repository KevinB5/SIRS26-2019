import hashlib, sys


if __name__ == "__main__":
	
	if(len(sys.argv) < 1):
		print ("\nUSAGE:\t  <BIN_TO_HASH> \n")
		sys.exit(1)

	else:
		
		bin = bytes(sys.argv[1], "utf-8")
		print("BINARY GIVEN:", bin)

		f = open(bin, "rb")
		lines = f.read()
		
		hash_object = hashlib.sha512(lines)
		hex_dig = hash_object.hexdigest()

		print("BIN HASHED (STARTS IN $, IGNORE THE SPACE):", hex_dig)









