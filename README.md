# SIRS26-2019

Virtual Machine Setup:
- Download Ubuntu 18.04.3 from https://www.osboxes.org/ubuntu/
- Clone the virtual machine to have Server and Client versions.
- Default password: osboxes.org

MySQL Setup:

	-STEPS FOR MAC:
		- brew services start mysql ( might be needed )
		- mysql.server start
		- sudo mysql -u root
		- use SIRS26USERS;
		- ALTER TABLE Users MODIFY password varchar(500);
		- UPDATE Users SET password='$2b$14$hErDfgnwRJo3KqKlh8TMz.QPFHw.Dcz.XWe3I6LbiWqZV1fOd6F5y' WHERE user_id=3;
		- $ mysql -u root -h localhost SIRS26SCOREBOARD < SIRS26SCOREBOARD.sql
		
		
- Download python3 & pip3:
	- $ sudo apt install python3
	- $ sudo apt install python3-pip 
- Download python MySQL module: 
	- $ sudo pip3 install mysql-connector-python
- Install MySQL Server on Ubuntu: 
	- $ sudo apt-get install apache2
	- On Mac: brew install httpd
	- $ sudo /etc/init.d/apache2 start
	- On Mac: sudo /usr/sbin/apachectl start
	- $ sudo apt-get install mysql-server
	- $ sudo /etc/init.d/mysql start
	- On Mac:  mysql.server start
- (ALTERNATIVE) Install MySQL Server on Kali: 
	- $ sudo apt-get install apache2
	- $ sudo /etc/init.d/apache2 start
	- $ sudo apt-get install mariadb-server
	- $ sudo /etc/init.d/mysql start
- Import Database:
	- $ sudo mysql -u root
	- $ CREATE DATABASE SIRS26USERS;
	- $ quit
	- You have to leave MySQL to import.
	- $ sudo mysqldump -u root -pmysql SIRS26USERS < database/SIRS26USERS.sql
	- On Mac : https://stackoverflow.com/questions/11407349/how-to-export-and-import-a-sql-file-from-command-line-with-options
- Export Database:
	- $ sudo mysqldump -u root -pmysql SIRS26USERS > database/SIRS26USERS.sql
- Remove Database:
	- $ sudo mysql -u root
	- $ drop database SIRS26USERS;
- Setup Database User (If it is not created on import):
	- $ sudo mysql -u root
	- Check users with:
	- $ SELECT Host,User FROM mysql.user;
	- Create user:
	- $ use SIRS26USERS;
	- $ CREATE USER 'SIRSGROUP26'@'localhost' IDENTIFIED BY 'group26';
	- $ GRANT ALL PRIVILEGES ON SIRS26USERS TO 'SIRSGROUP26'@'localhost';
	- $ GRANT ALL PRIVILEGES ON SIRS26SCOREBOARD TO 'SIRSGROUP26'@'localhost';
	- Caso peça permissões também para tables específicas (Apenas mudar Users para outra table criada):
	- $ GRANT ALL PRIVILEGES ON SIRS26USERS.Users TO 'SIRSGROUP26'@'localhost';
	- $ GRANT ALL PRIVILEGES ON SIRS26SCOREBOARD.Scoreboard TO 'SIRSGROUP26'@'localhost';
	- $ GRANT ALL PRIVILEGES ON SIRS26SCOREBOARD.Vulnerability TO 'SIRSGROUP26'@'localhost';
- Create Table Users:
	- Check Commands.txt

- How to use log (python):
	- After importing file:
		- import System_log.py
	- User action (Type of message must be one of these: 'info','warning','error','critical'):
		- System_log.writeUserLog('user_id', 'username', 'action', 'sql_table', 'acceptance', 'type_of_message')
	- System event (Type of message must be one of these: 'info','warning','error','critical'):
		- System_log.writeSystemLog('topic', 'event','type_of_message')

Certificate Creation: https://carlo-hamalainen.net/2013/01/24/python-ssl-socket-echo-test-with-self-signed-certificate/ 

- Create certificates:
	- openssl genrsa -des3 -out server.orig.key 2048
	- openssl rsa -in server.orig.key -out server.key
	- openssl req -new -key server.key -out server.csr
	- openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
	
	https://www.portugal-a-programar.pt/forums/topic/51606-socket-ssl/
	
	1 - genrsa -out server.key 1024
	2 - req -new -key server.key -out server.csr
	3 - x509 -req -days 365 -in server.csr -signkey server.key -out server.crt


- File Server.py uses package re. No need to install comes with python3 already




- FIREWALL DEPLOYMENT AND TESTS

	- Step 1 --- Make Virtual Machines talk to each other :

		- https://www.youtube.com/watch?v=8V4Ez4NUHAk

	- Step 2 --- Configure Firewall in Ubuntu: ( https://www.geektechlab.com/6-simple-steps-to-configure-firewall-on-ubuntu-18-04/ )
		
		- Install ufw : apt-get install ufw ( Step 2.1 --- must be done )
		
		- Setup default policies : ( Step 2.2 --- must be done )
		
				- sudo ufw default deny incoming
				
				- sudo ufw default allow outgoing
				
		- Allow SSH Connections : 
		
				- sudo ufw allow ssh ( port 22 ) ( Step 2.3 --- must be done )

				(If SSH daemon is configured on a port other than the default, we can specify that for
				listening to that port in our command. If we configure SSH on it, 
				the following command listens to port 2244.)
				
				( Step 2.4 --- not to be done this and the others below are just for documentation purposes )
				- sudo ufw allow 2244  
				
				( We will use the following commands to specify the rule for UFW to allow incoming connections
				  on a specific port. For example, if we want our server to listen to HTTP on port 82,
				  the command to execute is below. )
				  
				- sudo ufw allow http
				- sudo ufw allow 82
			
				( For https we do )
				
				- sudo ufw allow https
			
				( We can also give a particular range of ports, which means more than one port. 
				  One thing to note is that we have to specify protocol in the command (tcp or udp).)
				  
				- sudo ufw allow 5000:5004/tcp
				- sudo ufw allow 5000:5004/udp

				( Sometimes we want to deny specific connections using IP address of the source. )

				- sudo ufw deny from 113.105.203.97

				With the following command, we can check the status of UFW.

				- sudo ufw status verbose
			
 		Another way to setup firewall :  ( https://www.geeksforgeeks.org/how-to-setup-firewall-in-linux/ )

Python package to encrypt:
- $pip install pycrypto
- How to use: https://www.novixys.com/blog/using-aes-encryption-decryption-python-pycrypto/
- https://stackoverflow.com/questions/30056762/rsa-encryption-and-decryption-in-python
	


Hash of password:
- pip3 install py-bcrypt
- pip3 install datetime
- why work factor of 14: https://cptwin.netlify.com/post/2019-03-02-password-hashing-work-factor-recommendations-in-2019/



