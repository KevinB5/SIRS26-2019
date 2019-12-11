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
				
How to use:
	
	After setup we can start the program.
	For that we need to have all 3 VMs running, and then follow the next steps for each one:
		
		- Open New Terminal (CTRL+ALT+T)
		- $ cd ~/Documents/SIRS26-2019/(VM NAME)
			example: $ cd ~/Documents/SIRS26-2019/Client
		- $ python3 (VM NAME).py
			example: $ python3 Client.py
		The step above should look like the image at Screenshots/1_Startup.JPG .
	Now we have Client, Server and TrustManager running.
	After everything running we can use our program.
		
	Now we only interact with Client Interface (Client VM):
	
	First, you need to identify yourself to TrustManager like show at Screenshots/2_NS.JPG ;
		Input your Username;
	You will be prompted to Login Menu, choose option 1 ;
		Input your password;
	If everything went fine, it should look like Screenshots/4_User_Login.JPG and you're logged in the program.
	
	Now it's time to navigate between menus and explore the program;
	Remember to navigate between menus we allways need to input the number of the option we want;
	
	At this point we're at the Main Menu;
	
	 	We have 4 options : 
	 		1. Scoreboard (Takes us to Scoreboard Menu)
			2. Submit     (Takes us to Submit Menu)
			3. Compute Fingerprint (Takes us to Compute Fingerprint )
			0. Last Menu (Takes us back to the last Menu)
		
		Input the number of the option to follow;
		Example: 1
	
	A briefly explanation of each option and it's following ones:
	
		Scoreboard Menu:
	
			1. Check Score 
			2. Check Vulnerabilities and Fingerprints
			3. Check Team ScoreBoard 
			4. Check Team Vulnerabilities and Fingerprints
			0. Last Menu (Takes us back to the last Menu)
		
			Check score shows your current score;
			Check Vulnerabilities and Fingerprints shows Vulnerabilities and Fingerprints you have submited;
			
			Team Leader Options Only:
			
			Check Team ScoreBoard shows the team ScoreBoard;
			Check Team Vulnerabilities and Fingerprints shows all submited Vulnerabilities and Fingerprints 
			from members of your team;
			
		Submit Menu:
				
 			1. Fingerprint and Vulnerabilities
			0. Last Menu (Takes us back to the last Menu)
		
			Fingerprint and Vulnerabilities option will ask for the fingerprint and vulnerabilities:
				The input for fingerprint is the computed fingerprint we can get for the option Compute Fingerprint explained further ahead,
				The input for vulnerabilities is the name of the file containing the vulnerabilities;
				
		Compute Fingerprint:
			
			This option will ask for the Binary:
				The input to give to Binary is the name of the file of which we want to generate the corresponding Fingerprint;
	
	To exit the program we just need to go to Login Menu again and choose option 0.Exit ;
	
	For more examples of the interactions go to folder Screenshots ,
	
	That's it, now we know how to use the program,
	Explore it and enjoy.
	Stay safe.
	
			
