import mysql.connector
from Backend.connection import Connect

class FeedbackDB:
    def __init__(self):
        self.conn = mysql.connector.connect(**Connect)
        self.cursor = self.conn.cursor()

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Haven't finished <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def AddFB(self,data):
        self.cursor.execute("INSERT INTO feedback(employee_id,performance_score,description,dateFB) values(%s,%s,%s,%s)",
                            (data[0],data[1],data[2],data[3]))
        self.conn.commit()

    def getAllFB(self):
        self.cursor.execute("SELECT feedback_id, concat(first_name,' ',last_name) as Name, performance_score, description, date_format(dateFB, '%b %d, %Y %h:%i:%s %p') as Date, a.active \
                            FROM employee e \
                            INNER JOIN feedback a  \
                                ON e.employee_id = a.employee_id \
                            WHERE a.active =1 \
                            order by Name ASC;")
        rows = self.cursor.fetchall()
        return rows

    def deleteMonthly(self, month):
        self.cursor.execute("SET SQL_SAFE_UPDATES = 0;")
        self.cursor.execute("UPDATE feedback \
                            SET active = 0 \
                            WHERE month(dateFB) = %s;",
                            (month,))
        self.cursor.execute("SET SQL_SAFE_UPDATES = 1;")              

        self.conn.commit()

    def deletePeriod(self, period):
        self.cursor.execute("SET SQL_SAFE_UPDATES = 0;")
        self.cursor.execute("UPDATE feedback \
                            SET active = 0 \
                            WHERE dateFB BETWEEN DATE(%s) AND DATE(%s);",
                            (period[0], period[1]))
        self.cursor.execute("SET SQL_SAFE_UPDATES = 1;")              

        self.conn.commit()
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    def getAllFeedback(self):
        self.cursor.execute("SELECT * FROM feedback WHERE active = 1")
        rows = self.cursor.fetchall()
        return rows

    
    def getFeedbackByEmployeeID(self, employee_id):
        self.cursor.execute("SELECT * FROM feedback WHERE employee_id = ? AND active = 1", (employee_id,))
        rows = self.cursor.fetchall()
        return rows


    def addFeedback(self, employee_id, performance_score, description):
        self.cursor.execute("INSERT INTO feedback (employee_id, performance_score, description) VALUES (?, ?, ?)",
                            (employee_id, performance_score, description))
        self.conn.commit()


    def removeFeedback(self, feedback_id):
        self.cursor.execute("UPDATE feedback SET active = 0 WHERE feedback_id = %s", (feedback_id,))
        self.conn.commit()


    def updateFeedback(self, feedback_id, employee_id, performance_score, description):
        self.cursor.execute("UPDATE feedback SET employee_id = ?, performance_score = ?, description = ? WHERE feedback_id = ?",
                            (employee_id, performance_score, description, feedback_id))
        self.conn.commit()


    def __del__(self):
        self.conn.close()