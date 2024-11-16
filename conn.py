import mysql.connector

def createConnection():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "JV2047labs.?",
        db = "students" 
    )
    