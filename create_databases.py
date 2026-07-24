import sqlite3


def create_company():
    conn = sqlite3.connect("company.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS employees(
        id INTEGER PRIMARY KEY,
        name TEXT,
        department TEXT,
        salary INTEGER
    )
    """)

    cur.executemany(
        "INSERT INTO employees(name, department, salary) VALUES (?, ?, ?)",
        [
            ("Alice", "Engineering", 50000),
            ("Bob", "HR", 60000),
            ("Charlie", "Finance", 70000),
        ],
    )

    conn.commit()
    conn.close()


def create_sales():
    conn = sqlite3.connect("sales.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY,
        customer TEXT,
        amount REAL
    )
    """)

    cur.executemany(
        "INSERT INTO orders(customer, amount) VALUES (?, ?)",
        [
            ("Acme", 1250.5),
            ("Globex", 890),
            ("Initech", 4200.75),
        ],
    )

    conn.commit()
    conn.close()


def create_inventory():
    conn = sqlite3.connect("inventory.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY,
        name TEXT,
        price REAL,
        stock INTEGER
    )
    """)

    cur.executemany(
        "INSERT INTO products(name, price, stock) VALUES (?, ?, ?)",
        [
            ("Keyboard", 999, 15),
            ("Mouse", 499, 30),
            ("Monitor", 7999, 8),
        ],
    )

    conn.commit()
    conn.close()


def create_college():
    conn = sqlite3.connect("college.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY,
        name TEXT,
        branch TEXT,
        cgpa REAL
    )
    """)

    cur.executemany(
        "INSERT INTO students(name, branch, cgpa) VALUES (?, ?, ?)",
        [
            ("Aisha", "CSE", 8.8),
            ("Neha", "ECE-AI", 9.2),
            ("Riya", "IT", 8.5),
        ],
    )

    conn.commit()
    conn.close()


create_company()
create_sales()
create_inventory()
create_college()

print("All databases created successfully!")