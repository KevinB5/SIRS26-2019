# SIRS26-2019

Virtual Machine Setup:
- Download Ubuntu 18.04.3 from https://www.osboxes.org/ubuntu/
- Default password: osboxes.org
- execute:
	- $ sudo apt get update
	- $ sudo apt get upgrade
- Clone 4 times the virtual machine to have Server (VM1), Client(VM2), Trust Manager(VM3) and Switch(VM4) versions.

- Global config (for VM 1,2 and 3):
	- Install python3:
		- $ sudo apt install python3
		- $ sudo apt install python3-pip
	- Install apache2:
		- $ sudo pip3 install mysql-connector
		- $ sudo /etc/init.d/mysql start (may need to start apache2 also)
	- Install mySQL-server:
		- $ sudo apt-get install mysql-server
	- Install pycrypto and pycryptodome:
		- $ pip install pycrypto
		- $ pip install pycryptodome
	- Install bcrypt and datetime:
		- $ pip install bcrypt
		- $ pip install datetime
	- Install firewall:
		- $ apt-get install ufw
		- Setup default policies (must be done):
			- $ sudo ufw default deny incoming
			- $ sudo ufw default allow outgoing

- VM 1 - Server: (192.168.1.1):
	- VirtualBoxSettings:
		- Network - Adapter 2 - Internal Network (sirs_switchServer)
		- $ sudo hostnamectl set-hostname server
		- $ sudo vi /etc/hosts
		- In the hosts file, change the name for 127.0.1.1 to server
		- Edit /etc/network/interfaces  - (Follow interfaces picture on Screenshots/interfaces_settings.JPG)
- VM 2 - Client: (192.168.2.1)
	- VirtualBoxSettings:
		- Network - Adapter 2 - Internal Network (sirs_switchClient)
		- $ sudo hostnamectl set-hostname client
		- $ sudo vi /etc/hosts
		- In the hosts file, change the name for 127.0.1.1 to client
		- Edit /etc/network/interfaces  - (Follow interfaces picture on Screenshots/interfaces_settings.JPG)
- VM 3 - TrustManager: (192.168.3.1)
	- VirtualBoxSettings:
		- Network - Adapter 2 - Internal Network (sirs_switchTrustManager)
		- $ sudo hostnamectl set-hostname trustmanager
		- $ sudo vi /etc/hosts
		- In the hosts file, change the name for 127.0.1.1 to trustmanager
		- Edit /etc/network/interfaces  - (Follow interfaces picture on Screenshots/interfaces_settings.JPG)
- VM 4 - Switch/Firewall: (192.168.1.254 , 192.168.2.254 , 192.168.3.254)
	- VirtualBoxSettings:
		- Network - Adapter 2 - Internal Network (sirs_switchServer)
		- Network - Adapter 3 - Internal Network (sirs_switchClient)
		- Network - Adapter 4 - Internal Network (sirs_switchTrustManager)
		- $ sudo hostnamectl set-hostname switch
		- $ sudo vi /etc/hosts
		- In the hosts file, change the name for 127.0.1.1 to switch
		- Edit /etc/sysctl.conf :
			- Uncoment net.ipv4.ip_forward=1

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
	



