-- Delete existing tables to start fresh
DROP TABLE IF EXISTS income;
DROP TABLE IF EXISTS expense;
DROP TABLE IF EXISTS books;

-- Create the 'books' table to store different budget books
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- Create the 'income' table with a foreign key linking to the 'books' table
CREATE TABLE income (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    description TEXT NOT NULL,
    amount REAL NOT NULL,
    method TEXT NOT NULL,
    book_id INTEGER NOT NULL,
    FOREIGN KEY (book_id) REFERENCES books (id)
);

-- Create the 'expense' table with a foreign key linking to the 'books' table
CREATE TABLE expense (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    description TEXT NOT NULL,
    amount REAL NOT NULL,
    method TEXT NOT NULL,
    book_id INTEGER NOT NULL,
    FOREIGN KEY (book_id) REFERENCES books (id)
);

-- Insert a default book to start with
INSERT INTO books (name) VALUES ('Default Book');

