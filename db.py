import sqlite3

class Database:
    def __init__(self, db):
        # Establish the connection and create the cursor
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()

        # SQL query to create the employees table if it doesn't exist
        sql = """
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age TEXT,
            doj TEXT,
            email TEXT,
            gender TEXT,
            contact TEXT,
            address TEXT
        )
        """
        self.cur.execute(sql)  # Execute the query
        self.con.commit()  # Commit the changes

    def insert(self, name, age, doj, email, gender, contact, address):
        # Insert a new employee record
        self.cur.execute(
            "INSERT INTO employees VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)",
            (name, age, doj, email, gender, contact, address)
        )
        self.con.commit()

    def fetch(self):
        # Fetch all employee records
        self.cur.execute("SELECT * FROM employees")
        rows = self.cur.fetchall()
        return rows

    def remove(self, id):
        # Delete an employee record (corrected tuple syntax)
        self.cur.execute("DELETE FROM employees WHERE id = ?", (id,))
        self.con.commit()

    def update(self, id, name, age, doj, email, gender, contact, address):
        # Update an employee record
        self.cur.execute(
            """UPDATE employees 
               SET name = ?, age = ?, doj = ?, email = ?, 
                   gender = ?, contact = ?, address = ? 
               WHERE id = ?""",
            (name, age, doj, email, gender, contact, address, id)
        )
        self.con.commit()



