import mysql.connector
from Backend.connection import Connect

class AppointmentDB:
    def __init__(self):
        self.conn = mysql.connector.connect(**Connect)
        self.cursor = self.conn.cursor()


    def getAllAppointment(self):
        self.cursor.execute("SELECT * FROM appointment WHERE active = 1")
        rows = self.cursor.fetchall()
        return rows


    def getAppointmentByAppointmentID(self, appointment_id):
        self.cursor.execute("SELECT * FROM appointment WHERE appointment_id = ? WHERE active = 1", (appointment_id,))
        rows = self.cursor.fetchall()
        return rows


    def getAppointmentByCustomerID(self, customer_id):
        self.cursor.execute("SELECT * FROM appointment WHERE customer_id = ? WHERE active = 1", (customer_id,))
        rows = self.cursor.fetchall()
        return rows

    def getAppointmentByDateTime(self, datetime):
        self.cursor.execute("SELECT * FROM appointment WHERE datetime = ? WHERE active = 1", (datetime,))
        rows = self.cursor.fetchall()
        return rows
    
    def getAppointmentByServiceID(self, service_id):
        self.cursor.execute("SELECT * FROM appointment WHERE service_id = ? WHERE active = 1", (service_id,))
        rows = self.cursor.fetchall()
        return rows



    def addAppointment(self, customer_id, datetime, service_id, appointment_id):
        self.cursor.execute("INSERT INTO appointment (customer_id, datetime, service_id, appointment_id) VALUES (?, ?, ?, ?)",
                            (customer_id, datetime, service_id, appointment_id))
        self.conn.commit()

    
    def removeAppointment(self, appointment_id):
        self.cursor.execute("UPDATE appointment SET active = 0 WHERE appointment_id = ?", (appointment_id,))
        self.conn.commit()


    def updateAppointment(self, customer_id, datetime, service_id, appointment_id):
        self.cursor.execute("UPDATE appointment SET customer_id = ?, datetime = ?, service_id = ?, appointment_id = ?",
                            (customer_id, datetime, service_id, appointment_id))
        self.conn.commit()


    def __del__(self):
        self.conn.close()