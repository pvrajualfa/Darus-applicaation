# Quick fix for the single file - rebuild with corrected database
import os
import sys
import subprocess

# Read the current single file
with open("Darus_complete_single.py", "r") as f:
    content = f.read()

# Fix the database.py section by moving get_all_heads inside the class
fixed_content = content.replace(
'''    def get_students(self):
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

    def get_vouchers(self):
        cur = self.conn.execute("SELECT * FROM vouchers ORDER BY date DESC")
        return cur.fetchall()

    def add_head(self, typ, head):
        self.conn.execute("INSERT INTO heads(type,name) VALUES(?,?)", (typ, head))
        self.conn.commit()

    def add_subhead(self, typ, head, sub):
        row = self.conn.execute("SELECT id FROM heads WHERE type=? AND name=?", (typ, head)).fetchone()
        if row:
            head_id = row[0]
            exists = self.conn.execute("SELECT id FROM subheads WHERE head_id=? AND name=?", (head_id, sub)).fetchone()
            if not exists:
                self.conn.execute("INSERT INTO subheads(head_id,name) VALUES(?,?)", (head_id, sub))
                self.conn.commit()''',
'''    def get_students(self):
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

    def get_vouchers(self):
        cur = self.conn.execute("SELECT * FROM vouchers ORDER BY date DESC")
        return cur.fetchall()

    def add_head(self, typ, head):
        self.conn.execute("INSERT INTO heads(type,name) VALUES(?,?)", (typ, head))
        self.conn.commit()

    def add_subhead(self, typ, head, sub):
        row = self.conn.execute("SELECT id FROM heads WHERE type=? AND name=?", (typ, head)).fetchone()
        if row:
            head_id = row[0]
            exists = self.conn.execute("SELECT id FROM subheads WHERE head_id=? AND name=?", (head_id, sub)).fetchone()
            if not exists:
                self.conn.execute("INSERT INTO subheads(head_id,name) VALUES(?,?)", (head_id, sub))
                self.conn.commit()'''
)

# Write the corrected file
with open("Darus_complete_single_fixed.py", "w") as f:
    f.write(fixed_content)

print("Created Darus_complete_single_fixed.py with corrected database class")

# Now build the EXE
cmd = [
    "pyinstaller",
    "--onefile",
    "--name=SchoolManagement_Working",
    "--hidden-import=sqlite3",
    "--clean",
    "Darus_complete_single_fixed.py"
]

print("Building working EXE...")
result = subprocess.run(cmd, capture_output=True, text=True)

if result.returncode == 0:
    print("EXE built successfully!")
    print("Location: dist/SchoolManagement_Working.exe")
else:
    print("Build failed:")
    print(result.stderr)
