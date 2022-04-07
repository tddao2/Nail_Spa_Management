import mysql.connector
from Backend.connection import Connect

class InvoiceLineItemDB:
    def __init__(self):
        self.conn = mysql.connector.connect(**Connect)
        self.cursor = self.conn.cursor()

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Haven't finished <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def Add_InvoiceItem(self, InvId, SerId):

        for index in range(len(SerId)):
            self.cursor.execute("INSERT INTO invoice_line_item(invoice_id, service_id) VALUES (%s, %s)",
                                (InvId, SerId[index]))
            self.conn.commit()

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    def getAllInvoiceLineItem(self):
        self.cursor.execute("SELECT * FROM invoice_line_item WHERE active = 1")
        rows = self.cursor.fetchall()
        return rows

    def getInvoiceLineItemByinvoiceLineItemId(self, invoice_line_item_id):
        self.cursor.execute("SELECT * FROM invoice_line_item WHERE invoice_line_item_id = ? AND active = 1", (invoice_line_item_id,))
        rows = self.cursor.fetchall()
        return rows


    def getInvoiceLineItemByInvoiceId(self, invoice_id):
        self.cursor.execute("SELECT * FROM invoice_line_item WHERE invoice_id = ? AND active = 1", (invoice_id,))
        rows = self.cursor.fetchall()
        return rows


    def getInvoiceLineItemByServiceId(self, service_id):
        self.cursor.execute("SELECT * FROM invoice_line_item WHERE service_id = ? AND active = 1", (service_id,))
        rows = self.cursor.fetchall()
        return rows


   # def getInvoiceLineItemByInactive(self, active):
   #     self.cursor.execute("SELECT * FROM invoice_line_item WHERE active = 0", (active,))
   #     rows = self.cursor.fetchall()
   #     return rows



    def addInvoiceLineItem(self, invoice_line_item_id, invoice_id, service_id):
        self.cursor.execute("INSERT INTO invoice_line_item (invoice_line_item_id, invoice_id, service_id) VALUES (?, ?, ?)",
                            (invoice_line_item_id, invoice_id, service_id))
        self.conn.commit()


    def removeInvoiceLineItem(self, invoice_line_item_id):
        self.cursor.execute("UPDATE invoice_line_item SET active = 0 WHERE invoice_line_item_id = ?", (invoice_line_item_id,))
        self.conn.commit()


    def updateInvoiceLineItem(self, invoice_line_item_id, invoice_id, service_id):
        self.cursor.execute("UPDATE invoice_line_item SET invoice_line_item_id = ?, invoice_id = ?, service_id = ?",
                            (invoice_line_item_id, invoice_id, service_id))
        self.conn.commit()


    def __del__(self):
        self.conn.close()