#!/usr/bin/python3

import sqlite3
import csv

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

#     # Create the users table
#     cursor.execute('''
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT NOT NULL,
#         email TEXT NOT NULL,
#         age INTEGER NOT NULL
#     )
#     ''')

#     with open('user_data.csv', 'r') as file:
#         reader = csv.reader(file)
#         next(reader)  # Skip the header row if there is one

#         # Insert each row into the users table
#         for row in reader:
#             cursor.execute('''
#             INSERT INTO users (name, email, age)
#             VALUES (?, ?, ?)
#             ''', (row[0], row[1], int(row[2])))


#     cursor.execute("SELECT * FROM users")
#     results = cursor.fetchall()
#     for row in results:
#         print(row)
