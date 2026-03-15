from PySide6.QtWidgets import *
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
