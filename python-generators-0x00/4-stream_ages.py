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

def stream_user_ages():
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:
        if 'age' in row and isinstance(row['age'], decimal.Decimal):
            yield int(row['age'])
    cursor.close()
    connection.close()

def calculate_average_age():
    total_age = 0
    count = 0
    for age in stream_user_ages():
        total_age += age  # Using the + operator to sum ages
        count += 1
    if count == 0:
        return 0  # Avoid division by zero
    return total_age / count

# Print the average age
average_age = calculate_average_age()
print(f"Average age of users: {average_age:.2f}")
