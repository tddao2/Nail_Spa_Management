import mysql.connector
from Backend.connection import Connect

class AccountDB:
    def __init__(self):
        self.conn = mysql.connector.connect(**Connect)
        self.cursor = self.conn.cursor()


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