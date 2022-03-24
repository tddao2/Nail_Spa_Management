import mysql.connector
from Backend.connection import Connect

class CustomerDB:
    def __init__(self):
        self.conn = mysql.connector.connect(**Connect)
        self.cursor = self.conn.cursor()


    def getAllCustomer(self):
        self.cursor.execute("SELECT * FROM customer WHERE active = 1")
        rows = self.cursor.fetchall()
        return rows


    def getCustomerByCustomerID(self, customer_id):
        self.cursor.execute("SELECT * FROM customer WHERE customer_id = ? AND active = 1", (customer_id,))
        rows = self.cursor.fetchall()
        return rows


    def getCustomerByFirstName(self, first_name):
        self.cursor.execute("SELECT * FROM customer WHERE first_name = ? AND active = 1", (first_name,))
        rows = self.cursor.fetchall()
        return rows


    def getCustomerByLastName(self, last_name):
        self.cursor.execute("SELECT * FROM customer WHERE last_name = ? AND active = 1", (last_name,))
        rows = self.cursor.fetchall()
        return rows


    def getCustomerByPhone(self, phone):
        self.cursor.execute("SELECT * FROM customer WHERE phone = ? AND active = 1", (phone,))
        rows = self.cursor.fetchall()
        return rows


    def addCustomer(self, first_name, last_name, phone, email):
        self.cursor.execute("INSERT INTO customer (first_name, last_name, phone, email) VALUES (?, ?, ?, ?)",
                            (first_name, last_name, phone, email))
        self.conn.commit()


    def removeCustomer(self, customer_id):
        self.cursor.execute("UPDATE customer SET active = 0 WHERE customer_id = ?", (customer_id,))
        self.conn.commit()


    def updateCustomer(self, customer_id, first_name, last_name, phone, email):
        self.cursor.execute("UPDATE customer SET first_name = ?, last_name = ?, phone = ?, email = ? WHERE customer_id = ?",
                            (first_name, last_name, phone, email, customer_id))
        self.conn.commit()


    def __del__(self):
        self.conn.close()