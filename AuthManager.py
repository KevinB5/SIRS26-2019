import DB_User
import DB_Scoreboard

# Global Variables

validOperations = ['readScoreboard','submitFingerprint','submitVulnerability','readTeamScoreboard','readTeamVulnerabilities','readTeamFingerprinting']
validUser=getUsersList()
validGroupID=getGroupIDList()
validAuthType= [2,3]


# Functions for authorization control
def readScoreboard(operation, user, groupid, authtype):
	if(authtype<1 or authtype>2)
		return False
	else:
		return True

def submitFingerprint(operation, user, groupid, authtype):
	if(authtype<1 or authtype>2)
		return False
	else:
		return True

def submitVulnerability(operation, user, groupid, authtype):
	if(authtype<1 or authtype>2)
	 return False
	else:
		return True

def readTeamScoreboard(operation, user, groupid, authtype):
	if(groupid==)
	if(authtype!=2)
		return False
	else:
		return True

def readTeamVulnerabilities(operation, user, groupid, authtype):

	if(groupid==)
	if(authtype!=2)
		return False
	else:
		return True

def readTeamFingerprinting(operation, user, groupid, authtype):
	if(groupid==)
	if(authtype!=2)
	 return False
	else:
		return True

def default():
    return False

switcher = {
	1:readScoreboard(operation,user,groupid,authtype)
	2: submitFingerprint(operation, user, groupid, authtype)
	3: submitVulnerability(operation, user, groupid, authtype)
	4: readTeamScoreboard(operation, user, groupid, authtype)
	5: readTeamVulnerabilities(operation, user, groupid, authtype)
	6: readTeamFingerprinting(operation, user, groupid, authtype)
}

def switch(operation,user,groupid,authtype):
    return switcher.get(validOperations.index(operation)+1, default)()

def getAuthorization(operation, user, groupid, authtype):

	if(validOperations.contains(operation) and validUser.contains(user) and validGroupID.contains(groupid) and validAuthType.contains(authtype)):
		if(validOperations.index(operation)==''):
			return 0
		else:
	else:
		return 0