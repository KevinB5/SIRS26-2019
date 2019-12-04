import DB_User
import DB_Scoreboard

# Global Variables

validOperations = [1,2,3,4]
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
		userAuthType=DB_User.getUserAuthType(user)
		
		if(userGroupID!=None and userAuthType!=None):
			
			userGroupIDInt=userGroupID[0]
			userAuthTypeInt=userAuthType[0]

			# checkAuthorization(operation,user,userGroupIDInt,userAuthTypeInt)
			for elm in validGroupID:
				validGroupIDList.append(elm[0])
			
			if( (userGroupIDInt in validGroupIDList) and (userAuthTypeInt in validAuthType) ):
				if(operation not in validOperations):
					return False
				else:
					if (operation==1 or operation==2 or operation==3):
						#read User Score -- operation = 1
						#read User Vulns and Fingerps -- operation = 2
						#read Scoreboard
						if(userAuthTypeInt not in validAuthType):
							return False
						else:
							return True
					elif (operation==4):
						#only for admin: read vulns and fingpr of all team
						if(userAuthTypeInt != 1):
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
