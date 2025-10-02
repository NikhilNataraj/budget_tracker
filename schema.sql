-- Drop tables in reverse order of dependency
DROP TABLE IF EXISTS income;
DROP TABLE IF EXISTS expense;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS users;


-- Create the 'users' table to store user credentials
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
);

-- Create the 'books' table, now linked to a user
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Create the 'income' table, linked to a book
CREATE TABLE income (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    description TEXT NOT NULL,
    amount REAL NOT NULL,
    method TEXT NOT NULL,
    book_id INTEGER NOT NULL,
    FOREIGN KEY (book_id) REFERENCES books (id)
);

-- Create the 'expense' table, linked to a book
CREATE TABLE expense (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    description TEXT NOT NULL,
    amount REAL NOT NULL,
    method TEXT NOT NULL,
    book_id INTEGER NOT NULL,
    FOREIGN KEY (book_id) REFERENCES books (id)
);