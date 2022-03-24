import mysql.connector
from Backend.connection import Connect

class RoleDB:
    def __init__(self):
        self.conn = mysql.connector.connect(**Connect)
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