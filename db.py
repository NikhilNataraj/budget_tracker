import sqlite3

def get_db_connection():
    """Establishes a connection to the database."""
    conn = sqlite3.connect('budget.db')
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn

# =================================================================
#  User Management Functions
# =================================================================

def add_user(email, password_hash):
    """Adds a new user to the database."""
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
    """Fetches a user by their email address."""
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    """Fetches a user by their ID."""
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return user

# =================================================================
#  Book Management (User-Specific)
# =================================================================

def get_books(user_id):
    """Fetches all books for a specific user."""
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books WHERE user_id = ? ORDER BY name', (user_id,)).fetchall()
    conn.close()
    return books

def add_book(book_name, user_id):
    """Adds a new book for a specific user."""
    conn = get_db_connection()
    conn.execute('INSERT INTO books (name, user_id) VALUES (?, ?)', (book_name, user_id))
    conn.commit()
    conn.close()

def get_book_by_name(book_name, user_id):
    """Fetches a single book by its name for a specific user."""
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE name = ? AND user_id = ?', (book_name, user_id)).fetchone()
    conn.close()
    return book

def delete_book(book_id, user_id):
    """Deletes a book and its transactions, ensuring it belongs to the user."""
    conn = get_db_connection()
    try:
        # First, verify the book belongs to the user before deleting
        book = conn.execute('SELECT id FROM books WHERE id = ? AND user_id = ?', (book_id, user_id)).fetchone()
        if book:
            conn.execute('DELETE FROM income WHERE book_id = ?', (book_id,))
            conn.execute('DELETE FROM expense WHERE book_id = ?', (book_id,))
            conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
            conn.commit()
        else:
            print("Error: Attempt to delete a book not owned by the user.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

# =================================================================
#  Transactions Management (User and Book Specific)
# =================================================================

def get_transactions(transaction_type, book_id):
    """Fetches all transactions for a specific book."""
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