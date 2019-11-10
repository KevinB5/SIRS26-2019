import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="SIRSGROUP26",
    passwd="group26"
)

print(db)