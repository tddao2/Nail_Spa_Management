import mysql.connector

class ServiceTypeDB:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host: "cis4375.csummbr3vhgu.us-east-2.rds.amazonaws.com",
            user: "admin",
            password: "cis4375spring2022",
            db: "cis4375db",
            raise_on_warnings: True
        )
        self.cursor = self.conn.cursor()


    def getServiceTypeID(self, service_type):
        self.cursor.execute("SELECT * FROM service_type WHERE service_type = (?)", service_type)
        rows = self.cursor.fetchone()
        return rows[0]


    def getServiceTypeName(self, service_type_id):
        self.cursor.execute("SELECT * FROM service_type WHERE service_type_id = (?)", service_type_id)
        rows = self.cursor.fetchone()
        return rows[1]


    def __del__(self):
        self.conn.close()