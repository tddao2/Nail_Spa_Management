import mysql.connector
# from mysql.connector import errorcode
from Backend.connection import Connect

class EmployeeDB:
    def __init__(self):
        self.cnx = mysql.connector.connect(**Connect)
        self.cursor = self.cnx.cursor()

    def fetch(self, userfetch):
        self.cursor.execute("SELECT * FROM account WHERE username = %s", (userfetch,))
        row = self.cursor.fetchone()
        return row
    
    def insertAccount(self, account):
        self.cursor.execute("INSERT INTO account (username,password,secret_question,secret_answer,role_id,account_status_id,active) VALUES (%s,%s,%s,%s,%s,%s,%s)", 
                            (account[0],account[1],account[2],account[3],account[4],account[5],account[6]))
        self.cnx.commit()

    def insertEmployee(self, employee):
        self.cursor.execute("INSERT INTO employee (first_name,last_name,birthday,phone,email,address,employee_status_id,account_id,active) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            (employee[0],employee[1],employee[2],employee[3],employee[4],employee[5],employee[6],employee[7],employee[8])) 
        self.cnx.commit()

    def fetchSQ(self, fetchSQ):
        self.cursor.execute("SELECT * FROM account WHERE username = %s and secret_question = %s", (fetchSQ[0],fetchSQ[1]))
        row = self.cursor.fetchone()
        return row

    def Resetpassword(self, pwUpdate):
        self.cursor.execute("UPDATE account \
                            SET password = %s \
                            WHERE username = %s",
                            (pwUpdate[0],pwUpdate[1]))
        self.cnx.commit()