#!/usr/bin/python3

import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params):
        self.db_name = db_name
        self.query = query
        self.params = params
    
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query,self.params)
        return self.cursor
    
    def __exit__(self , exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.cursor.close()
        self.conn.close()

# Usage example (personal test notes for duture ref)
# query = "SELECT * FROM users WHERE age = ?"
# params = (27,)

# with ExecuteQuery('example.db', query, params) as cursor:
#     results = cursor.fetchall()
#     for row in results:
#         print(row)
