#!/usr/bin/python3

import mysql.connector
import decimal

"""
Please replace host,user,password with your server settings in DB_CONFIG
"""

DB_CONFIG = {
    'host': 'localhost',
    'user': 'mikelesnr',
    'password': 'Michael2331#',
    'database': 'ALX_prodev'
}

def connect_to_prodev():
    return mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database']
    )

def stream_users():
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    for row in cursor:
        # Convert Decimal objects to int
        if 'age' in row and isinstance(row['age'], decimal.Decimal):
            row['age'] = int(row['age'])
        yield row
    cursor.close()
    connection.close()

#test code used
# from itertools import islice
# stream_users = __import__('0-stream_users').stream_users

# # Iterate over the generator function and print only the first 6 rows
# for user in islice(stream_users(), 6):
#     print(user)