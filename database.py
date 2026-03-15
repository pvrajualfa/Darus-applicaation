import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "ui2", "data")
os.makedirs(DATA_DIR, exist_ok=True)


class Database:

    def __init__(self):
        self.conn = sqlite3.connect(os.path.join(DATA_DIR, "school.db"))
        self.create_tables()

    # ================= TABLES =================
    def create_tables(self):

        # -------- STUDENTS --------
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

        # -------- HEADS --------
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS heads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            name TEXT COLLATE NOCASE,
            UNIQUE(type, name)
        )
        """)

        # -------- SUBHEADS --------
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS subheads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            head_id INTEGER,
            name TEXT COLLATE NOCASE,
            UNIQUE(head_id, name),
            FOREIGN KEY(head_id) REFERENCES heads(id)
        )       
        """)

        # 🔒 Prevent duplicate subheads under same head
        self.conn.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS
            idx_subheads_headid_name
            ON subheads(head_id, name)
         """)
# -------- VOUCHERS --------
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS vouchers(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            type TEXT,
            head TEXT,
            sub TEXT,
            student TEXT,
            class TEXT,
            amount REAL,
            mode TEXT,
            note TEXT
        )
        """)

        self.conn.commit()

    # ================= HEADS =================
    def add_head(self, typ, head):
        self.conn.execute(
            "INSERT INTO heads(type,name) VALUES(?,?)",
            (typ, head)
        )
        self.conn.commit()

    def add_subhead(self, typ, head, sub):

        # Get Head ID
        row = self.conn.execute(
            "SELECT id FROM heads WHERE type=? AND name=?",
            (typ, head)
        ).fetchone()

        if not row:
            return

        head_id = row[0]

        # Check Subhead Exists
        exists = self.conn.execute(
            "SELECT id FROM subheads WHERE head_id=? AND name=?",
            (head_id, sub)
        ).fetchone()

        # Insert only if not exists
        if not exists:
            self.conn.execute(
                "INSERT INTO subheads(head_id,name) VALUES(?,?)",
                (head_id, sub)
            )
            self.conn.commit()

    def add_subhead_by_id(self, head_id, sub):

        sub = sub.strip().lower()

        self.conn.execute(
            "INSERT INTO subheads(head_id,name) VALUES(?,?)",
            (head_id, sub)
        )
        self.conn.commit()
    def get_heads(self, typ):
        cur = self.conn.execute(
            "SELECT name FROM heads WHERE type=?",
            (typ,)
        )
        return [r[0] for r in cur.fetchall()]

    def get_subheads_by_headid(self, head_id):

        cur = self.conn.execute("""
                                SELECT name
                                FROM subheads
                                WHERE head_id = ?
                                """, (head_id,))

        return [r[0] for r in cur.fetchall()]

    # ================= STUDENTS =================
    def next_student_id(self):
        cur = self.conn.execute("SELECT COUNT(*) FROM students")
        return f"S{cur.fetchone()[0] + 1:03}"

    def add_student(self, data):
        self.conn.execute("""
        INSERT INTO students(
            student_id,name,father,aadhaar,dob,join_date,class,
            phone1,phone2,location,city,address,annual_fee
        ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, data)
        self.conn.commit()

    def update_student(self, data):
        self.conn.execute("""
              UPDATE students
              SET name=?,
                  father=?,
                  aadhaar=?,
                  dob=?,
                  join_date=?,
                  class=?,
                  phone1=?,
                  phone2=?,
                  location=?,
                  city=?,
                  address=?,
                  annual_fee=?
              WHERE student_id = ?
              """, (
                  data[1], data[2], data[3], data[4], data[5],
                  data[6], data[7], data[8], data[9],
                  data[10], data[11], data[12], data[0]
              ))
        self.conn.commit()

    def update_voucher(self, vid, data):

        self.conn.execute("""
              UPDATE vouchers
              SET date=?,
                  type=?,
                  head=?,
                  subhead=?,
                  student=?,
                  class=?,
                  amount=?,
                  mode=?,
                  note=?
              WHERE id = ?
                          """, (*data, vid))

        self.conn.commit()
    def get_students(self):
        return self.conn.execute("SELECT * FROM students").fetchall()

    def delete_student(self, sid):
        self.conn.execute("DELETE FROM students WHERE student_id=?", (sid,))
        self.conn.commit()

    # ================= VOUCHERS =================
    def add_voucher(self, data):
        self.conn.execute("""
        INSERT INTO vouchers(
            date,type,head,sub,student,class,amount,mode,note
        ) VALUES(?,?,?,?,?,?,?,?,?)
        """, data)
        self.conn.commit()

    def get_vouchers(self):
        return self.conn.execute("SELECT * FROM vouchers").fetchall()

    # ================= TOTAL PAID =================
    def get_total_paid(self, student_name):
        cur = self.conn.execute("""
            SELECT IFNULL(SUM(amount),0)
            FROM vouchers
            WHERE student=? AND type='Income'
        """, (student_name,))
        return cur.fetchone()[0] or 0