import mysql.connector
from Backend.connection import Connect

class AccountStatusDB:
    def __init__(self):
        self.conn = mysql.connector.connect(**Connect)
        self.cursor = self.conn.cursor()

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Haven't finished <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def AcctFetch(self):
        self.cursor.execute("SELECT a.account_id, concat(first_name,' ',last_name) as full_name, username, role_name, acct_status \
                            FROM employee e \
                            INNER JOIN account a \
                                ON e.account_id = a.account_id \
                            INNER JOIN account_status asi \
                                ON a.account_status_id = asi.account_status_id \
                            INNER JOIN roles r \
                                ON a.role_id = r.role_id \
                            WHERE a.account_status_id IN (1,2) and a.active = 1;")
        rows = self.cursor.fetchall()
        return rows
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

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