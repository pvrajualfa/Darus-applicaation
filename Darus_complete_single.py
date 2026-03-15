import os, pathlib, sys
from importlib import import_module

TARGET = pathlib.Path(os.getcwd())/"ui2"

# Complete single-file application with all updated code
FILES = {
    "__init__.py": "",
    
    "header.py": '''from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt

class PageHeader(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedHeight(45)
        self.setStyleSheet("""
            background:#2F80ED;
            color:white;
            font-size:20px;
            font-weight:bold;
            padding:8px;
        """)
''',

    "database.py": '''import sqlite3
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

    def get_all_heads(self):
        cur = self.conn.execute("SELECT id, type, name FROM heads ORDER BY type, name")
        return cur.fetchall()

    def get_vouchers(self):
        cur = self.conn.execute("SELECT * FROM vouchers ORDER BY date DESC")
        return cur.fetchall()

    def add_head(self, typ, head):
        self.conn.execute("INSERT INTO heads(type,name) VALUES(?,?)", (typ, head))
        self.conn.commit()
''',

    "common_form.py": '''from PySide6.QtWidgets import QLineEdit, QComboBox, QPushButton, QDateEdit, QLabel, QGroupBox
from PySide6.QtCore import Qt, Signal, QObject

class DataManager(QObject):
    student_updated = Signal()
    class_updated = Signal()

data_manager = DataManager()

def format_text_for_db(text):
    return text.strip().replace("'", "''")

# Enhanced widgets
class EnhancedLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(34)

class EnhancedComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(34)

class EnhancedDateEdit(QDateEdit):
    def __init__(self, date, parent=None, calendarPopup=False):
        super().__init__(date, parent)
        self.setCalendarPopup(calendarPopup)

# Styling functions
def style_lineedit(widget):
    widget.setMinimumHeight(34)
    widget.setStyleSheet("""
        QLineEdit {
            border:1px solid #d0d0d0;
            border-radius:6px;
            padding-left:6px;
            background:white;
            color: #333333;
        }
        QLineEdit:focus {
            border:2px solid #2F80ED;
        }
    """)

def style_combo(widget):
    widget.setMinimumHeight(34)
    widget.setStyleSheet("""
        QComboBox {
            border:1px solid #d0d0d0;
            border-radius:6px;
            padding-left:6px;
            background:white;
            color: #333333;
            min-height: 34px;
        }
        QComboBox:focus {
            border:2px solid #2F80ED;
        }
        QComboBox QAbstractItemView {
            background-color: white;
            border: 1px solid #d0d0d0;
            selection-background-color: #e3f2fd;
            selection-color: #1976d2;
            color: #333333;
        }
        QComboBox QAbstractItemView::item {
            padding: 5px;
            border: none;
            min-height: 20px;
        }
        QComboBox QAbstractItemView::item:selected {
            background-color: #e3f2fd;
            color: #1976d2;
        }
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left: 1px solid #d0d0d0;
        }
        QComboBox::down-arrow {
            width: 8px;
            height: 8px;
            background-color: #36ABD6;
        }
        QComboBox::down-arrow:hover,
        QComboBox::down-arrow:pressed {
            background-color: #1D4ED8;
        }
    """)

def style_button(btn):
    btn.setMinimumHeight(36)
    btn.setStyleSheet("""
        QPushButton {
            background:#36ABD6;
            color:white;
            border:none;
            border-radius:6px;
            font-weight:bold;
            padding:8px 16px;
        }
        QPushButton:hover {
            background:#1D4ED8;
        }
        QPushButton:pressed {
            background:#0F3D91;
        }
    """)

def style_dateedit(widget):
    widget.setMinimumHeight(34)
    widget.setStyleSheet("""
        QDateEdit {
            border:1px solid #d0d0d0;
            border-radius:6px;
            padding-left:6px;
            background:white;
            color: #333333;
        }
        QDateEdit:focus {
            border:2px solid #2F80ED;
        }
        QDateEdit::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left: 1px solid #d0d0d0;
        }
        QDateEdit::down-arrow {
            width: 8px;
            height: 8px;
            background-color: #36ABD6;
        }
        QDateEdit::down-arrow:hover,
        QDateEdit::down-arrow:pressed {
            background-color: #1D4ED8;
        }
        QCalendarWidget {
            background-color: white;
            color: #333333;
            font-size: 12px;
        }
        QCalendarWidget QAbstractItemView {
            background-color: white;
            color: #333333;
            selection-background-color: #36ABD6;
            selection-color: white;
        }
        QCalendarWidget QToolButton {
            background-color: #f8f9fa;
            color: #333333;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            padding: 4px 8px;
            font-weight: bold;
            min-width: 80px;
        }
        QCalendarWidget QToolButton:hover {
            background-color: #e3f2fd;
            color: #1976d2;
        }
        QCalendarWidget QToolButton::menu-indicator {
            width: 0px;
        }
        QCalendarWidget QSpinBox {
            background-color: white;
            color: #333333;
            border: 1px solid #d0d0d0;
            border-radius: 4px;
            padding: 2px 4px;
        }
        QCalendarWidget QSpinBox::up-button,
        QCalendarWidget QSpinBox::down-button {
            width: 20px;
            background-color: #f8f9fa;
            border-left: 1px solid #d0d0d0;
        }
        QCalendarWidget QSpinBox::up-button:hover,
        QCalendarWidget QSpinBox::down-button:hover {
            background-color: #e3f2fd;
        }
    """)

def style_label(widget):
    widget.setStyleSheet("""
        QLabel {
            font-weight:bold;
            color: #36ABD6;
            font-size: 13px;
            padding: 2px 0px;
        }
    """)

def style_groupbox(box):
    box.setStyleSheet("""
        QGroupBox {
            background:white;
            border:1px solid #e5e7eb;
            border-radius:10px;
            margin-top:10px;
            padding:10px;
            font-weight:bold;
            color: #333333;
        }
        QGroupBox:title {
            subcontrol-origin: margin;
            left:10px;
            padding:0 3px;
            color: #36ABD6;
            font-weight: bold;
        }
    """)

# Data loading functions
def load_students_into_combo(combo, db):
    combo.clear()
    combo.addItem("Select Student", None)
    students = db.get_students()
    for student in students:
        combo.addItem(f"{student[1]} - {student[2]}", student)

def load_heads_into_combo(combo, db, typ=None):
    combo.clear()
    combo.addItem("Select Head", None)
    heads = db.get_heads(typ) if typ else db.get_all_heads()
    for head in heads:
        combo.addItem(head[1], head[0])

def load_subheads_into_combo(combo, db, head_id):
    combo.clear()
    combo.addItem("Select Subhead", None)
    if head_id:
        subheads = db.get_subheads_by_headid(head_id)
        for subhead in subheads:
            combo.addItem(subhead[1], subhead[0])

def load_payment_modes_into_combo(combo):
    combo.clear()
    combo.addItems(["Cash", "Bank", "UPI", "Cheque"])

def load_classes_into_combo(combo):
    combo.clear()
    combo.addItems(["6th", "7th", "8th", "9th", "10th"])
''',

    "common_table.py": '''from PySide6.QtWidgets import QHeaderView, QAbstractItemView
from PySide6.QtCore import Qt

def style_table(table):
    header = table.horizontalHeader()
    header.setSectionResizeMode(QHeaderView.Stretch)
    header.setStyleSheet("""
        QHeaderView::section {
            font-weight: bold;
            padding: 8px;
            background-color: #f8f9fa;
            border: 1px solid #e0e0e0;
            color: #333333;
        }
    """)

    table.verticalHeader().setVisible(False)
    table.setAlternatingRowColors(True)
    table.setSortingEnabled(True)
    table.setEditTriggers(QAbstractItemView.NoEditTriggers)
    table.horizontalHeader().setSortIndicatorShown(True)
    table.setSelectionBehavior(QAbstractItemView.SelectRows)

    table.setStyleSheet("""
        QTableWidget {
            background-color: white;
            alternate-background-color: #f8f9fa;
            gridline-color: #e0e0e0;
            color: #333333;
            border: 1px solid #e0e0e0;
        }
        QTableWidget::item {
            padding: 5px;
            border-bottom: 1px solid #e0e0e0;
        }
        QTableWidget::item:selected {
            background-color: #e3f2fd;
            color: #1976d2;
        }
        QTableWidget::item:hover {
            background-color: #f5f5f5;
        }
    """)

    for r in range(table.rowCount()):
        for c in range(table.columnCount()):
            it = table.item(r, c)
            if it:
                it.setTextAlignment(Qt.AlignCenter)
''',

    "mainwindow.py": '''from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from ui2.header import PageHeader
from ui2.vouchers import VoucherPage
from ui2.reports import ReportPage
from ui2.heads import HeadPage
from ui2.student_list import StudentListPage
from ui2.student_registration import StudentRegistration

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 1200, 800)
        
        # Apply light theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout(central_widget)
        
        # Navigation
        nav_layout = QHBoxLayout()
        
        # Navigation buttons
        self.btn_vouchers = QPushButton("Vouchers")
        self.btn_reports = QPushButton("Reports")
        self.btn_heads = QPushButton("Manage Heads")
        self.btn_students = QPushButton("Students")
        self.btn_registration = QPushButton("Student Registration")
        
        # Style navigation buttons
        for btn in [self.btn_vouchers, self.btn_reports, self.btn_heads, self.btn_students, self.btn_registration]:
            btn.setMinimumHeight(40)
            btn.setStyleSheet("""
                QPushButton {
                    background: white;
                    border: 1px solid #e0e0e0;
                    border-radius: 6px;
                    padding: 8px 16px;
                    font-weight: bold;
                    color: #333333;
                }
                QPushButton:hover {
                    background: #f8f9fa;
                    border-color: #36ABD6;
                    color: #36ABD6;
                }
            """)
        
        nav_layout.addWidget(self.btn_vouchers)
        nav_layout.addWidget(self.btn_reports)
        nav_layout.addWidget(self.btn_heads)
        nav_layout.addWidget(self.btn_students)
        nav_layout.addWidget(self.btn_registration)
        nav_layout.addStretch()
        
        layout.addLayout(nav_layout)
        
        # Stack widget for pages
        self.stack = QStackedWidget()
        layout.addWidget(self.stack)
        
        # Create pages
        self.voucher_page = VoucherPage()
        self.report_page = ReportPage()
        self.head_page = HeadPage()
        self.student_list_page = StudentListPage()
        self.registration_page = StudentRegistration()
        
        # Add pages to stack
        self.stack.addWidget(self.voucher_page)
        self.stack.addWidget(self.report_page)
        self.stack.addWidget(self.head_page)
        self.stack.addWidget(self.student_list_page)
        self.stack.addWidget(self.registration_page)
        
        # Connect signals
        self.btn_vouchers.clicked.connect(lambda: self.stack.setCurrentWidget(self.voucher_page))
        self.btn_reports.clicked.connect(lambda: self.stack.setCurrentWidget(self.report_page))
        self.btn_heads.clicked.connect(lambda: self.stack.setCurrentWidget(self.head_page))
        self.btn_students.clicked.connect(lambda: self.stack.setCurrentWidget(self.student_list_page))
        self.btn_registration.clicked.connect(lambda: self.stack.setCurrentWidget(self.registration_page))
        
        # Set default page
        self.stack.setCurrentWidget(self.voucher_page)
''',

    "vouchers.py": '''from ui2.common_table import style_table
from PySide6.QtWidgets import *
from PySide6.QtCore import QDate, Qt, Signal
from ui2.database import Database
from ui2.header import PageHeader
from ui2.common_form import (style_dateedit, format_text_for_db, EnhancedLineEdit, EnhancedComboBox, EnhancedDateEdit, 
                              style_lineedit, style_combo, style_button, style_label, data_manager, load_students_into_combo, 
                              load_heads_into_combo, load_subheads_into_combo, load_payment_modes_into_combo)

class VoucherPage(QWidget):
    voucher_saved = Signal()
    
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.backend = None
        self.edit_voucher_id = None
        
        # Apply light theme
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                color: #333333;
            }
            QFrame {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
            QLabel {
                color: #333333;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.addWidget(PageHeader("Voucher Entry"))

        # Create a card frame for the form
        card = QFrame()
        form = QFormLayout(card)
        form.setSpacing(12)

        self.date = EnhancedDateEdit(QDate.currentDate(), calendarPopup=True)
        style_dateedit(self.date)
        self.date.setDisplayFormat("dd/MM/yyyy")
        
        self.type_combo = EnhancedComboBox()
        style_combo(self.type_combo)
        self.type_combo.addItems(["Select Income/Expense", "Income", "Expense"])

        self.head = EnhancedComboBox()
        style_combo(self.head)
        self.subhead = EnhancedComboBox()
        style_combo(self.subhead)

        self.student_lbl = QLabel("Student")
        style_label(self.student_lbl)
        self.student_combo = EnhancedComboBox()
        style_combo(self.student_combo)

        self.class_lbl = QLabel("Class")
        style_label(self.class_lbl)
        self.class_edit = EnhancedLineEdit()
        style_lineedit(self.class_edit)
        self.class_edit.setReadOnly(True)

        self.amount = EnhancedLineEdit()
        style_lineedit(self.amount)
        self.mode = EnhancedComboBox()
        style_combo(self.mode)
        self.note = EnhancedLineEdit()
        style_lineedit(self.note)

        # Add labels
        date_lbl = QLabel("Date")
        style_label(date_lbl)
        type_lbl = QLabel("Type")
        style_label(type_lbl)
        head_lbl = QLabel("Head")
        style_label(head_lbl)
        subhead_lbl = QLabel("Subhead")
        style_label(subhead_lbl)
        amount_lbl = QLabel("Amount")
        style_label(amount_lbl)
        mode_lbl = QLabel("Mode")
        style_label(mode_lbl)
        note_lbl = QLabel("Note")
        style_label(note_lbl)
        
        form.addRow(date_lbl, self.date)
        form.addRow(type_lbl, self.type_combo)
        form.addRow(head_lbl, self.head)
        form.addRow(subhead_lbl, self.subhead)
        form.addRow(self.student_lbl, self.student_combo)
        form.addRow(self.class_lbl, self.class_edit)
        form.addRow(amount_lbl, self.amount)
        form.addRow(mode_lbl, self.mode)
        form.addRow(note_lbl, self.note)

        layout.addWidget(card)

        btn_row = QHBoxLayout()
        btn_save = QPushButton("Save")
        btn_print = QPushButton("Print")
        btn_new = QPushButton("New")
        style_button(btn_save)
        style_button(btn_print)
        style_button(btn_new)

        btn_row.addWidget(btn_save)
        btn_row.addWidget(btn_print)
        btn_row.addWidget(btn_new)
        layout.addLayout(btn_row)

        # Table
        self.table = QTableWidget()
        style_table(self.table)
        layout.addWidget(self.table)

        # Connections
        btn_save.clicked.connect(self.save_voucher)
        btn_new.clicked.connect(self.clear_form)
        self.type_combo.currentTextChanged.connect(self.load_heads)
        self.head.currentIndexChanged.connect(self.load_subheads)
        self.student_combo.currentIndexChanged.connect(self.load_student_class)

        # Hide student section initially
        self.student_lbl.setVisible(False)
        self.student_combo.setVisible(False)
        self.class_lbl.setVisible(False)
        self.class_edit.setVisible(False)

        # Load data
        load_students_into_combo(self.student_combo, self.db)
        load_payment_modes_into_combo(self.mode)
        load_heads_into_combo(self.head, self.db)
        load_subheads_into_combo(self.subhead, self.db, None)

    def load_heads(self):
        load_heads_into_combo(self.head, self.db, self.type_combo.currentText())

    def load_subheads(self):
        head_id = self.head.currentData()
        load_subheads_into_combo(self.subhead, self.db, head_id)

        if self.head.currentText().lower() == "fees":
            self.student_lbl.setVisible(True)
            self.student_combo.setVisible(True)
            self.class_lbl.setVisible(True)
            self.class_edit.setVisible(True)
        else:
            self.student_lbl.setVisible(False)
            self.student_combo.setVisible(False)
            self.class_lbl.setVisible(False)
            self.class_edit.setVisible(False)
            self.student_combo.setCurrentIndex(0)
            self.class_edit.clear()

    def load_student_class(self):
        student = self.student_combo.currentData()
        if student:
            self.class_edit.setText(student[7])
        else:
            self.class_edit.clear()

    def save_voucher(self):
        if self.type_combo.currentIndex() == 0:
            QMessageBox.warning(self, "Error", "Select Type")
            return
        
        if self.head.currentIndex() == 0:
            QMessageBox.warning(self, "Error", "Select Head")
            return

        if self.subhead.currentIndex() == 0:
            QMessageBox.warning(self, "Error", "Select Subhead")
            return

        if self.head.currentText().lower() == "fees":
            if self.student_combo.currentIndex() == 0:
                QMessageBox.warning(self, "Error", "Select Student")
                return

        try:
            amount = float(self.amount.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Enter valid amount")
            return

        if self.mode.currentIndex() == 0:
            QMessageBox.warning(self, "Error", "Select Mode")
            return

        student = self.student_combo.currentData() or ("", "", "", "", "", "", "", "")

        voucher_data = (
            self.date.date().toString("yyyy-MM-dd"),
            self.type_combo.currentText(),
            self.head.currentText(),
            self.subhead.currentText(),
            student[2] if student else "",
            student[7] if student else "",
            amount,
            self.mode.currentText(),
            format_text_for_db(self.note.text())
        )

        self.db.add_voucher(*voucher_data)
        QMessageBox.information(self, "Success", "Voucher saved successfully!")
        self.clear_form()
        self.refresh()

    def clear_form(self):
        self.type_combo.setCurrentIndex(0)
        self.amount.clear()
        self.note.clear()
        self.student_combo.setCurrentIndex(0)
        self.class_edit.clear()

    def refresh(self):
        # Refresh table data
        vouchers = self.db.get_vouchers()
        self.table.setRowCount(len(vouchers))
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels(["ID", "Date", "Type", "Head", "Subhead", "Student", "Class", "Amount", "Mode", "Note"])
        
        for row, voucher in enumerate(vouchers):
            for col, data in enumerate(voucher):
                self.table.setItem(row, col, QTableWidgetItem(str(data)))
        
        style_table(self.table)
''',

    "student_list.py": '''from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from ui2.database import Database
from ui2.header import PageHeader
from ui2.common_table import style_table

class StudentListPage(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        
        layout = QVBoxLayout(self)
        layout.addWidget(PageHeader("Student List"))
        
        # Table
        self.table = QTableWidget()
        style_table(self.table)
        layout.addWidget(self.table)
        
        self.load_data()
    
    def load_data(self):
        students = self.db.get_students()
        self.table.setRowCount(len(students))
        self.table.setColumnCount(14)
        self.table.setHorizontalHeaderLabels(["ID", "Student ID", "Name", "Father", "Aadhaar", "DOB", "Join Date", "Class", "Phone1", "Phone2", "Location", "City", "Address", "Annual Fee"])
        
        for row, student in enumerate(students):
            for col, data in enumerate(student):
                self.table.setItem(row, col, QTableWidgetItem(str(data)))
        
        style_table(self.table)
''',

    "student_registration.py": '''from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QRegularExpression, Signal, QDate
from PySide6.QtGui import QRegularExpressionValidator
from ui2.database import Database
from ui2.header import PageHeader
from ui2.common_form import (style_lineedit, style_combo, style_button, style_dateedit, style_label, format_text_for_db, 
                              EnhancedLineEdit, EnhancedComboBox, EnhancedDateEdit, 
                              data_manager, load_classes_into_combo)

class StudentRegistration(QWidget):
    student_added = Signal()

    def __init__(self):
        super().__init__()
        
        # Apply light theme
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                color: #333333;
            }
            QFrame {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
            QLabel {
                color: #333333;
            }
        """)

        self.db = Database()
        self.mode = "NEW"

        main = QVBoxLayout(self)
        main.setSpacing(15)

        main.addWidget(PageHeader("Student Registration"))

        # Form card
        card = QFrame()
        grid = QGridLayout(card)
        grid.setSpacing(12)

        self.student_id = EnhancedLineEdit()
        style_lineedit(self.student_id)
        self.name = EnhancedLineEdit()
        style_lineedit(self.name)
        self.father = EnhancedLineEdit()
        style_lineedit(self.father)
        self.aadhaar = EnhancedLineEdit()
        style_lineedit(self.aadhaar)
        self.dob = EnhancedDateEdit(calendarPopup=True)
        style_dateedit(self.dob)
        self.dob.setDisplayFormat("dd/MM/yyyy")
        self.dob.setDate(QDate())
        
        self.join_date = EnhancedDateEdit(calendarPopup=True)
        style_dateedit(self.join_date)
        self.class_combo = EnhancedComboBox()
        style_combo(self.class_combo)
        self.phone1 = EnhancedLineEdit()
        style_lineedit(self.phone1)
        self.phone2 = EnhancedLineEdit()
        style_lineedit(self.phone2)
        self.address = EnhancedLineEdit()
        style_lineedit(self.address)
        self.location = EnhancedLineEdit()
        style_lineedit(self.location)
        self.city = EnhancedLineEdit()
        style_lineedit(self.city)
        self.annual_fee = EnhancedLineEdit()
        style_lineedit(self.annual_fee)

        # Add fields to grid
        fields = [
            ("ID", self.student_id), ("Name", self.name),
            ("Father", self.father), ("Aadhaar", self.aadhaar),
            ("DOB", self.dob), ("Join Date", self.join_date),
            ("Class", self.class_combo), ("Phone1", self.phone1),
            ("Phone2", self.phone2), ("Address", self.address),
            ("Location", self.location), ("City", self.city),
            ("Annual Fee", self.annual_fee)
        ]

        for i, (label_text, widget) in enumerate(fields):
            label = QLabel(label_text)
            style_label(label)
            grid.addWidget(label, i // 2, (i % 2) * 2)
            grid.addWidget(widget, i // 2, (i % 2) * 2 + 1)

        main.addWidget(card)

        # Buttons
        btn_layout = QHBoxLayout()
        self.btn_save = QPushButton("Save")
        self.btn_new = QPushButton("New")
        style_button(self.btn_save)
        style_button(self.btn_new)

        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_new)
        btn_layout.addStretch()

        main.addLayout(btn_layout)

        # Connections
        self.btn_save.clicked.connect(self.save_student)
        self.btn_new.clicked.connect(self.clear_form)

        # Load classes
        self.class_combo.addItems(["6th", "7th", "8th", "9th", "10th"])

    def save_student(self):
        if not self.name.text():
            QMessageBox.warning(self, "Error", "Enter student name")
            return

        data = (
            self.student_id.text(),
            format_text_for_db(self.name.text()),
            format_text_for_db(self.father.text()),
            self.aadhaar.text(),
            self.dob.date().toString("dd/MM/yyyy") if self.dob.date().isValid() else "",
            self.join_date.date().toString("dd/MM/yyyy") if self.join_date.date().isValid() else "",
            self.class_combo.currentText(),
            self.phone1.text(),
            self.phone2.text(),
            format_text_for_db(self.address.text()),
            format_text_for_db(self.location.text()),
            format_text_for_db(self.city.text()),
            self.annual_fee.text()
        )

        self.db.add_student(*data)
        QMessageBox.information(self, "Success", "Student saved successfully!")
        self.clear_form()
        self.student_added.emit()

    def clear_form(self):
        self.student_id.clear()
        self.name.clear()
        self.father.clear()
        self.aadhaar.clear()
        self.dob.setDate(QDate())
        self.join_date.setDate(QDate())
        self.class_combo.setCurrentIndex(0)
        self.phone1.clear()
        self.phone2.clear()
        self.address.clear()
        self.location.clear()
        self.city.clear()
        self.annual_fee.clear()
''',

    "reports.py": '''from ui2.common_table import style_table
from PySide6.QtWidgets import *
from PySide6.QtCore import QDate
from ui2.database import Database
from ui2.header import PageHeader
from ui2.common_form import style_dateedit, style_combo, style_button, style_label

class ReportPage(QWidget):
   def __init__(self):
       super().__init__()
       
       # Apply light theme
       self.setStyleSheet("""
           QWidget {
               background-color: #f8f9fa;
               color: #333333;
           }
           QFrame {
               background-color: white;
               border-radius: 8px;
               border: 1px solid #e0e0e0;
           }
           QLabel {
               color: #333333;
           }
       """)

       layout = QVBoxLayout(self)
       layout.addWidget(PageHeader("Reports"))

       tabs = QTabWidget()
       tabs.setStyleSheet("""
       QTabBar::tab {
           font-weight: bold;
           padding: 6px 12px;
       }
       QTabBar::tab:selected {
           color: #1D4ED8;
       }
       """)
       
       self.finance_page = FinancePage()
       self.fee_page = FeePage()

       tabs.addTab(self.finance_page, "Finance")
       tabs.addTab(self.fee_page, "Fees")
       layout.addWidget(tabs)

class FinancePage(QWidget):
   def __init__(self):
       super().__init__()
       self.db = Database()
       layout = QVBoxLayout(self)
       layout.setSpacing(12)
       
       # Filter card
       filter_card = QFrame()
       filter_layout = QVBoxLayout(filter_card)
       filter_layout.setSpacing(12)
       filter_layout.setContentsMargins(15, 15, 15, 15)
       
       top = QHBoxLayout()
       self.from_date = QDateEdit(calendarPopup=True)
       self.from_date.setDisplayFormat("dd/MM/yyyy")
       self.to_date = QDateEdit(calendarPopup=True)
       self.to_date.setDisplayFormat("dd/MM/yyyy")
       style_dateedit(self.from_date)
       style_dateedit(self.to_date)
       self.from_date.setDate(QDate.currentDate().addMonths(-1))
       self.to_date.setDate(QDate.currentDate())

       self.type_combo = QComboBox()
       self.type_combo.addItems(["All", "Income", "Expense"])
       style_combo(self.type_combo)

       btn_load = QPushButton("Load Report")
       style_button(btn_load)
       btn_load.clicked.connect(self.load_report)

       from_label = QLabel("From")
       style_label(from_label)
       to_label = QLabel("To")
       style_label(to_label)
       type_label = QLabel("Type")
       style_label(type_label)

       top.addWidget(from_label)
       top.addWidget(self.from_date)
       top.addWidget(to_label)
       top.addWidget(self.to_date)
       top.addWidget(type_label)
       top.addWidget(self.type_combo)
       top.addWidget(btn_load)
       top.addStretch()

       filter_layout.addLayout(top)
       layout.addWidget(filter_card)

       # Summary
       self.summary = QLabel("")
       self.summary.setStyleSheet("""
           font-weight:bold;
           font-size:15px;
           padding:10px;
           background:#F4F6F8;
           border-radius:6px;
           color: #333333;
       """)
       layout.addWidget(self.summary)

       # Table
       self.table = QTableWidget()
       style_table(self.table)
       layout.addWidget(self.table)
       self.load_report()

   def load_report(self):
       vouchers = self.db.get_vouchers()
       self.table.setRowCount(len(vouchers))
       self.table.setColumnCount(10)
       self.table.setHorizontalHeaderLabels(["ID", "Date", "Type", "Head", "Subhead", "Student", "Class", "Amount", "Mode", "Note"])
       
       for row, voucher in enumerate(vouchers):
           for col, data in enumerate(voucher):
               self.table.setItem(row, col, QTableWidgetItem(str(data)))
       
       style_table(self.table)

class FeePage(QWidget):
   def __init__(self):
       super().__init__()
       self.db = Database()
       layout = QVBoxLayout(self)

       # Filter card
       filter_card = QFrame()
       filter_layout = QVBoxLayout(filter_card)
       filter_layout.setSpacing(12)
       filter_layout.setContentsMargins(15, 15, 15, 15)
       
       top = QHBoxLayout()
       self.class_combo = QComboBox()
       self.class_combo.addItems(["All","6th","7th","8th","9th","10th"])
       style_combo(self.class_combo)

       btn = QPushButton("Load")
       style_button(btn)
       btn.clicked.connect(self.load_report)

       class_label = QLabel("Select Class")
       style_label(class_label)

       top.addWidget(class_label)
       top.addWidget(self.class_combo)
       top.addWidget(btn)
       top.addStretch()

       filter_layout.addLayout(top)
       layout.addWidget(filter_card)

       # Summary
       self.summary = QLabel("")
       self.summary.setStyleSheet("""
           font-weight:bold;
           font-size:15px;
           padding:10px;
           background:#F4F6F8;
           border-radius:6px;
           color: #333333;
       """)
       layout.addWidget(self.summary)

       # Table
       self.table = QTableWidget()
       style_table(self.table)
       layout.addWidget(self.table)
       self.load_report()

   def load_report(self):
       students = self.db.get_students()
       self.table.setRowCount(len(students))
       self.table.setColumnCount(14)
       self.table.setHorizontalHeaderLabels(["ID", "Student ID", "Name", "Father", "Aadhaar", "DOB", "Join Date", "Class", "Phone1", "Phone2", "Location", "City", "Address", "Annual Fee"])
       
       for row, student in enumerate(students):
           for col, data in enumerate(student):
               self.table.setItem(row, col, QTableWidgetItem(str(data)))
       
       style_table(self.table)
''',

    "heads.py": '''from ui2.common_table import style_table
from ui2.common_form import style_label, style_button, style_groupbox, style_lineedit, style_combo
from PySide6.QtWidgets import *
from database import Database
from ui2.header import PageHeader
from PySide6.QtCore import Qt, Signal


class HeadPage(QWidget):
    head_added = Signal()
    subhead_added = Signal()

    def __init__(self):
        super().__init__()
        self.db = Database()
        self.entry_mode = "HEAD"

        layout = QVBoxLayout(self)
        layout.addWidget(PageHeader("Manage Heads"))

        # Create main horizontal layout for two sections
        main_layout = QHBoxLayout()
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # ================= ADD HEAD SECTION (LEFT) =================
        head_widget = QWidget()
        head_widget.setFixedSize(500, 300)
        head_layout = QVBoxLayout(head_widget)
        head_layout.setSpacing(15)
        head_layout.setContentsMargins(10, 10, 10, 10)
        
        head_group = QGroupBox("Add Head")
        head_group_layout = QVBoxLayout()
        head_group_layout.setSpacing(15)
        head_group_layout.setContentsMargins(10, 10, 10, 10)
        
        # Initialize widgets
        self.head_type = QComboBox()
        self.head_type.addItems(["Income", "Expense"])
        self.head_type.setMinimumHeight(35)
        self.head_type.setView(QListView())
        style_combo(self.head_type)
        
        self.head_name = QLineEdit()
        self.head_name.setMinimumHeight(35)
        style_lineedit(self.head_name)
        
        self.btn_add_head = QPushButton("Add Head")
        self.btn_add_head.setFixedWidth(120)
        style_button(self.btn_add_head)
        
        # Type row
        type_row = QHBoxLayout()
        type_label = QLabel("Type:")
        style_label(type_label)
        type_row.addWidget(type_label)
        type_row.addWidget(self.head_type)
        head_group_layout.addLayout(type_row)
        
        # Head Name row
        name_row = QHBoxLayout()
        name_label = QLabel("Head Name:")
        style_label(name_label)
        name_row.addWidget(name_label)
        name_row.addWidget(self.head_name)
        head_group_layout.addLayout(name_row)
        
        # Button
        head_button_layout = QHBoxLayout()
        head_button_layout.addStretch()
        head_button_layout.addWidget(self.btn_add_head)
        head_button_layout.addStretch()
        head_group_layout.addLayout(head_button_layout)
        
        head_group.setLayout(head_group_layout)
        style_groupbox(head_group)
        head_layout.addWidget(head_group)
        
        head_widget.setLayout(head_layout)
        main_layout.addWidget(head_widget)

        # ================= ADD SUBHEAD SECTION (RIGHT) =================
        subhead_widget = QWidget()
        subhead_widget.setFixedSize(500, 300)
        subhead_layout = QVBoxLayout(subhead_widget)
        subhead_layout.setSpacing(15)
        subhead_layout.setContentsMargins(10, 10, 10, 10)
        
        sub_group = QGroupBox("Add Subhead")
        sub_group_layout = QVBoxLayout()
        sub_group_layout.setSpacing(15)
        sub_group_layout.setContentsMargins(10, 10, 10, 10)
        
        # Initialize widgets
        self.sub_type = QComboBox()
        self.sub_type.addItems(["Income", "Expense"])
        self.sub_type.setMinimumHeight(35)
        self.sub_type.setView(QListView())
        style_combo(self.sub_type)
        
        self.sub_head_combo = QComboBox()
        self.sub_head_combo.setMinimumHeight(35)
        self.sub_head_combo.setView(QListView())
        style_combo(self.sub_head_combo)
        
        self.sub_name = QLineEdit()
        self.sub_name.setMinimumHeight(35)
        style_lineedit(self.sub_name)
        
        self.btn_add_sub = QPushButton("Add Subhead")
        self.btn_add_sub.setFixedWidth(120)
        style_button(self.btn_add_sub)
        
        # Type row
        sub_type_row = QHBoxLayout()
        sub_type_label = QLabel("Type:")
        style_label(sub_type_label)
        sub_type_row.addWidget(sub_type_label)
        sub_type_row.addWidget(self.sub_type)
        sub_group_layout.addLayout(sub_type_row)
        
        # Head row
        head_row = QHBoxLayout()
        head_label = QLabel("Head:")
        style_label(head_label)
        head_row.addWidget(head_label)
        head_row.addWidget(self.sub_head_combo)
        sub_group_layout.addLayout(head_row)
        
        # Subhead row
        subhead_row = QHBoxLayout()
        subhead_label = QLabel("Subhead:")
        style_label(subhead_label)
        subhead_row.addWidget(subhead_label)
        subhead_row.addWidget(self.sub_name)
        sub_group_layout.addLayout(subhead_row)
        
        # Button
        sub_button_layout = QHBoxLayout()
        sub_button_layout.addStretch()
        sub_button_layout.addWidget(self.btn_add_sub)
        sub_button_layout.addStretch()
        sub_group_layout.addLayout(sub_button_layout)
        
        sub_group.setLayout(sub_group_layout)
        style_groupbox(sub_group)
        subhead_layout.addWidget(sub_group)
        
        subhead_widget.setLayout(subhead_layout)
        main_layout.addWidget(subhead_widget)
        main_layout.addStretch()
        
        layout.addLayout(main_layout)

        # ================= TABLE =================
        self.table = QTableWidget()
        style_table(self.table)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.cellDoubleClicked.connect(self.select_row)
        layout.addWidget(self.table)

        # ================= DELETE BUTTON =================
        btn_layout = QHBoxLayout()
        self.btn_delete = QPushButton("Delete")
        style_button(self.btn_delete)
        self.btn_delete.setEnabled(False)

        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_delete)
        layout.addLayout(btn_layout)

        # ================= CONNECTIONS =================
        self.btn_add_head.clicked.connect(self.add_head)
        self.btn_add_sub.clicked.connect(self.add_subhead)
        self.btn_delete.clicked.connect(self.delete_selected)
        self.head_type.currentTextChanged.connect(self.load_heads)
        self.sub_type.currentTextChanged.connect(self.load_heads)

        # ================= INITIAL LOAD =================
        self.load_data()

    def add_head(self):
        typ = self.head_type.currentText()
        head = self.head_name.text().strip()

        if not head:
            QMessageBox.warning(self, "Warning", "Enter head name")
            return

        try:
            self.db.add_head(typ, head)
            QMessageBox.information(self, "Success", "Head added successfully")
            self.head_name.clear()
            self.load_data()
            self.head_added.emit()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to add head: {str(e)}")

    def add_subhead(self):
        typ = self.sub_type.currentText()
        head = self.sub_head_combo.currentText()
        sub = self.sub_name.text().strip()

        if not head or head == "Select Head":
            QMessageBox.warning(self, "Warning", "Select head")
            return

        if not sub:
            QMessageBox.warning(self, "Warning", "Enter subhead name")
            return

        try:
            self.db.add_subhead(typ, head, sub)
            QMessageBox.information(self, "Success", "Subhead added successfully")
            self.sub_name.clear()
            self.load_data()
            self.subhead_added.emit()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to add subhead: {str(e)}")

    def load_heads(self):
        self.sub_head_combo.clear()
        self.sub_head_combo.addItem("Select Head", None)
        
        typ = self.sub_type.currentText()
        heads = self.db.get_heads(typ)
        
        for head in heads:
            self.sub_head_combo.addItem(head[1], head[0])

    def load_data(self):
        data = []
        
        heads = self.db.get_all_heads()
        for head in heads:
            data.append(("HEAD", head[1], head[0], "", ""))
        
        for head in heads:
            subheads = self.db.get_subheads_by_headid(head[0])
            for subhead in subheads:
                data.append(("SUBHEAD", subhead[1], head[1], head[0], subhead[0]))
        
        self.table.setRowCount(len(data))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Type", "Name", "Head", "Head ID", "Subhead ID"])
        
        for row, item in enumerate(data):
            for col, value in enumerate(item):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))
        
        self.table.setColumnHidden(3, True)
        self.table.setColumnHidden(4, True)
        style_table(self.table)

    def select_row(self, row, col):
        self.btn_delete.setEnabled(True)

    def delete_selected(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            return

        item_type = self.table.item(current_row, 0).text()
        name = self.table.item(current_row, 1).text()

        reply = QMessageBox.question(self, "Confirm Delete", 
                                   f"Are you sure you want to delete {item_type}: {name}?",
                                   QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                if item_type == "HEAD":
                    head_id = self.table.item(current_row, 3).text()
                    self.delete_head(head_id)
                else:
                    subhead_id = self.table.item(current_row, 4).text()
                    self.delete_subhead(subhead_id)
                
                self.load_data()
                self.btn_delete.setEnabled(False)
                QMessageBox.information(self, "Success", "Deleted successfully")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to delete: {str(e)}")

    def delete_head(self, head_id):
        subheads = self.db.get_subheads_by_headid(head_id)
        for subhead in subheads:
            self.db.conn.execute("DELETE FROM subheads WHERE id = ?", (subhead[0],))
        
        self.db.conn.execute("DELETE FROM heads WHERE id = ?", (head_id,))
        self.db.conn.commit()

    def delete_subhead(self, subhead_id):
        self.db.conn.execute("DELETE FROM subheads WHERE id = ?", (subhead_id,))
        self.db.conn.commit()
''',
}

def _safe(s):
    try:
        return s.encode('utf-8','ignore').decode('utf-8','ignore')
    except:
        return str(s)

def ensure():
    for path, content in FILES.items():
        p = TARGET / path
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", encoding="utf-8", errors="ignore") as f:
            f.write(_safe(content))

def run():
    sys.path.insert(0, str(pathlib.Path(os.getcwd())))
    ensure()
    mod = import_module("ui2.mainwindow")
    from PySide6.QtWidgets import QApplication
    import sys as _s
    app = QApplication(_s.argv)
    w = mod.MainWindow()
    w.show()
    _s.exit(app.exec())

if __name__=="__main__":
    run()
