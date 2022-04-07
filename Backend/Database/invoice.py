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
        if row:
            return row[0]
        else:
            return None

    def getAllInvoice(self):
        self.cursor.execute("SELECT i.invoice_id, concat(e.first_name,' ',e.last_name) as Employee,concat(c.first_name,' ',c.last_name) as Customer, tip, discount, invoice_total, invoice_datetime \
                            FROM employee e \
                            JOIN invoice i \
                                ON e.employee_id = i.employee_id \
                            JOIN customer c \
                                ON i.customer_id = c.customer_id \
                            WHERE i.active = 1;")
        rows = self.cursor.fetchall()
        return rows

    def getAllInvoiceInline(self):
        self.cursor.execute("SELECT i.invoice_id, concat(e.first_name,' ',e.last_name) as Employee, service_name,concat(c.first_name,' ',c.last_name) as Customer, tip, discount, invoice_total, invoice_datetime \
                            FROM employee e \
                            JOIN invoice i \
                                ON e.employee_id = i.employee_id \
                            JOIN customer c \
                                ON i.customer_id = c.customer_id \
                            JOIN invoice_line_item il \
                                ON i.invoice_id = il.invoice_id \
                            JOIN service s \
                                ON il.service_id = s.service_id \
                            WHERE i.active = 1;")
        rows = self.cursor.fetchall()
        return rows

    def SearchInvoice(self, invoiceId):
        self.cursor.execute("SELECT invoice_id, concat(e.first_name,' ',e.last_name) as Employee,concat(c.first_name,' ',c.last_name) as Customer, tip, discount, invoice_total, invoice_datetime \
                            FROM employee e \
                            JOIN invoice i \
                                ON e.employee_id = i.employee_id \
                            JOIN customer c \
                                ON i.customer_id = c.customer_id \
                            WHERE invoice_id = %s and i.active = 1;",
                            (invoiceId,))
        rows = self.cursor.fetchall()
        return rows

    def SearchInvoicebyCusF(self, CusF):
        print(CusF)
        self.cursor.execute("SELECT invoice_id, concat(e.first_name,' ',e.last_name) as Employee,concat(c.first_name,' ',c.last_name) as Customer, tip, discount, invoice_total, invoice_datetime \
                            FROM employee e \
                            JOIN invoice i \
                                ON e.employee_id = i.employee_id \
                            JOIN customer c \
                                ON i.customer_id = c.customer_id \
                            WHERE c.first_name LIKE '%"+CusF+"%' and i.active = 1;")
        rows = self.cursor.fetchall()
        return rows

    def SearchInvoicebyCusL(self, CusL):
        self.cursor.execute("SELECT invoice_id, concat(e.first_name,' ',e.last_name) as Employee,concat(c.first_name,' ',c.last_name) as Customer, tip, discount, invoice_total, invoice_datetime \
                            FROM employee e \
                            JOIN invoice i \
                                ON e.employee_id = i.employee_id \
                            JOIN customer c \
                                ON i.customer_id = c.customer_id \
                            WHERE c.last_name LIKE '%"+CusL+"%' and i.active = 1;")
        rows = self.cursor.fetchall()
        return rows

    def SearchInvoicebyEmpF(self, EmpF):
        self.cursor.execute("SELECT invoice_id, concat(e.first_name,' ',e.last_name) as Employee,concat(c.first_name,' ',c.last_name) as Customer, tip, discount, invoice_total, invoice_datetime \
                            FROM employee e \
                            JOIN invoice i \
                                ON e.employee_id = i.employee_id \
                            JOIN customer c \
                                ON i.customer_id = c.customer_id \
                            WHERE e.first_name LIKE '%"+EmpF+"%' and i.active = 1;")
        rows = self.cursor.fetchall()
        return rows

    def SearchInvoicebyEmpL(self, EmpL):
        self.cursor.execute("SELECT invoice_id, concat(e.first_name,' ',e.last_name) as Employee,concat(c.first_name,' ',c.last_name) as Customer, tip, discount, invoice_total, invoice_datetime \
                            FROM employee e \
                            JOIN invoice i \
                                ON e.employee_id = i.employee_id \
                            JOIN customer c \
                                ON i.customer_id = c.customer_id \
                            WHERE e.last_name LIKE '%"+EmpL+"%' and i.active = 1;")
        rows = self.cursor.fetchall()
        return rows

    def DeleteInvoice(self, invoice_id):
        self.cursor.execute("UPDATE invoice SET active = 0 WHERE invoice_id = %s", (invoice_id,))
        self.conn.commit()

    def InvoiceHistory(self):
        self.cursor.execute("SELECT invoice_id, concat(e.first_name,' ',e.last_name) as Employee,concat(c.first_name,' ',c.last_name) as Customer, tip, discount, invoice_total, invoice_datetime \
                            FROM employee e \
                            JOIN invoice i \
                                ON e.employee_id = i.employee_id \
                            JOIN customer c \
                                ON i.customer_id = c.customer_id \
                            WHERE i.active = 0;")
        rows = self.cursor.fetchall()
        return rows

    def SearchHInvoice(self, invoiceId):
        self.cursor.execute("SELECT invoice_id, concat(e.first_name,' ',e.last_name) as Employee,concat(c.first_name,' ',c.last_name) as Customer, tip, discount, invoice_total, invoice_datetime \
                            FROM employee e \
                            JOIN invoice i \
                                ON e.employee_id = i.employee_id \
                            JOIN customer c \
                                ON i.customer_id = c.customer_id \
                            WHERE invoice_id = %s and i.active = 0;",
                            (invoiceId,))
        rows = self.cursor.fetchall()
        return rows

    def SearchHInvoicebyCusF(self, CusF):
        print(CusF)
        self.cursor.execute("SELECT invoice_id, concat(e.first_name,' ',e.last_name) as Employee,concat(c.first_name,' ',c.last_name) as Customer, tip, discount, invoice_total, invoice_datetime \
                            FROM employee e \
                            JOIN invoice i \
                                ON e.employee_id = i.employee_id \
                            JOIN customer c \
                                ON i.customer_id = c.customer_id \
                            WHERE c.first_name LIKE '%"+CusF+"%' and i.active = 0;")
        rows = self.cursor.fetchall()
        return rows

    def SearchHInvoicebyCusL(self, CusL):
        self.cursor.execute("SELECT invoice_id, concat(e.first_name,' ',e.last_name) as Employee,concat(c.first_name,' ',c.last_name) as Customer, tip, discount, invoice_total, invoice_datetime \
                            FROM employee e \
                            JOIN invoice i \
                                ON e.employee_id = i.employee_id \
                            JOIN customer c \
                                ON i.customer_id = c.customer_id \
                            WHERE c.last_name LIKE '%"+CusL+"%' and i.active = 0;")
        rows = self.cursor.fetchall()
        return rows

    def SearchHInvoicebyEmpF(self, EmpF):
        self.cursor.execute("SELECT invoice_id, concat(e.first_name,' ',e.last_name) as Employee,concat(c.first_name,' ',c.last_name) as Customer, tip, discount, invoice_total, invoice_datetime \
                            FROM employee e \
                            JOIN invoice i \
                                ON e.employee_id = i.employee_id \
                            JOIN customer c \
                                ON i.customer_id = c.customer_id \
                            WHERE e.first_name LIKE '%"+EmpF+"%' and i.active = 0;")
        rows = self.cursor.fetchall()
        return rows

    def SearchHInvoicebyEmpL(self, EmpL):
        self.cursor.execute("SELECT invoice_id, concat(e.first_name,' ',e.last_name) as Employee,concat(c.first_name,' ',c.last_name) as Customer, tip, discount, invoice_total, invoice_datetime \
                            FROM employee e \
                            JOIN invoice i \
                                ON e.employee_id = i.employee_id \
                            JOIN customer c \
                                ON i.customer_id = c.customer_id \
                            WHERE e.last_name LIKE '%"+EmpL+"%' and i.active = 0;")
        rows = self.cursor.fetchall()
        return rows

    def SearchDetailsInvoice(self, invoiceId):
        self.cursor.execute("SELECT i.invoice_id, concat(e.first_name,' ',e.last_name) as Employee, service_name,concat(c.first_name,' ',c.last_name) as Customer, tip, discount, invoice_total, invoice_datetime \
                            FROM employee e \
                            JOIN invoice i \
                                ON e.employee_id = i.employee_id \
                            JOIN customer c \
                                ON i.customer_id = c.customer_id \
                            JOIN invoice_line_item il \
                                ON i.invoice_id = il.invoice_id \
                            JOIN service s \
                                ON il.service_id = s.service_id \
                            WHERE i.invoice_id = %s and i.active = 1;",
                            (invoiceId,))
        rows = self.cursor.fetchall()
        return rows

    def SearchDetailsInvoicebyCusF(self, CusF):
        print(CusF)
        self.cursor.execute("SELECT i.invoice_id, concat(e.first_name,' ',e.last_name) as Employee, service_name,concat(c.first_name,' ',c.last_name) as Customer, tip, discount, invoice_total, invoice_datetime \
                            FROM employee e \
                            JOIN invoice i \
                                ON e.employee_id = i.employee_id \
                            JOIN customer c \
                                ON i.customer_id = c.customer_id \
                            JOIN invoice_line_item il \
                                ON i.invoice_id = il.invoice_id \
                            JOIN service s \
                                ON il.service_id = s.service_id \
                            WHERE c.first_name LIKE '%"+CusF+"%' and i.active = 1;")
        rows = self.cursor.fetchall()
        return rows

    def SearchDetailsInvoicebyCusL(self, CusL):
        self.cursor.execute("SELECT i.invoice_id, concat(e.first_name,' ',e.last_name) as Employee, service_name,concat(c.first_name,' ',c.last_name) as Customer, tip, discount, invoice_total, invoice_datetime \
                            FROM employee e \
                            JOIN invoice i \
                                ON e.employee_id = i.employee_id \
                            JOIN customer c \
                                ON i.customer_id = c.customer_id \
                            JOIN invoice_line_item il \
                                ON i.invoice_id = il.invoice_id \
                            JOIN service s \
                                ON il.service_id = s.service_id \
                            WHERE c.last_name LIKE '%"+CusL+"%' and i.active = 1;")
        rows = self.cursor.fetchall()
        return rows

    def SearchDetailsInvoicebyEmpF(self, EmpF):
        self.cursor.execute("SELECT i.invoice_id, concat(e.first_name,' ',e.last_name) as Employee, service_name,concat(c.first_name,' ',c.last_name) as Customer, tip, discount, invoice_total, invoice_datetime \
                            FROM employee e \
                            JOIN invoice i \
                                ON e.employee_id = i.employee_id \
                            JOIN customer c \
                                ON i.customer_id = c.customer_id \
                            JOIN invoice_line_item il \
                                ON i.invoice_id = il.invoice_id \
                            JOIN service s \
                                ON il.service_id = s.service_id \
                            WHERE e.first_name LIKE '%"+EmpF+"%' and i.active = 1;")
        rows = self.cursor.fetchall()
        return rows

    def SearchDetailsInvoicebyEmpL(self, EmpL):
        self.cursor.execute("SELECT i.invoice_id, concat(e.first_name,' ',e.last_name) as Employee, service_name,concat(c.first_name,' ',c.last_name) as Customer, tip, discount, invoice_total, invoice_datetime \
                            FROM employee e \
                            JOIN invoice i \
                                ON e.employee_id = i.employee_id \
                            JOIN customer c \
                                ON i.customer_id = c.customer_id \
                            JOIN invoice_line_item il \
                                ON i.invoice_id = il.invoice_id \
                            JOIN service s \
                                ON il.service_id = s.service_id \
                            WHERE e.last_name LIKE '%"+EmpL+"%' and i.active = 1;")
        rows = self.cursor.fetchall()
        return rows

    def TotalSale(self):
        self.cursor.execute("SELECT SUM(invoice_total) FROM invoice WHERE date(invoice_datetime) = curdate() and active = 1;")
        row = self.cursor.fetchone()
        if row:
            return row[0]
        else:
            return None

    def SalaryReport(self, DateFrom, DateTo):
        self.cursor.execute("SELECT concat(e.first_name,' ',e.last_name) as Employee, SUM(tip), SUM(invoice_total), Round((SUM(invoice_total) * 0.6),2), Round((SUM(invoice_total) * 0.4),2) \
                            FROM employee e \
                            JOIN invoice i \
                                ON e.employee_id = i.employee_id \
                            JOIN customer c \
                                ON i.customer_id = c.customer_id\
                            WHERE DATE(i.invoice_datetime) BETWEEN %s AND %s AND i.active = 1\
                            GROUP BY Employee;",
                            (DateFrom,DateTo))
        rows = self.cursor.fetchall()
        return rows

    def CountInvReport(self, DateFrom, DateTo):
        self.cursor.execute("SELECT concat(e.first_name,' ',e.last_name) as Employee, COUNT(*)\
                            FROM employee e \
                            JOIN invoice i \
                            ON e.employee_id = i.employee_id \
                            WHERE DATE(i.invoice_datetime) BETWEEN %s AND %s AND i.active = 1 \
                            GROUP BY Employee;",
                            (DateFrom,DateTo))
        rows = self.cursor.fetchall()
        return rows

    def DiscountReport(self, DateFrom, DateTo):
        print(DateFrom, DateTo)
        self.cursor.execute("SELECT i.invoice_id, concat(e.first_name,' ',e.last_name) as Employee, concat(c.first_name,' ',c.last_name) as Customer, tip, discount, invoice_total, invoice_datetime \
                            FROM employee e \
                            JOIN invoice i \
                                ON e.employee_id = i.employee_id \
                            JOIN customer c \
                                ON i.customer_id = c.customer_id \
                            WHERE discount > 0 AND DATE(i.invoice_datetime) BETWEEN %s AND %s AND i.active = 1;",
                            (DateFrom,DateTo))
        rows = self.cursor.fetchall()
        return rows

    def RevenueReport(self, DateFrom, DateTo):
        print(DateFrom, DateTo)
        self.cursor.execute("SELECT SUM(invoice_total) \
                            FROM invoice \
                            WHERE DATE(invoice_datetime) BETWEEN %s AND %s AND active = 1;",
                            (DateFrom,DateTo))
        rows = self.cursor.fetchall()
        return rows
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
      


    # def addInvoice(self, invoice_number, employee_id, customer_id, invoice_total, invoice_datetime, payment_total, payment_datetime):
    #     self.cursor.execute("INSERT INTO invoice (invoice_number, employee_id, customer_id, invoice_total, invoice_datetime, payment_total, payment_datetime) VALUES (?, ?, ?, ?, ?, ?,?)",
    #                         (invoice_number, employee_id, customer_id, invoice_total, invoice_datetime, payment_total, payment_datetime))
    #     self.conn.commit()


    def removeInvoice(self, invoice_id):
        self.cursor.execute("UPDATE invoice SET active = 0 WHERE invoice_id = ?", (invoice_id,))
        self.conn.commit()


    def updateInvoice(self, invoice_id, invoice_number, employee_id, customer_id, invoice_total, invoice_datetime, payment_total, payment_datetime):
        self.cursor.execute("UPDATE invoice SET username = ?, password = ?, secret_question = ?, secret_answer = ?, role_id = ?, account_status_id = ? WHERE account_id = ?",
                            (invoice_number, employee_id, customer_id, invoice_total, invoice_datetime, payment_total, payment_datetime, invoice_id))
        self.conn.commit()


    def __del__(self):
        self.conn.close()