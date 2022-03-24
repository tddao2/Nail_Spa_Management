import mysql.connector
from Backend.connection import Connect

class FeedbackDB:
    def __init__(self):
        self.conn = mysql.connector.connect(**Connect)
        self.cursor = self.conn.cursor()


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
        self.cursor.execute("UPDATE feedback SET active = 0 WHERE feedback_id = ?", (feedback_id,))
        self.conn.commit()


    def updateFeedback(self, feedback_id, employee_id, performance_score, description):
        self.cursor.execute("UPDATE feedback SET employee_id = ?, performance_score = ?, description = ? WHERE feedback_id = ?",
                            (employee_id, performance_score, description, feedback_id))
        self.conn.commit()


    def __del__(self):
        self.conn.close()