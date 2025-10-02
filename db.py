import sqlite3

def get_db_connection():
    """Establishes a connection to the database."""
    conn = sqlite3.connect('budget.db')
    # Enable foreign key constraint enforcement
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn

# =================================================================
#  Book Management Functions
# =================================================================

def get_books():
    """Fetches all books from the database."""
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books ORDER BY name').fetchall()
    conn.close()
    return books

def add_book(book_name):
    """Adds a new book to the database."""
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO books (name) VALUES (?)', (book_name,))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Book '{book_name}' already exists.")
    finally:
        conn.close()

def get_book_by_name(book_name):
    """Fetches a single book by its name."""
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE name = ?', (book_name,)).fetchone()
    conn.close()
    return book

def delete_book(book_id):
    """Deletes a book and all its associated transactions."""
    conn = get_db_connection()
    try:
        # Delete all associated income and expense records first
        conn.execute('DELETE FROM income WHERE book_id = ?', (book_id,))
        conn.execute('DELETE FROM expense WHERE book_id = ?', (book_id,))
        # Then, delete the book itself
        conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()


# =================================================================
#  Transaction Management Functions
# =================================================================

def get_transactions(transaction_type, book_id):
    """Fetches all records for a specific book."""
    conn = get_db_connection()
    transactions = conn.execute(f'SELECT * FROM {transaction_type} WHERE book_id = ?', (book_id,)).fetchall()
    conn.close()
    return transactions

def get_single_transaction(transaction_type, transaction_id):
    """Fetches a single transaction by its ID."""
    conn = get_db_connection()
    transaction = conn.execute(f'SELECT * FROM {transaction_type} WHERE id = ?', (transaction_id,)).fetchone()
    conn.close()
    return transaction


def add_transaction(transaction_type, data, book_id):
    """Adds a new transaction for a given book."""
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