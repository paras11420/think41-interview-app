import sqlite3
import pandas as pd

# Connect to SQLite DB (creates file if it doesn't exist)
conn = sqlite3.connect('ecommerce.db')

# Load CSVs into DataFrames
users_df = pd.read_csv('users.csv')
orders_df = pd.read_csv('orders.csv')

# Load into tables
users_df.to_sql('users', conn, if_exists='replace', index=False)
orders_df.to_sql('orders', conn, if_exists='replace', index=False)

# Verify with simple queries
print("Users Table (first 5 rows):")
print(pd.read_sql_query("SELECT * FROM users LIMIT 5", conn))

print("\nOrders Table (first 5 rows):")
print(pd.read_sql_query("SELECT * FROM orders LIMIT 5", conn))

conn.close()
