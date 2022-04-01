import mysql.connector
from Backend.connection import Connect

class InvoiceDB:
    def __init__(self):
        self.conn = mysql.connector.connect(**Connect)
        self.cursor = self.conn.cursor()

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Haven't finished <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def Add_Invoice(self, empId, cusId, tip, discount, total):
        self.cursor.execute("INSERT INTO invoice(employee_id, customer_id, tip, discount, invoice_total) VALUES (%s, %s, %s, %s, %s)",
                            (empId, cusId, tip, discount, total))
        self.conn.commit()

        self.cursor.execute("SELECT LAST_INSERT_ID();")
        row = self.cursor.fetchone()
        # print("Add_Invoice ", row)
        return row[0]

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


    def getAllActiveInvoice(self):
        self.cursor.execute("SELECT * FROM invoice WHERE active = 1")
        rows = self.cursor.fetchall()
        return rows


    def getInvoiceByInvoiceID(self, invoice_id):
        self.cursor.execute("SELECT * FROM invoice WHERE invoice_id = ? AND active = 1", (invoice_id,))
        rows = self.cursor.fetchall()
        return rows


    def getInvoiceByInvoiceNumber(self, invoice_number):
        self.cursor.execute("SELECT * FROM invoice WHERE invoice_number = ? AND active = 1", (invoice_number,))
        rows = self.cursor.fetchall()
        return rows

    def getInvoiceByEmployeeID(self, employee_id):
        self.cursor.execute("SELECT * FROM invoice WHERE employee_id = ? AND active = 1", (employee_id,))
        rows = self.cursor.fetchall()
        return rows

    def getInvoiceByCustomerID(self, customer_id):
        self.cursor.execute("SELECT * FROM invoice WHERE customer_id = ? AND active = 1", (customer_id,))
        rows = self.cursor.fetchall()
        return rows

    def getInvoiceByInvoiceTotal(self, invoice_total):
        self.cursor.execute("SELECT * FROM invoice WHERE invoice_total = ? AND active = 1", (invoice_total,))
        rows = self.cursor.fetchall()
        return rows

    def getInvoiceByInvoiceDatetime(self, invoice_datetime):
        self.cursor.execute("SELECT * FROM invoice WHERE invoice_datetime = ? AND active = 1", (invoice_datetime,))
        rows = self.cursor.fetchall()
        return rows

    def getInvoiceByPaymentTotal(self, payment_total):
        self.cursor.execute("SELECT * FROM invoice WHERE payment_total = ? AND active = 1", (payment_total,))
        rows = self.cursor.fetchall()
        return rows

    def getInvoiceByPaymentDatetime(self, payment_datetime):
        self.cursor.execute("SELECT * FROM invoice WHERE payment_datetime = ? AND active = 1", (payment_datetime,))
        rows = self.cursor.fetchall()
        return rows

  #  def getInvoiceByInActive(self, active):
   #     self.cursor.execute("SELECT * FROM invoice WHERE active = 0", (active,))
    #    rows = self.cursor.fetchall()
     #   return rows
      


    def addInvoice(self, invoice_number, employee_id, customer_id, invoice_total, invoice_datetime, payment_total, payment_datetime):
        self.cursor.execute("INSERT INTO invoice (invoice_number, employee_id, customer_id, invoice_total, invoice_datetime, payment_total, payment_datetime) VALUES (?, ?, ?, ?, ?, ?,?)",
                            (invoice_number, employee_id, customer_id, invoice_total, invoice_datetime, payment_total, payment_datetime))
        self.conn.commit()


    def removeInvoice(self, invoice_id):
        self.cursor.execute("UPDATE invoice SET active = 0 WHERE invoice_id = ?", (invoice_id,))
        self.conn.commit()


    def updateInvoice(self, invoice_id, invoice_number, employee_id, customer_id, invoice_total, invoice_datetime, payment_total, payment_datetime):
        self.cursor.execute("UPDATE invoice SET username = ?, password = ?, secret_question = ?, secret_answer = ?, role_id = ?, account_status_id = ? WHERE account_id = ?",
                            (invoice_number, employee_id, customer_id, invoice_total, invoice_datetime, payment_total, payment_datetime, invoice_id))
        self.conn.commit()


    def __del__(self):
        self.conn.close()