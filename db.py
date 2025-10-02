import sqlite3

def get_db_connection():
    """Establishes a connection to the database."""
    conn = sqlite3.connect('budget.db')
    # Return rows as dictionaries
    conn.row_factory = sqlite3.Row
    return conn

def get_transactions(transaction_type):
    """
    Fetches all records from a given table (income or expense).
    :param transaction_type: 'income' or 'expense'
    :return: A list of all transactions.
    """
    conn = get_db_connection()
    transactions = conn.execute(f'SELECT * FROM {transaction_type}').fetchall()
    conn.close()
    return transactions

def get_single_transaction(transaction_type, transaction_id):
    """
    Fetches a single transaction by its ID.
    :param transaction_type: 'income' or 'expense'
    :param transaction_id: The ID of the transaction to fetch.
    :return: A single transaction object.
    """
    conn = get_db_connection()
    transaction = conn.execute(f'SELECT * FROM {transaction_type} WHERE id = ?',
                               (transaction_id,)).fetchone()
    conn.close()
    return transaction


def add_transaction(transaction_type, data):
    """
    Adds a new transaction to the specified table.
    :param transaction_type: 'income' or 'expense'
    :param data: A dictionary containing transaction details.
    """
    conn = get_db_connection()
    conn.execute(f'INSERT INTO {transaction_type} (date, description, amount, method) VALUES (?, ?, ?, ?)',
                 (data['date'], data['description'], data['amount'], data['method']))
    conn.commit()
    conn.close()

def update_transaction(transaction_type, transaction_id, data):
    """
    Updates an existing transaction.
    :param transaction_type: 'income' or 'expense'
    :param transaction_id: The ID of the transaction to update.
    :param data: A dictionary with the new data.
    """
    conn = get_db_connection()
    conn.execute(f'UPDATE {transaction_type} SET date = ?, description = ?, amount = ?, method = ? WHERE id = ?',
                 (data['date'], data['description'], data['amount'], data['method'], transaction_id))
    conn.commit()
    conn.close()

def delete_transaction(transaction_type, transaction_id):
    """
    Deletes a transaction by its ID.
    :param transaction_type: 'income' or 'expense'
    :param transaction_id: The ID of the transaction to delete.
    """
    conn = get_db_connection()
    conn.execute(f'DELETE FROM {transaction_type} WHERE id = ?', (transaction_id,))
    conn.commit()
    conn.close()
