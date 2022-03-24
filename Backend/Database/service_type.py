import mysql.connector
from Backend.connection import Connect

class ServiceTypeDB:
    def __init__(self):
        self.conn = mysql.connector.connect(**Connect)
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