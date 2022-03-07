import mysql.connector

class FeedbackDB:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host: "cis4375.csummbr3vhgu.us-east-2.rds.amazonaws.com",
            user: "admin",
            password: "cis4375spring2022",
            db: "cis4375db",
            raise_on_warnings: True
        )
        self.cursor = self.conn.cursor()


    def fetch(self):
        self.cursor.execute("SELECT * FROM feedback WHERE active = 1")
        rows = self.cursor.fetchall()
        return rows


    def insert(self, employee_id, performance_score, description):
        self.cursor.execute("INSERT INTO feedback (employee_id, performance_score, description) VALUES (?, ?, ?)",
                            (employee_id, performance_score, description))
        self.conn.commit()


    def remove(self, feedback_id):
        self.cursor.execute("UPDATE feedback SET active = 0 WHERE feedback_id = ?", (feedback_id,))
        self.conn.commit()


    def update(self, feedback_id, employee_id, performance_score, description):
        self.cursor.execute("UPDATE feedback SET employee_id = ?, performance_score = ?, description = ? WHERE feedback_id = ?",
                            (employee_id, performance_score, description, feedback_id))
        self.conn.commit()


    def __del__(self):
        self.conn.close()