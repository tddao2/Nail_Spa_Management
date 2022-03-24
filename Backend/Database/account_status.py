import mysql.connector

class AccountStatusDB:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host: "cis4375.csummbr3vhgu.us-east-2.rds.amazonaws.com",
            user: "admin",
            password: "cis4375spring2022",
            db: "cis4375db",
            raise_on_warnings: True
        )
        self.cursor = self.conn.cursor()


    def getAccountStatusID(self, account_status):
        self.cursor.execute("SELECT * FROM account_status WHERE account_status = (?)", account_status)
        
        # Fetch the account status information.
        rows = self.cursor.fetchone()

        # Return account status ID.
        return rows[0]


    def getAccountStatusName(self, account_status_id):
        self.cursor.execute("SELECT * FROM account_status WHERE account_status_id = (?)", account_status_id)
        
        # Fetch the account status information.
        rows = self.cursor.fetchone()

        # Return account status name.
        return rows[1]


    def __del__(self):
        self.conn.close()