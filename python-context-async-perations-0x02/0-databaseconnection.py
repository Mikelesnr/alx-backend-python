#!/usr/bin/python3

import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.cursor.close()
        self.conn.close()

# Usage example (my personal testing note for future reference)
# with DatabaseConnection('example.db') as cursor:
#     cursor.execute("SELECT * FROM users")
#     results = cursor.fetchall()
#     for row in results:
#         print(row)
