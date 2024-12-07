#!/usr/bin/python3
import sqlite3
import functools
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

#### decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = args[0]  # Assuming the first argument is the SQL query
        logging.info(f"Executing query: {query}")
        result = func(*args, **kwargs)
        logging.info("Query executed successfully")
        return result
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")