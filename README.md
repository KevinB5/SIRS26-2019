# SIRS26-2019

Virtual Machine Setup:
- Download Ubuntu 18.04.3 from https://www.osboxes.org/ubuntu/
- Clone the virtual machine to have Server and Client versions.
- Default password: osboxes.org

MySQL Setup:
- Download python MySQL module: 
	- $ python pip install mysql-connector-python
- Install MySQL Server on Ubuntu: 
	- $ apt-get install apache2
	- $ /etc/init.d/apache2 start
	- $ apt-get install mysql-server
	- $ /etc/init.d/mysql start
- (ALTERNATIVE) Install MySQL Server on Kali: 
	- $ apt-get install apache2
	- $ apt-get install mariadb-server
	- $ apt-get install mysql-server
	- $ /etc/init.d/mysql start
- Import Database:
	- $ mysql -u root
	- $ CREATE DATABASE SIRS26;
	- $ quit
	- You have to leave MySQL to import.
	- $ mysqldump -u root -pmysql SIRS26 < SIRS26.sql
- Export Database:
	- $ mysqldump -u root -pmysql SIRS26 > SIRS26.sql
- Remove Database:
	- $ mysql -u root
	- $ drop database SIRS26;
- Setup Database User (If it is not created on import):
	- $ mysql -u root
	- Check users with:
	- $ SELECT Host,User FROM mysql.user;
	- Create user:
	- $ use SIRS26;
	- $ CREATE USER 'SIRSGROUP26'@'localhost' IDENTIFIED BY 'group26';
	- $ GRANT ALL PRIVILEGES ON SIRS26 TO 'SIRSGROUP26'@'localhost';

