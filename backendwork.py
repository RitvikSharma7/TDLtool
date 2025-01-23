import sqlite3

class TDLDB:

    def __init__(self, db_name="TDLDB.db"):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        self.c.execute("""
        CREATE TABLE IF NOT EXISTS Tasks (
            tasks TEXT
        )
        """)
        self.conn.commit()

    def add_task(self, task):
        self.c.execute("INSERT INTO Tasks (tasks) VALUES (?)", (task,))
        self.conn.commit()

    def del_task(self, task):
        self.c.execute("DELETE FROM Tasks WHERE tasks = ?", (task,))
        self.conn.commit()

    def all_tasks(self):
        self.c.execute("SELECT tasks FROM Tasks")
        return self.c.fetchall()
    
    def del_all_tasks(self):
        self.c.execute("DELETE FROM Tasks")
        self.conn.commit()

    def close_db(self):
        self.conn.close()