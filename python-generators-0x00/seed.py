#!/usr/bin/python3
import mysql.connector
import csv
import uuid

"""
Please replace host,user and password in DB_CONFIG with your own mysql server details
"""

DB_CONFIG = {
    'host': 'localhost',
    'user': 'mikelesnr',
    'password': 'Michael2331#',
    'database': 'ALX_prodev'
}

def connect_db():
    return mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password']
    )

def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    cursor.close()

def connect_to_prodev():
    return mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database']
    )


def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(3, 0) NOT NULL,
            INDEX (user_id)
        )
    """)
    cursor.close()

def insert_data(connection, csv_file):
    cursor = connection.cursor()
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            print(row)
            if len(row) != 3:
                print(f"Skipping row with unexpected number of columns: {row}")
                continue
            try:
                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (str(uuid.uuid4()), row[0], row[1], row[2]))
            except Exception as e:
                print(f"Error inserting row {row}: {e}")
    connection.commit()
    cursor.close()
