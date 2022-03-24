import mysql.connector
from Backend.connection import Connect

class EmployeeStatusDB:
    def __init__(self):
        self.conn = mysql.connector.connect(**Connect)
        self.cursor = self.conn.cursor()


    def getEmployeeStatusID(self, employee_status):
        self.cursor.execute("SELECT * FROM employee_status WHERE employee_status = (?)", employee_status)
        rows = self.cursor.fetchone()
        return rows[0]


    def getEmployeeStatusName(self, employee_status_id):
        self.cursor.execute("SELECT * FROM employee_status WHERE employee_status_id = (?)", employee_status_id)
        rows = self.cursor.fetchone()
        return rows[1]


    def __del__(self):
        self.conn.close()