import mysql.connector
from Backend.connection import Connect

class AdminDB:
    def __init__(self):
        self.cnx = mysql.connector.connect(**Connect)
        self.cursor = self.cnx.cursor(buffered=True)

    def EmpFetch(self):
        self.cursor.execute("SELECT employee_id, first_name, last_name, birthday, email, phone, address, emp_status \
                            FROM employee \
                            INNER JOIN employee_status \
                                ON employee.employee_status_id = employee_status.employee_status_id \
                            WHERE active = 0;")
        rows = self.cursor.fetchall()
        return rows
    
    def EmpUpdate(self, data):
        self.cursor.execute("UPDATE employee \
                            SET first_name = %s, last_name = %s, birthday = %s, email = %s, phone = %s, address = %s, employee_status_id = %s \
                            WHERE employee_id = %s",
                            (data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]))
        self.cnx.commit()

    def EmpDelete(self, data):
        self.cursor.execute("UPDATE employee \
                            SET active = 1 \
                            WHERE employee_id = %s",
                            (data,))
        self.cnx.commit()

    def EmpSearch(self, data):
        self.cursor.execute("SELECT employee_id, first_name, last_name, birthday, email, phone, address, emp_status \
                            FROM employee \
                            INNER JOIN employee_status \
                                ON employee.employee_status_id = employee_status.employee_status_id \
                            WHERE "+data[0]+" LIKE '%"+data[1]+"%' and active = 0")
        rows = self.cursor.fetchall()
        return rows

    def EmpFetchHistory(self):
        self.cursor.execute("SELECT employee_id, first_name, last_name, birthday, email, phone, address, emp_status \
                            FROM employee \
                            INNER JOIN employee_status \
                                ON employee.employee_status_id = employee_status.employee_status_id \
                            WHERE active = 1;")
        rows = self.cursor.fetchall()
        return rows

    def AcctFetch(self):
        self.cursor.execute("SELECT a.account_id, concat(first_name,' ',last_name) as full_name, username, role_name, acct_status \
                            FROM employee e \
                            INNER JOIN account a \
                                ON e.account_id = a.account_id \
                            INNER JOIN account_status asi \
                                ON a.account_status_id = asi.account_status_id \
                            INNER JOIN roles r \
                                ON a.role_id = r.role_id \
                            WHERE acct_status = 'active';")
        rows = self.cursor.fetchall()
        return rows

    def AcctFetchAll(self):
        self.cursor.execute("SELECT a.account_id, concat(first_name,' ',last_name) as full_name, username, role_name, acct_status \
                            FROM employee e \
                            INNER JOIN account a \
                                ON e.account_id = a.account_id \
                            INNER JOIN account_status asi \
                                ON a.account_status_id = asi.account_status_id \
                            INNER JOIN roles r \
                                ON a.role_id = r.role_id;")
        rows = self.cursor.fetchall()
        return rows

    def AcctUpdate(self, data):
        self.cursor.execute("UPDATE account \
                            SET role_id = %s, account_status_id = %s \
                            WHERE account_id = %s",
                            (data[0],data[1],data[2]))
        self.cnx.commit()

    def AcctSearch(self, data):
        self.cursor.execute("SELECT a.account_id, concat(first_name,' ',last_name) as full_name, username, role_name, acct_status \
                            FROM employee e \
                            INNER JOIN account a \
                                ON e.account_id = a.account_id \
                            INNER JOIN account_status asi \
                                ON a.account_status_id = asi.account_status_id \
                            INNER JOIN roles r \
                                ON a.role_id = r.role_id \
                            WHERE "+data[0]+" LIKE '%"+data[1]+"%'") 
        rows = self.cursor.fetchall()
        return rows
