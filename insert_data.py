import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('mattress.db')
c = conn.cursor()

# Create tables
c.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    size TEXT NOT NULL,
    height REAL NOT NULL,
    type TEXT NOT NULL
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL,
    product_name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    status TEXT NOT NULL,
    price REAL NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products (id)
)
''')

# Insert data into the products table
products = [
    ('Ultra Comfort Mattress', 1299, 'Queen', 12, 'Hybrid (Memory Foam + Pocket Coils)'),
    ('Ultra Comfort Mattress', 1299, 'Twin', 12, 'Hybrid (Memory Foam + Pocket Coils)'),
    ('Ultra Comfort Mattress', 1299, 'Twin XL', 12, 'Hybrid (Memory Foam + Pocket Coils)'),
    ('Ultra Comfort Mattress', 1299, 'Full', 12, 'Hybrid (Memory Foam + Pocket Coils)'),
    ('Ultra Comfort Mattress', 1299, 'King', 12, 'Hybrid (Memory Foam + Pocket Coils)'),
    ('Ultra Comfort Mattress', 1299, 'California King', 12, 'Hybrid (Memory Foam + Pocket Coils)'),
    ('Dream Sleep Mattress', 899, 'Queen', 10, 'All-Foam'),
    ('Dream Sleep Mattress', 899, 'Twin', 10, 'All-Foam'),
    ('Dream Sleep Mattress', 899, 'Full', 10, 'All-Foam'),
    ('Dream Sleep Mattress', 899, 'King', 10, 'All-Foam'),
    ('Luxury Cloud Mattress', 1899, 'Queen', 14, 'Hybrid (Latex + Memory Foam + Coils)'),
    ('Luxury Cloud Mattress', 1899, 'Twin XL', 14, 'Hybrid (Latex + Memory Foam + Coils)'),
    ('Luxury Cloud Mattress', 1899, 'Full', 14, 'Hybrid (Latex + Memory Foam + Coils)'),
    ('Luxury Cloud Mattress', 1899, 'King', 14, 'Hybrid (Latex + Memory Foam + Coils)'),
    ('Luxury Cloud Mattress', 1899, 'California King', 14, 'Hybrid (Latex + Memory Foam + Coils)'),
    ('Luxury Cloud Mattress', 1899, 'Split King', 14, 'Hybrid (Latex + Memory Foam + Coils)'),
    ('Essential Plus Mattress', 699, 'Queen', 8, 'All-Foam'),
    ('Essential Plus Mattress', 699, 'Twin', 8, 'All-Foam'),
    ('Essential Plus Mattress', 699, 'Full', 8, 'All-Foam'),
    ('Performance Sport Mattress', 1499, 'Queen', 13, 'Hybrid (Performance Foam + Coils)'),
    ('Performance Sport Mattress', 1499, 'Twin XL', 13, 'Hybrid (Performance Foam + Coils)'),
    ('Performance Sport Mattress', 1499, 'Full', 13, 'Hybrid (Performance Foam + Coils)'),
    ('Performance Sport Mattress', 1499, 'King', 13, 'Hybrid (Performance Foam + Coils)'),
    ('Performance Sport Mattress', 1499, 'California King', 13, 'Hybrid (Performance Foam + Coils)')
]

c.executemany('''
INSERT INTO products (name, price, size, height, type)
VALUES (?, ?, ?, ?, ?)
''', products)

# Insert an order into the orders table
order = (1, 1, 'Ultra Comfort Mattress', 1, 'Pending', 1299)
c.execute('''
INSERT INTO orders (id, product_id, product_name, quantity, status, price)
VALUES (?, ?, ?, ?, ?, ?)
''', order)

# Commit the changes and close the connection
conn.commit()
conn.close()
