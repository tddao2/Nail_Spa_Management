import mysql.connector

class AccountDB:
    def __init__(self):
        self.conn = mysql.connector.connect(**{
            "host": "cis4375.csummbr3vhgu.us-east-2.rds.amazonaws.com",
            "user": "admin",
            "password": "cis4375spring2022",
            "db": "cis4375db",
            "raise_on_warnings": True
        })
        self.cursor = self.conn.cursor()

    def fetch(self, userfetch):
        print("looking up account")
        self.cursor.execute("SELECT * FROM account WHERE username = %s", (userfetch,))
        row = self.cursor.fetchone()
        return row


    def fetchAll(self):
        self.cursor.execute("SELECT * FROM account WHERE active = 1")
        rows = self.cursor.fetchall()
        return rows


    def insert(self, account):
        self.cursor.execute("INSERT INTO account (username,password,secret_question,secret_answer,role_id,account_status_id,active) VALUES (%s,%s,%s,%s,%s,%s,%s)", 
                            (account[0],account[1],account[2],account[3],account[4],account[5],account[6]))
        self.conn.commit()

    # def insert(self, first_name, last_name, birthday, phone, email, address, account_status_id, account_id):
    #     self.cursor.execute("INSERT INTO account (first_name, last_name, birthday, phone, email, address, account_status_id, account_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
    #                         (first_name, last_name, birthday, phone, email, address, account_status_id, account_id))
    #     self.conn.commit()


    # def remove(self, account_id):
    #     self.cursor.execute("UPDATE account SET active = 0 WHERE account_id = ?", (account_id,))
    #     self.conn.commit()


    # def update(self, account_id, first_name, last_name, birthday, phone, email, address, account_status_id, account_id):
    #     self.cursor.execute("UPDATE account SET first_name = ?, last_name = ?, birthday = ?, phone = ?, email = ?, address = ?, account_status_id = ?, account_id = ? WHERE account_id = ?",
    #                         (first_name, last_name, birthday, phone, email, address, account_status_id, account_id, account_id))
    #     self.conn.commit()


    def __del__(self):
        self.conn.close()