import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(os.path.join(DATA_DIR, "school.db"))
        self.create_tables()

    def create_tables(self):
        # Students table
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            name TEXT,
            father TEXT,
            aadhaar TEXT,
            dob TEXT,
            join_date TEXT,
            class TEXT,
            phone1 TEXT,
            phone2 TEXT,
            location TEXT,
            city TEXT,
            address TEXT,
            annual_fee REAL
        )
        """)

        # Heads table
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS heads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            name TEXT COLLATE NOCASE,
            UNIQUE(type, name)
        )
        """)

        # Subheads table
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS subheads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            head_id INTEGER,
            name TEXT COLLATE NOCASE,
            UNIQUE(head_id, name),
            FOREIGN KEY(head_id) REFERENCES heads(id)
        )       
        """)

        # Vouchers table
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS vouchers(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            type TEXT,
            head TEXT,
            subhead TEXT,
            student_name TEXT,
            class TEXT,
            amount REAL,
            mode TEXT,
            note TEXT
        )
        """)

        self.conn.commit()

    def add_student(self, student_id, name, father, aadhaar, dob, join_date, class_name, phone1, phone2, location, city, address, annual_fee):
        self.conn.execute("""
        INSERT INTO students(student_id, name, father, aadhaar, dob, join_date, class, phone1, phone2, location, city, address, annual_fee)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (student_id, name, father, aadhaar, dob, join_date, class_name, phone1, phone2, location, city, address, annual_fee))
        self.conn.commit()

    def get_students(self):
        cur = self.conn.execute("SELECT * FROM students ORDER BY name")
        return cur.fetchall()

    def get_all_heads(self):
        cur = self.conn.execute("SELECT id, type, name FROM heads ORDER BY type, name")
        return cur.fetchall()

    def get_heads(self, typ):
        cur = self.conn.execute("SELECT id, name FROM heads WHERE type=? ORDER BY name", (typ,))
        return cur.fetchall()

    def get_subheads_by_headid(self, head_id):
        cur = self.conn.execute("SELECT id, name FROM subheads WHERE head_id=? ORDER BY name", (head_id,))
        return cur.fetchall()

    def add_voucher(self, date, typ, head, subhead, student_name, class_name, amount, mode, note):
        self.conn.execute("""
        INSERT INTO vouchers(date, type, head, subhead, student_name, class, amount, mode, note)
        VALUES(?,?,?,?,?,?,?,?,?)
        """, (date, typ, head, subhead, student_name, class_name, amount, mode, note))
        self.conn.commit()

    def add_subhead(self, typ, head, sub):
        row = self.conn.execute("SELECT id FROM heads WHERE type=? AND name=?", (typ, head)).fetchone()
        if row:
            head_id = row[0]
            exists = self.conn.execute("SELECT id FROM subheads WHERE head_id=? AND name=?", (head_id, sub)).fetchone()
            if not exists:
                self.conn.execute("INSERT INTO subheads(head_id,name) VALUES(?,?)", (head_id, sub))
                self.conn.commit()

    def get_vouchers(self):
        cur = self.conn.execute("SELECT * FROM vouchers ORDER BY date DESC")
        return cur.fetchall()

    def add_head(self, typ, head):
        self.conn.execute("INSERT INTO heads(type,name) VALUES(?,?)", (typ, head))
        self.conn.commit()

    def get_total_paid(self, student_name):
        result = self.conn.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM vouchers WHERE student_name=? AND type='Income'",
            (student_name,)
        ).fetchone()
        return result[0] if result else 0
