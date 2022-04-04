import mysql.connector
from Backend.connection import Connect

class EmployeeDB:
    def __init__(self):
        self.conn = mysql.connector.connect(**Connect)
        self.cursor = self.conn.cursor()

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Haven't finished <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def insertEmployee(self, employee):
        self.cursor.execute("INSERT INTO employee (first_name,last_name,birthday,phone,email,address,employee_status_id,account_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                            (employee[0],employee[1],employee[2],employee[3],employee[4],employee[5],employee[6],employee[7])) 
        self.conn.commit()
    
    def EmpFetch(self):
        self.cursor.execute("SELECT employee_id, first_name, last_name, birthday, email, phone, address, emp_status \
                            FROM employee \
                            INNER JOIN employee_status \
                                ON employee.employee_status_id = employee_status.employee_status_id \
                            WHERE active = 1;")
        rows = self.cursor.fetchall()
        return rows

    def EmpfetchAll(self):
        self.cursor.execute("SELECT employee_id, concat(first_name,' ',last_name) as Name \
                            FROM employee \
                            WHERE active = 1 \
                            ORDER BY Name ASC")
        rows = self.cursor.fetchall()
        return rows

    def EmpUpdate(self, data):
        self.cursor.execute("UPDATE employee \
                            SET first_name = %s, last_name = %s, birthday = %s, email = %s, phone = %s, address = %s, employee_status_id = %s \
                            WHERE employee_id = %s",
                            (data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]))
        self.conn.commit()

    def EmpDelete(self, data):
        self.cursor.execute("UPDATE employee \
                            SET active = 0 \
                            WHERE employee_id = %s",
                            (data,))
        self.conn.commit()

    def EmpSearch(self, data):
        self.cursor.execute("SELECT employee_id, first_name, last_name, birthday, email, phone, address, emp_status \
                            FROM employee \
                            INNER JOIN employee_status \
                                ON employee.employee_status_id = employee_status.employee_status_id \
                            WHERE "+data[0]+" LIKE '%"+data[1]+"%' and active = 1")
        rows = self.cursor.fetchall()
        return rows

    def EmpFetchHistory(self):
        self.cursor.execute("SELECT employee_id, first_name, last_name, birthday, email, phone, address, emp_status \
                            FROM employee \
                            INNER JOIN employee_status \
                                ON employee.employee_status_id = employee_status.employee_status_id \
                            WHERE active = 0;")
        rows = self.cursor.fetchall()
        return rows
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    def getAllEmployee(self):
        self.cursor.execute("SELECT * FROM employee WHERE active = 1")
        rows = self.cursor.fetchall()
        return rows


    def getEmployeeByEmployeeID(self, employee_id):
        self.cursor.execute("SELECT * FROM employee WHERE employee_id = ? AND active = 1", (employee_id,))
        rows = self.cursor.fetchall()
        return rows


    def getEmployeeByFirstName(self, first_name):
        self.cursor.execute("SELECT * FROM employee WHERE first_name = ? AND active = 1", (first_name,))
        rows = self.cursor.fetchall()
        return rows


    def getEmployeeByLastName(self, last_name):
        self.cursor.execute("SELECT * FROM employee WHERE last_name = ? AND active = 1", (last_name,))
        rows = self.cursor.fetchall()
        return rows


    def getEmployeeByPhone(self, phone):
        self.cursor.execute("SELECT * FROM employee WHERE phone = ? AND active = 1", (phone,))
        rows = self.cursor.fetchall()
        return rows


    def addEmployee(self, first_name, last_name, birthday, phone, email, address, employee_status_id, account_id):
        self.cursor.execute("INSERT INTO employee (first_name, last_name, birthday, phone, email, address, employee_status_id, account_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                            (first_name, last_name, birthday, phone, email, address, employee_status_id, account_id))
        self.conn.commit()


    def removeEmployee(self, employee_id):
        self.cursor.execute("UPDATE employee SET active = 0 WHERE employee_id = ?", (employee_id,))
        self.conn.commit()


    def updateEmployee(self, employee_id, first_name, last_name, birthday, phone, email, address, employee_status_id, account_id):
        self.cursor.execute("UPDATE employee SET first_name = ?, last_name = ?, birthday = ?, phone = ?, email = ?, address = ?, employee_status_id = ?, account_id = ? WHERE employee_id = ?",
                            (first_name, last_name, birthday, phone, email, address, employee_status_id, account_id, employee_id))
        self.conn.commit()


    def __del__(self):
        self.conn.close()