import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

print("Connecting to the PostgreSQL database...")
# Connect to the database using the URL from the environment variables
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

print("Reading schema.sql file...")
# Read the schema.sql file and execute the SQL commands within it
with open('schema.sql') as f:
    cur.execute(f.read())

print("Committing changes...")
# Commit the changes and close the connection
conn.commit()
cur.close()
conn.close()

print("PostgreSQL database initialized successfully.")