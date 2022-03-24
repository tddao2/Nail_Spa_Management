import mysql.connector

class RoleDB:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host: "cis4375.csummbr3vhgu.us-east-2.rds.amazonaws.com",
            user: "admin",
            password: "cis4375spring2022",
            db: "cis4375db",
            raise_on_warnings: True
        )
        self.cursor = self.conn.cursor()


    def getRoleID(self, role_name):
        self.cursor.execute("SELECT * FROM role WHERE role_name = (?)", role_name)
        
        # Fetch the role information.
        rows = self.cursor.fetchone()

        # Return role ID.
        return rows[0]


    def getRoleName(self, role_id):
        self.cursor.execute("SELECT * FROM role WHERE role_id = (?)", role_id)
        
        # Fetch the role information.
        rows = self.cursor.fetchone()

        # Return role name.
        return rows[1]


    def __del__(self):
        self.conn.close()