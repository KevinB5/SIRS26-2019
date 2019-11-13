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
	- $ sudo /etc/init.d/apache2 start
	- $ sudo apt-get install mysql-server
	- $ sudo /etc/init.d/mysql start
- (ALTERNATIVE) Install MySQL Server on Kali: 
	- $ sudo apt-get install apache2
	- $ sudo /etc/init.d/apache2 start
	- $ sudo apt-get install mariadb-server
	- $ sudo /etc/init.d/mysql start
- Import Database:
	- $ sudo mysql -u root
	- $ CREATE DATABASE SIRS26;
	- $ quit
	- You have to leave MySQL to import.
	- $ sudo mysqldump -u root -pmysql SIRS26 < SIRS26.sql
- Export Database:
	- $ sudo mysqldump -u root -pmysql SIRS26 > SIRS26.sql
- Remove Database:
	- $ sudo mysql -u root
	- $ drop database SIRS26;
- Setup Database User (If it is not created on import):
	- $ sudo mysql -u root
	- Check users with:
	- $ SELECT Host,User FROM mysql.user;
	- Create user:
	- $ use SIRS26;
	- $ CREATE USER 'SIRSGROUP26'@'localhost' IDENTIFIED BY 'group26';
	- $ GRANT ALL PRIVILEGES ON SIRS26 TO 'SIRSGROUP26'@'localhost';
	- Caso peça permissões também para tables específicas (Apenas mudar Users para outra table criada):
	- $ GRANT ALL PRIVILEGES ON SIRS26.Users TO 'SIRSGROUP26'@'localhost';
- Create Table Users:
	- Check Commands.txt
	
	
	
	

Certificate Creation: https://carlo-hamalainen.net/2013/01/24/python-ssl-socket-echo-test-with-self-signed-certificate/ 

- Create certificates:
	- openssl genrsa -des3 -out server.orig.key 2048
	- openssl rsa -in server.orig.key -out server.key
	- openssl req -new -key server.key -out server.csr
	- openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt



