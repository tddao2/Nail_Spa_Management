import mysql.connector
from Backend.connection import Connect

class AccountDB:
    def __init__(self):
        self.conn = mysql.connector.connect(**Connect)
        self.cursor = self.conn.cursor()

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Haven't finished <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def fetch(self, userfetch):
        self.cursor.execute("SELECT * FROM account WHERE username = %s", (userfetch,))
        row = self.cursor.fetchone()
        return row

    def insertAccount(self, account):
        self.cursor.execute("INSERT INTO account (username,password,secret_question,secret_answer,role_id,account_status_id,active) VALUES (%s,%s,%s,%s,%s,%s,%s)", 
                            (account[0],account[1],account[2],account[3],account[4],account[5],account[6]))
        self.conn.commit()

    def fetchSQ(self, fetchSQ):
        self.cursor.execute("SELECT * FROM account WHERE username = %s and secret_question = %s", (fetchSQ[0],fetchSQ[1]))
        row = self.cursor.fetchone()
        return row

    def Resetpassword(self, pwUpdate):
        self.cursor.execute("UPDATE account \
                            SET password = %s \
                            WHERE username = %s",
                            (pwUpdate[0],pwUpdate[1]))
        self.conn.commit()

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
        self.conn.commit()

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

    def getEmpByPass(self):
        self.cursor.execute("SELECT employee_id, password \
                            from employee e \
                            INNER JOIN account a \
                                ON e.account_id = a.account_id \
                            INNER JOIN account_status asi \
                                ON a.account_status_id = asi.account_status_id \
                            WHERE acct_status = 'active';") 
        rows = self.cursor.fetchall()
        return rows
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    def getAllAccount(self):
        self.cursor.execute("SELECT * FROM account WHERE active = 1")
        rows = self.cursor.fetchall()
        return rows


    def getAccountByAccountID(self, account_id):
        self.cursor.execute("SELECT * FROM account WHERE account_id = ? AND active = 1", (account_id,))
        rows = self.cursor.fetchall()
        return rows


    def getAccountByUsername(self, username):
        self.cursor.execute("SELECT * FROM account WHERE username = ? AND active = 1", (username,))
        rows = self.cursor.fetchall()
        return rows


    def addAccount(self, username, password, secret_question, secret_answer, role_id, account_status_id):
        self.cursor.execute("INSERT INTO account (username, password, secret_question, secret_answer, role_id, account_status_id) VALUES (?, ?, ?, ?, ?, ?)",
                            (username, password, secret_question, secret_answer, role_id, account_status_id))
        self.conn.commit()


    def removeAccount(self, account_id):
        self.cursor.execute("UPDATE account SET active = 0 WHERE account_id = ?", (account_id,))
        self.conn.commit()


    def updateAccount(self, account_id, username, password, secret_question, secret_answer, role_id, account_status_id):
        self.cursor.execute("UPDATE account SET username = ?, password = ?, secret_question = ?, secret_answer = ?, role_id = ?, account_status_id = ? WHERE account_id = ?",
                            (username, password, secret_question, secret_answer, role_id, account_status_id, account_id))
        self.conn.commit()


    def __del__(self):
        self.conn.close()