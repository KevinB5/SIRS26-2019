import mysql.connector
import sys


try:
    db = mysql.connector.connect(
        host="localhost",
        user="SIRSGROUP26",
        passwd="group26",
        database="SIRS26"
    )

    username = raw_input("Insert your username:")
    password = raw_input("Insert your password:")
    cursor = db.cursor(prepared=True)
    query = "SELECT username FROM Users WHERE username=%s AND password=%s;"
    parameters = (username,password)
    cursor.execute(query,parameters)
    result = cursor.fetchone()

    if result != None:
        print('Login Successful')
    else:
        sys.exit()

except:
    print("Error connecting to the server")

finally:
    if db.is_connected():
        cursor.close()
        db.close()

if(result):
    print('MENU:')