import mysql.connector
from Backend.connection import Connect

class FeedbackDB:
    def __init__(self):
        self.cnx = mysql.connector.connect(**Connect)
        self.cursor = self.cnx.cursor(buffered=True)

    def EmpfetchAll(self):
        self.cursor.execute("SELECT employee_id, concat(first_name,' ',last_name) as Name \
                            FROM employee \
                            ORDER BY Name ASC")
        rows = self.cursor.fetchall()
        return rows

    def AddFB(self,data):
        self.cursor.execute("INSERT INTO feedback(employee_id,performance_score,description,dateFB) values(%s,%s,%s,%s)",
                            (data[0],data[1],data[2],data[3]))
        self.cnx.commit()