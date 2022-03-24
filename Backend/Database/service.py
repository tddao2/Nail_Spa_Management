import mysql.connector
from Backend.connection import Connect

class ServiceDB:
    def __init__(self):
        self.conn = mysql.connector.connect(**Connect)
        self.cursor = self.conn.cursor()


    def getAllService(self):
        self.cursor.execute("SELECT * FROM service WHERE active = 1")
        rows = self.cursor.fetchall()
        return rows


    def getServiceByServiceID(self, service_id):
        self.cursor.execute("SELECT * FROM service WHERE service_id = ? AND active = 1", (account_id,))
        rows = self.cursor.fetchall()
        return rows


    def getServiceByName(self, service_description):
        self.cursor.execute("SELECT * FROM service WHERE service_description = ? AND active = 1", (username,))
        rows = self.cursor.fetchall()
        return rows

    def getServiceByName(self, price):
        self.cursor.execute("SELECT * FROM service WHERE price = ? AND active = 1", (username,))
        rows = self.cursor.fetchall()
        return rows
    
    def getServiceByName(self, service_type_id):
        self.cursor.execute("SELECT * FROM service WHERE service_type_id = ? AND active = 1", (username,))
        rows = self.cursor.fetchall()
        return rows



    def addAService(self, service_name, service_description, price, service_type_id):
        self.cursor.execute("INSERT INTO account (service_name, service_description, price, service_type_id) VALUES (?, ?, ?, ?)",
                            (service_name, service_description, price, service_type_id))
        self.conn.commit()


    def removeService(self, service_id):
        self.cursor.execute("UPDATE service SET active = 0 WHERE service_id = ?", (service_id,))
        self.conn.commit()


    def updateService(self, service_id, service_name, service_description, price, service_type_id):
        self.cursor.execute("UPDATE service SET service_name = ?, service_description = ?, price = ?, service_type_id = ?",
                            (service_name, service_description, price, service_type_id, service_id))
        self.conn.commit()


    def __del__(self):
        self.conn.close()