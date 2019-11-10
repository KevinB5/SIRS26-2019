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
	- $ mysql -u root -p SIRS26 < SIRS26.sql
- Export Database:
	- $ mysql -u root -p SIRS26 > SIRS26.sql
- Remove Database:
	- $ drop database SIRS26;

