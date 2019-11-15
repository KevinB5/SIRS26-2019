# SIRS26-2019

Virtual Machine Setup:
- Download Ubuntu 18.04.3 from https://www.osboxes.org/ubuntu/
- Clone the virtual machine to have Server and Client versions.
- Default password: osboxes.org

MySQL Setup:
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
	- $ sudo mysqldump -u root -pmysql SIRS26USERS < SIRS26USERS.sql
	- On Mac : https://stackoverflow.com/questions/11407349/how-to-export-and-import-a-sql-file-from-command-line-with-options
- Export Database:
	- $ sudo mysqldump -u root -pmysql SIRS26USERS > SIRS26USERS.sql
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


- File Server.py uses package re. No need to install comes with python3 already
