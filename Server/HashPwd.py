import bcrypt, datetime


BCRYPT_DEFAULT_COST = 14
BCRYPT_ADMIN_COST = 16



class Hash:

	def __init__(self, plain_text_password, userPriviliges):
		self.plain_text_password = plain_text_password
		self.userPriviliges = userPriviliges


	def diff_month(self, year1, year2, month1, month2):
		""" difference between months """
		return (year1 - year2) * 12 + month1 - month2



	def work_factor(self):
		""" calculate the work factor to use in the hash function """
		# difference of months between 15/01/2019 and today
		x = datetime.datetime.now()
		year1, year2 = x.year, 2019
		month1, month2 = x.month, 1

		diffMonth = self.diff_month(year1, year2, month1, month2)
		
		if( self.userPriviliges == "admin"):
			return (diffMonth//18) + BCRYPT_ADMIN_COST
		else:
			return (diffMonth//18) + BCRYPT_DEFAULT_COST



	def get_hashed_password(self):
		""" calculate the hash of the password """
		# Hash a password for the first time
		#   (Using bcrypt, the salt is saved into the hash itself)
		workFactor = self.work_factor()
		return str(bcrypt.hashpw(self.plain_text_password, bcrypt.gensalt(workFactor)), "utf-8")



	def check_password(self, hashed_password):
		""" Check if hashed_password is the hash of the plain_text_password corresponds """
		# Check hashed password. Using bcrypt, the salt is saved into the hash itself
		return bcrypt.checkpw(self.plain_text_password, hashed_password)




