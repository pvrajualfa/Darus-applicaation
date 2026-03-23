import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(os.path.join(DATA_DIR, "school.db"))
        self.create_tables()
        # Update existing students to current academic year
        self.update_existing_students_academic_year()

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
        
        # Add academic_year column if it doesn't exist
        try:
            self.conn.execute("ALTER TABLE students ADD COLUMN academic_year TEXT")
            print("Added academic_year column to students table")
        except sqlite3.OperationalError:
            # Column already exists
            pass

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

    def add_student(self, student_id, name, father, aadhaar, dob, join_date, class_name, phone1, phone2, location, city, address, annual_fee, academic_year):
        self.conn.execute("""
        INSERT INTO students(student_id, name, father, aadhaar, dob, join_date, class, phone1, phone2, location, city, address, annual_fee, academic_year)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (student_id, name, father, aadhaar, dob, join_date, class_name, phone1, phone2, location, city, address, annual_fee, academic_year))
        self.conn.commit()

    def get_students(self, academic_year=None):
        if academic_year:
            cur = self.conn.execute("SELECT * FROM students WHERE academic_year=? ORDER BY name", (academic_year,))
        else:
            cur = self.conn.execute("SELECT * FROM students ORDER BY name")
        return cur.fetchall()

    def get_students_by_academic_year(self, academic_year):
        """Get students for a specific academic year"""
        cur = self.conn.execute("SELECT * FROM students WHERE academic_year=? ORDER BY name", (academic_year,))
        return cur.fetchall()

    def update_all_students_to_2025_2026(self):
        """Update all students to 2025-2026 academic year"""
        academic_year = "2025-2026"
        self.conn.execute("""
        UPDATE students SET academic_year=?
        """, (academic_year,))
        self.conn.commit()
        print(f"Updated all students to academic year: {academic_year}")

    def update_existing_students_academic_year(self):
        """Update existing students to current academic year if academic_year is NULL"""
        from PySide6.QtCore import QDate
        current_date = QDate.currentDate()
        if current_date.month() >= 6:  # June or later
            current_year = current_date.year()
            academic_year = f"{current_year}-{current_year+1}"
        else:  # Before June
            academic_year = f"{current_date.year()-1}-{current_date.year()}"
        
        self.conn.execute("""
        UPDATE students SET academic_year=? WHERE academic_year IS NULL OR academic_year=''
        """, (academic_year,))
        self.conn.commit()

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
