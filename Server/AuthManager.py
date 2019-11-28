import DB_User
import DB_Scoreboard

# Global Variables

validOperations = [1,2,3,4,5,6]
validUser=DB_User.getUsersList()
validGroupID=DB_User.getGroupIDList()
validGroupIDList=[]
validAuthType= [1,2]
operation=0
user=''
groupid=0
authtype=0

# Functions for authorization control


def getAuthorizationValues(operation, user):

	if(operation!=None and user!=None):
		userGroupID=DB_User.getUserGroupID(user)
		userGroupIDInt=userGroupID[0]
		userAuthType=DB_User.getUserAuthType(user)
		userAuthTypeInt=userAuthType[0]
		if(userGroupID!=None and userAuthType!=None):
			# checkAuthorization(operation,user,userGroupIDInt,userAuthTypeInt)
			for elm in validGroupID:
				validGroupIDList.append(elm[0])
			if( (userGroupIDInt in validGroupIDList) and (userAuthTypeInt in validAuthType) ):
				if(operation not in validOperations):
					return False
				else:
					if (operation==1):
						#readScoreboard
						if(userAuthTypeInt<1 or userAuthTypeInt>2):
							return False
						else:
							return True
					elif (operation==2):
						#readTeamScoreboard
						if(authtype!=2):
							return False
						else:
							return True
					elif (operation==3):
						#readTeamVulnerabilities
						if(authtype!=2):
							return False
						else:
							return True
					elif (operation==4):
						#readTeamFingerprinting
						if(authtype!=2):
							return False
						else:
							return True
					elif (operation==5):
						#submitFingerprint
						if(userAuthTypeInt<1 or userAuthTypeInt>2):
							return False
						else:
							return True
					elif (operation==6):
						#submitVulnerability
						if(userAuthTypeInt<1 or userAuthTypeInt>2):
							return False
						else:
							return True
					else:
						return False
			else:
				return False
	
		else:
			return False
	else:
		return False