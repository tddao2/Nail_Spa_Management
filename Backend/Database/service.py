import mysql.connector
from Backend.connection import Connect

class ServiceDB:
    def __init__(self):
        self.conn = mysql.connector.connect(**Connect)
        self.cursor = self.conn.cursor()

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Haven't finished <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def getAllServices(self):
        self.cursor.execute("SELECT service_id, service_name, price FROM service ORDER BY service_id ASC;")
        rows = self.cursor.fetchall()
        return rows

    def getAllServicesType(self):        
        self.cursor.execute("SELECT service_type_desc from service_type order by service_type_desc ASC;")
        rows = self.cursor.fetchall()
        return rows

    def getAllServiceName(self):
        self.cursor.execute("SELECT service_id, a.service_type_desc, service_name, price FROM service_type a \
                            JOIN service b \
                                ON a.service_type_code = b.service_type_code \
                            ORDER BY a.service_type_desc ASC;")
        rows = self.cursor.fetchall()
        return rows

    def ServiceUpdate(self, serviceId, serviceName, servicePrice):
        self.cursor.execute("UPDATE service \
                            SET service_name = %s,price = %s \
                            WHERE service_id = %s",
                            (serviceName, servicePrice, serviceId))
        self.conn.commit()
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


    def getAllService(self):
        self.cursor.execute("SELECT * FROM service")
        rows = self.cursor.fetchall()
        return rows


    def getServiceByServiceID(self, service_id):
        self.cursor.execute("SELECT * FROM service WHERE service_id = ?", (service_id,))
        rows = self.cursor.fetchall()
        return rows


    def getServiceByServiceDescription(self, service_description):
        self.cursor.execute("SELECT * FROM service WHERE service_description = ?", (service_description,))
        rows = self.cursor.fetchall()
        return rows

    def getServiceByPrice(self, price):
        self.cursor.execute("SELECT * FROM service WHERE price = ?", (price,))
        rows = self.cursor.fetchall()
        return rows
    
    def getServiceByServiceTypeID(self, service_type_id):
        self.cursor.execute("SELECT * FROM service WHERE service_type_id = ? ", (service_type_id,))
        rows = self.cursor.fetchall()
        return rows



    def addAService(self, service_name, service_description, price, service_type_id):
        self.cursor.execute("INSERT INTO service (service_name, service_description, price, service_type_id) VALUES (?, ?, ?, ?)",
                            (service_name, service_description, price, service_type_id))
        self.conn.commit()

    # Shouldn't the services table have an active column? When services are no longer available?
    #def removeService(self, service_id):
    #    self.cursor.execute("UPDATE service SET active = 0 WHERE service_id = ?", (service_id,))
    #    self.conn.commit()


    def updateService(self, service_id, service_name, service_description, price, service_type_id):
        self.cursor.execute("UPDATE service SET service_name = ?, service_description = ?, price = ?, service_type_id = ?",
                            (service_name, service_description, price, service_type_id, service_id))
        self.conn.commit()


    def __del__(self):
        self.conn.close()