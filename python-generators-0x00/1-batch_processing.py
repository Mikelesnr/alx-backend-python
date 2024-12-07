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

def stream_users_in_batches(batch_size):
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    batch = []
    for row in cursor:
        if 'age' in row and isinstance(row['age'], decimal.Decimal):
            row['age'] = int(row['age'])
        batch.append(row)
        if len(batch) == batch_size:
            yield batch
            #these print statements are for checkinh if batch sizes change when I change the batch size
            # print(batch)
            # print('next batch')
            batch = []
    if batch:
        yield batch
    cursor.close()
    connection.close()

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        processed_batch = [user for user in batch if user['age'] > 25]
        for user in processed_batch:
            print(user)


