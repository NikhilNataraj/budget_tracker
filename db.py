import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    return conn


# =================================================================
#  User Management Functions
# =================================================================
def add_user(email, password_hash):
    conn = get_db_connection()
    cur = conn.cursor()
    user_id = None
    try:
        # Use RETURNING id to get the new user's ID
        cur.execute('INSERT INTO users (email, password_hash) VALUES (%s, %s) RETURNING id',
                    (email, password_hash))
        user_id = cur.fetchone()[0]
        conn.commit()
    except psycopg2.IntegrityError:
        print(f"User with email '{email}' already exists.")
        conn.rollback()  # Rollback the transaction on error
    finally:
        cur.close()
        conn.close()
    return user_id


def get_user_by_email(email):
    conn = get_db_connection()
    # Use DictCursor to get rows as dictionaries
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM users WHERE email = %s', (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user


def get_user_by_id(user_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user


# =================================================================
#  Book Management (User-Specific)
# =================================================================
def get_books(user_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM books WHERE user_id = %s ORDER BY name', (user_id,))
    books = cur.fetchall()
    cur.close()
    conn.close()
    return books


def add_book(book_name, user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO books (name, user_id) VALUES (%s, %s)', (book_name, user_id))
    conn.commit()
    cur.close()
    conn.close()


def get_book_by_name(book_name, user_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM books WHERE name = %s AND user_id = %s', (book_name, user_id))
    book = cur.fetchone()
    cur.close()
    conn.close()
    return book


def delete_book(book_id, user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    # The ON DELETE CASCADE in the schema handles deleting associated transactions
    cur.execute('DELETE FROM books WHERE id = %s AND user_id = %s', (book_id, user_id))
    conn.commit()
    cur.close()
    conn.close()


# =================================================================
#  Transactions Management
# =================================================================
def get_transactions(transaction_type, book_id, start_date=None, end_date=None):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Note: table names cannot be parameterized, so f-string is safe here
    query = f'SELECT * FROM {transaction_type} WHERE book_id = %s'
    params = [book_id]

    if start_date and end_date:
        query += ' AND date BETWEEN %s AND %s'
        params.extend([start_date, end_date])

    query += ' ORDER BY date DESC'

    cur.execute(query, tuple(params))
    transactions = cur.fetchall()
    cur.close()
    conn.close()
    return transactions


def get_single_transaction(transaction_type, transaction_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(f'SELECT * FROM {transaction_type} WHERE id = %s', (transaction_id,))
    transaction = cur.fetchone()
    cur.close()
    conn.close()
    return transaction


def add_transaction(transaction_type, data, book_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        f'INSERT INTO {transaction_type} (date, description, amount, method, book_id) VALUES (%s, %s, %s, %s, %s)',
        (data['date'], data['description'], data['amount'], data['method'], book_id))
    conn.commit()
    cur.close()
    conn.close()


def update_transaction(transaction_type, transaction_id, data):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f'UPDATE {transaction_type} SET date = %s, description = %s, amount = %s, method = %s WHERE id = %s',
                (data['date'], data['description'], data['amount'], data['method'], transaction_id))
    conn.commit()
    cur.close()
    conn.close()


def delete_transaction(transaction_type, transaction_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f'DELETE FROM {transaction_type} WHERE id = %s', (transaction_id,))
    conn.commit()
    cur.close()
    conn.close()