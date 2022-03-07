import mysql.connector

class EmployeeDB:
    def __init__(self):
        print("initializing employeedb")
        self.conn = mysql.connector.connect(**{
            "host": "cis4375.csummbr3vhgu.us-east-2.rds.amazonaws.com",
            "user": "admin",
            "password": "cis4375spring2022",
            "db": "cis4375db",
            "raise_on_warnings": True
        })
        self.cursor = self.conn.cursor()
        print("initialized employeedb")



    def fetchByAccount(self, account_id):
        print("looking up account")
        self.cursor.execute("SELECT * FROM employee WHERE account_id = %s", (account_id,))
        row = self.cursor.fetchone()
        return row



    def fetchAll(self):
        self.cursor.execute("SELECT * FROM employee WHERE active = 1")
        rows = self.cursor.fetchall()
        return rows


    def insert(self, employee):
        self.cursor.execute("INSERT INTO employee (first_name,last_name,birthday,phone,email,address,employee_status_id,account_id,active) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            (employee[0],employee[1],employee[2],employee[3],employee[4],employee[5],employee[6],employee[7],employee[8])) 
        self.conn.commit()



    def remove(self, employee_id):
        self.cursor.execute("UPDATE employee SET active = 0 WHERE employee_id = ?", (employee_id,))
        self.conn.commit()


    def update(self, employee_id, first_name, last_name, birthday, phone, email, address, employee_status_id, account_id):
        self.cursor.execute("UPDATE employee SET first_name = ?, last_name = ?, birthday = ?, phone = ?, email = ?, address = ?, employee_status_id = ?, account_id = ? WHERE employee_id = ?",
                            (first_name, last_name, birthday, phone, email, address, employee_status_id, account_id, employee_id))
        self.conn.commit()


    def __del__(self):
        self.conn.close()