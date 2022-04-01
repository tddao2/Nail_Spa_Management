import mysql.connector
from Backend.connection import Connect

class CustomerDB:
    def __init__(self):
        self.conn = mysql.connector.connect(**Connect)
        self.cursor = self.conn.cursor()

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Haven't finished <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def getAllCustByIdAndFname(self):
        self.cursor.execute("SELECT customer_id, concat(first_name,' ',last_name) as Name, phone, email \
                            FROM customer \
                            ORDER BY Name ASC")
        rows = self.cursor.fetchall()
        return rows

    def fetchCusId(self, first, last):
        self.cursor.execute("SELECT customer_id FROM customer \
                            WHERE first_name LIKE '%"+first+"%' and last_name LIKE '%"+last+"%' and active = 1;")
        row = self.cursor.fetchone()
        if row:
            return row[0]
        else:
            return None

    def addCustomerAndGetId(self, first, last, phone, email):
        self.cursor.execute("INSERT INTO customer (first_name, last_name, phone, email) VALUES (%s, %s, %s, %s)",
                            (first, last, phone, email))
        self.conn.commit()

        self.cursor.execute("SELECT LAST_INSERT_ID();")
        row = self.cursor.fetchone()
        print("addCustomerAndGetId", row)
        return row[0]


    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


    def getAllCustomer(self):
        self.cursor.execute("SELECT * FROM customer WHERE active = 1")
        rows = self.cursor.fetchall()
        return rows


    def getCustomerByCustomerID(self, customer_id):
        self.cursor.execute("SELECT * FROM customer WHERE customer_id = %s AND active = 1", (customer_id,))
        rows = self.cursor.fetchall()
        return rows


    def getCustomerByFirstName(self, first_name):
        self.cursor.execute("SELECT * FROM customer WHERE first_name = %s AND active = 1", (first_name,))
        rows = self.cursor.fetchall()
        return rows


    def getCustomerByLastName(self, last_name):
        self.cursor.execute("SELECT * FROM customer WHERE last_name = %s AND active = 1", (last_name,))
        rows = self.cursor.fetchall()
        return rows


    def getCustomerByPhone(self, phone):
        self.cursor.execute("SELECT * FROM customer WHERE phone = %s AND active = 1", (phone,))
        rows = self.cursor.fetchall()
        return rows


    def addCustomer(self, first_name, last_name, phone, email):
        self.cursor.execute("INSERT INTO customer (first_name, last_name, phone, email) VALUES (%s, %s, %s, %s)",
                            (first_name, last_name, phone, email))
        self.conn.commit()


    def removeCustomer(self, customer_id):
        self.cursor.execute("UPDATE customer SET active = 0 WHERE customer_id = %s", (customer_id,))
        self.conn.commit()


    def updateCustomer(self, customer_id, first_name, last_name, phone, email):
        self.cursor.execute("UPDATE customer SET first_name = %s, last_name = %s, phone = %s, email = %s WHERE customer_id = %s",
                            (first_name, last_name, phone, email, customer_id))
        self.conn.commit()


    def __del__(self):
        self.conn.close()