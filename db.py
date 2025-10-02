import sqlite3


def get_db_connection():
    """Establishes a connection to the database."""
    conn = sqlite3.connect('budget.db')
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


# =================================================================
#  User Management Functions (No changes here)
# =================================================================
def add_user(email, password_hash):
    conn = get_db_connection()
    user_id = None
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (email, password_hash) VALUES (?, ?)', (email, password_hash))
        user_id = cursor.lastrowid
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"User with email '{email}' already exists.")
    finally:
        conn.close()
    return user_id


def get_user_by_email(email):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()
    return user


def get_user_by_id(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return user


# =================================================================
#  Book Management (No changes here)
# =================================================================
def get_books(user_id):
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books WHERE user_id = ? ORDER BY name', (user_id,)).fetchall()
    conn.close()
    return books


def add_book(book_name, user_id):
    conn = get_db_connection()
    conn.execute('INSERT INTO books (name, user_id) VALUES (?, ?)', (book_name, user_id))
    conn.commit()
    conn.close()


def get_book_by_name(book_name, user_id):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE name = ? AND user_id = ?', (book_name, user_id)).fetchone()
    conn.close()
    return book


def delete_book(book_id, user_id):
    conn = get_db_connection()
    try:
        book = conn.execute('SELECT id FROM books WHERE id = ? AND user_id = ?', (book_id, user_id)).fetchone()
        if book:
            conn.execute('DELETE FROM income WHERE book_id = ?', (book_id,))
            conn.execute('DELETE FROM expense WHERE book_id = ?', (book_id,))
            conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()


# =================================================================
#  Transactions Management (UPDATED FOR FILTERING)
# =================================================================

def get_transactions(transaction_type, book_id, start_date=None, end_date=None):
    """
    Fetches all transactions for a specific book, with optional date filtering.
    """
    conn = get_db_connection()
    query = f'SELECT * FROM {transaction_type} WHERE book_id = ?'
    params = [book_id]

    if start_date and end_date:
        query += ' AND date BETWEEN ? AND ?'
        params.extend([start_date, end_date])

    query += ' ORDER BY date DESC'  # Sort by most recent

    transactions = conn.execute(query, tuple(params)).fetchall()
    conn.close()
    return transactions


def get_single_transaction(transaction_type, transaction_id):
    """Fetches a single transaction by its ID."""
    conn = get_db_connection()
    transaction = conn.execute(f'SELECT * FROM {transaction_type} WHERE id = ?', (transaction_id,)).fetchone()
    conn.close()
    return transaction


def add_transaction(transaction_type, data, book_id):
    """Adds a new transaction to a specific book."""
    conn = get_db_connection()
    conn.execute(f'INSERT INTO {transaction_type} (date, description, amount, method, book_id) VALUES (?, ?, ?, ?, ?)',
                 (data['date'], data['description'], data['amount'], data['method'], book_id))
    conn.commit()
    conn.close()


def update_transaction(transaction_type, transaction_id, data):
    """Updates an existing transaction."""
    conn = get_db_connection()
    conn.execute(f'UPDATE {transaction_type} SET date = ?, description = ?, amount = ?, method = ? WHERE id = ?',
                 (data['date'], data['description'], data['amount'], data['method'], transaction_id))
    conn.commit()
    conn.close()


def delete_transaction(transaction_type, transaction_id):
    """Deletes a transaction by its ID."""
    conn = get_db_connection()
    conn.execute(f'DELETE FROM {transaction_type} WHERE id = ?', (transaction_id,))
    conn.commit()
    conn.close()