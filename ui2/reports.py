from ui2.common_table import style_table
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
