import sqlite3

# This script is used to initialize the database for the first time.

# Connect to the database file (it will be created if it doesn't exist)
connection = sqlite3.connect('budget.db')

# Read the schema.sql file and execute the SQL commands within it
with open('schema.sql') as f:
    connection.executescript(f.read())

# Commit the changes and close the connection
connection.commit()
connection.close()

print("Database 'budget.db' initialized successfully.")
