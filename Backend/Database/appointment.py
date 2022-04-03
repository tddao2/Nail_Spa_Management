import mysql.connector
from Backend.connection import Connect

class AppointmentDB:
    def __init__(self):
        self.conn = mysql.connector.connect(**Connect)
        self.cursor = self.conn.cursor()

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Haven't finished <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def addAppt(self,CusId, date, time, desc):
        self.cursor.execute("INSERT INTO appointment (customer_id, date_appt, time_appt, appt_desc) VALUES (%s,%s,%s,%s)",
                            (CusId, date, time, desc))
        self.conn.commit()

    def getAllAppt(self):
        self.cursor.execute("SELECT appointment_id, concat(c.first_name,' ',c.last_name) as CustomerName, phone, email, date_appt, time_appt, appt_desc \
                            FROM appointment a \
                            JOIN customer c \
                                ON a.customer_id = c.customer_id \
                            WHERE a.active = 1 \
                            ORDER BY time_appt ASC;")
        rows = self.cursor.fetchall()
        return rows

    def UpdateAppt(self, date, time, desc, id):
        self.cursor.execute("UPDATE appointment \
                            SET date_appt = %s, time_appt = %s, appt_desc = %s \
                            WHERE appointment_id = %s", 
                            (date, time, desc, id))
        self.conn.commit()

    def DeleteAppt(self, appointment_id):
        self.cursor.execute("UPDATE appointment SET active = 0 WHERE appointment_id = %s", (appointment_id,))
        self.conn.commit()

    def ApptHistory(self):
        self.cursor.execute("SELECT appointment_id,concat(c.first_name,' ',c.last_name) as CustomerName, phone, email, date_appt, time_appt, appt_desc, a.active \
                            FROM appointment a \
                            JOIN customer c \
	                            ON a.customer_id = c.customer_id \
                            WHERE a.active = 0 or (date_appt >= DATE_ADD(CURDATE(), INTERVAL -3 DAY) and date_appt <= CURDATE()) \
                            ORDER BY time_appt ASC;")
        rows = self.cursor.fetchall()
        return rows

    def SearchAllAppt(self, selection, FLP):
        self.cursor.execute("SELECT appointment_id, concat(c.first_name,' ',c.last_name) as CustomerName, phone, email, date_appt, time_appt, appt_desc \
                            FROM appointment a \
                            JOIN customer c \
                                ON a.customer_id = c.customer_id \
                            WHERE "+selection+" LIKE '%"+FLP+"%' and a.active = 1 \
                            ORDER BY time_appt ASC;")
        rows = self.cursor.fetchall()
        return rows

    def SearchApptHistory(self,selection,FLP):
        self.cursor.execute("SELECT appointment_id,concat(c.first_name,' ',c.last_name) as CustomerName, phone, email, date_appt, time_appt, appt_desc, a.active \
                            FROM appointment a \
                            JOIN customer c \
	                            ON a.customer_id = c.customer_id \
                            WHERE (a.active = 0 and "+selection+" LIKE '%"+FLP+"%') or (date_appt >= DATE_ADD(CURDATE(), INTERVAL -3 DAY) and date_appt <= CURDATE() and "+selection+" LIKE '%"+FLP+"%') \
                            ORDER BY time_appt ASC;")
        rows = self.cursor.fetchall()
        return rows
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


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