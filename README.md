# SIRS26-2019

Virtual Machine Setup:
- Download Ubuntu 18.04.3 from https://www.osboxes.org/ubuntu/
- Default password: osboxes.org
- execute:
	- $ sudo apt get update
	- $ sudo apt get upgrade
- Clone 2 times (Full Clone) the virtual machine to have Server (VM1), Client(VM2), Trust Manager(VM3) versions.

- Global config (for VM 1,2 and 3):
	- Install python3:
		- $ sudo apt install python3
		- $ sudo apt install python3-pip
	- Install apache2:
		- $ sudo apt-get install apache2
		- $ sudo /etc/init.d/apache2 start
	- Install mySQL-server:
		- $ sudo pip3 install mysql-connector
		- $ sudo apt-get install mysql-server
		- $ sudo /etc/init.d/mysql start
	- Install pycrypto and pycryptodome:
		- $ pip install pycrypto
		- $ pip install pycryptodome
	- Install bcrypt and datetime:
		- $ pip install bcrypt
		- $ pip install datetime
	- Install firewall:
		- $ sudo apt-get install ufw


- VM 1 - Server: (192.168.1.20):
	- VirtualBox Settings:
		- Network - Adapter 2 - Internal Network (sirs_switchServerClient)
	- $ sudo hostnamectl set-hostname server
	- $ sudo vi /etc/hosts
	- In the hosts file, change the name for 127.0.1.1 to server
	- Edit /etc/network/interfaces  - (Follow interfaces picture on Screenshots/interfaces_settings.JPG)
	
- VM 2 - Client: (192.168.1.10)
	- VirtualBox Settings:
		- Network - Adapter 2 - Internal Network (sirs_switchServerClient)
	- $ sudo hostnamectl set-hostname client
	- $ sudo vi /etc/hosts
	- In the hosts file, change the name for 127.0.1.1 to client
	- Edit /etc/network/interfaces  - (Follow interfaces picture on Screenshots/interfaces_settings.JPG)
	
- VM 3 - TrustManager: (192.168.1.100)
	- VirtualBox Settings:
		- Network - Adapter 2 - Internal Network (sirs_switchServerClient)
	- $ sudo hostnamectl set-hostname trustmanager
	- $ sudo vi /etc/hosts
	- In the hosts file, change the name for 127.0.1.1 to trustmanager
	- Edit /etc/network/interfaces  - (Follow interfaces picture on Screenshots/interfaces_settings.JPG)


- MySQL Setup:
	- Import Database:
		- $ sudo mysql -u root
		- $ CREATE DATABASE SIRS26USERS;
		- $ CREATE DATABASE SIRS26SCOREBOARD;
		- $ quit
		- You have to leave MySQL to import.
		- $ sudo mysql -u root -pmysql SIRS26USERS < database/SIRS26USERS.sql
		- $ sudo mysql -u root -pmysql SIRS26SCOREBOARD < database/SIRS26SCOREBOARD.sql
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

- FIREWALL DEPLOYMENT
	
		- Setup default policies (must be done for each VM):
			- $ sudo ufw default deny incoming
			- $ sudo ufw default allow outgoing
		- Setup specific rules:
		
			VM1(Server):
				- $ sudo ufw allow from 192.168.1.10 to any port 65433
			
			VM2(Client):
				- $ sudo ufw allow from 192.168.1.20 to any port 65433
				- $ sudo ufw allow from 192.168.1.100 to any port 65432
				
			VM3(TrustManager):
			
				- $ sudo ufw allow from 192.168.1.10 to any port 65432
