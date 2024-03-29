import bcrypt, datetime, sys


BCRYPT_DEFAULT_COST = 14
BCRYPT_ADMIN_COST = 16



def diff_month(year1, year2, month1, month2):
	""" difference between months """
	return (year1 - year2) * 12 + month1 - month2



def work_factor(userPriviliges):
	""" calculate the work factor to use in the hash function """
	# difference of months between 15/01/2019 and today
	x = datetime.datetime.now()
	year1, year2 = x.year, 2019
	month1, month2 = x.month, 1

	diffMonth = diff_month(year1, year2, month1, month2)
	
	if( userPriviliges == "Admin"):
		return (diffMonth//18) + BCRYPT_ADMIN_COST
	else:
		return (diffMonth//18) + BCRYPT_DEFAULT_COST



def get_hashed_password(plain_text_password, userPriviliges):
	""" calculate the hash of the password """
	# Hash a password for the first time
	#   (Using bcrypt, the salt is saved into the hash itself)
	workFactor = work_factor(userPriviliges)
	return bcrypt.hashpw(plain_text_password, bcrypt.gensalt(workFactor))




def check_password(plain_text_password, hashed_password):
	""" check if hashed_password is the hash of the plain_text_password corresponds """
	# Check hashed password. Using bcrypt, the salt is saved into the hash itself
	return bcrypt.checkpw(plain_text_password, hashed_password)



if __name__ == "__main__":
	
	if(len(sys.argv) < 1):
		print ("\nUSAGE:\t  <PASSWORD_TO_HASH> \n")
		sys.exit(1)

	else:
		passs = bytes(sys.argv[1], "utf-8")
		print("PASSWORD GIVEN:", passs)

		passs = get_hashed_password(passs, "user")
		print("PASSWORD HASHED (STARTS IN $, IGNORE THE SPACE):", str(passs, "utf-8") )









