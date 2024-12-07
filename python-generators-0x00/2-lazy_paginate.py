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

def paginate_users(page_size, offset):
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows

def lazy_paginate(page_size):
    offset = 0
    while True:
        rows = paginate_users(page_size, offset)
        if not rows:
            break
        yield from rows
        offset += page_size