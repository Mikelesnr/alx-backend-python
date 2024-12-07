#!/usr/bin/python3
import mysql.connector
import decimal

"""
Please replace host,user,password with your server settings in DB_CONFIG
"""

DB_CONFIG = {
    'host': 'localhost',
    'user': 'user_name',
    'password': 'mysql_password',
    'database': 'ALX_prodev'
}

def connect_to_prodev():
    return mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database']
    )

def stream_user_ages():
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:
        if 'age' in row and isinstance(row['age'], decimal.Decimal):
            yield int(row['age'])
    cursor.close()
    connection.close()
