import mysql.connector

class EmployeeStatusDB:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host: "cis4375.csummbr3vhgu.us-east-2.rds.amazonaws.com",
            user: "admin",
            password: "cis4375spring2022",
            db: "cis4375db",
            raise_on_warnings: True
        )
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