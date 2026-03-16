import sys
import os
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

# Add parent directory to path for direct execution
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui2.header import PageHeader
from ui2.vouchers import VoucherPage
from ui2.reports import ReportPage
from ui2.heads import HeadPage
from ui2.student_list import StudentListPage
from ui2.student_registration import StudentRegistration

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Darus Salah")
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
        
        # Main horizontal layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        sidebar = QWidget()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("""
            QWidget {
                background: white;
                color: #2c3e50;
            }
        """)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        sidebar_layout.setSpacing(10)
        
        # Sidebar title
        title_label = QLabel("Menu")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2F80ED;
                padding: 10px;
                background: #f8f9fa;
                border-radius: 6px;
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(title_label)
        
        # Navigation buttons
        self.btn_vouchers = QPushButton("Vouchers")
        self.btn_reports = QPushButton("Reports")
        self.btn_heads = QPushButton("Manage Heads")
        self.btn_students = QPushButton("Students")
        self.btn_registration = QPushButton("Student Registration")
        
        # Style sidebar buttons
        for btn in [self.btn_vouchers, self.btn_reports, self.btn_heads, self.btn_students, self.btn_registration]:
            btn.setMinimumHeight(45)
            btn.setStyleSheet("""
                QPushButton {
                    background: #2980b9;
                    border: none;
                    border-radius: 6px;
                    padding: 10px;
                    font-weight: bold;
                    color: white;
                }
                QPushButton:hover {
                    background: #5DADE2;
                }
                QPushButton:pressed {
                    background: #1F618D;
                }
            """)
        
        sidebar_layout.addWidget(self.btn_vouchers)
        sidebar_layout.addWidget(self.btn_reports)
        sidebar_layout.addWidget(self.btn_heads)
        sidebar_layout.addWidget(self.btn_students)
        sidebar_layout.addWidget(self.btn_registration)
        sidebar_layout.addStretch()
        
        # Exit button
        self.btn_exit = QPushButton("Exit")
        self.btn_exit.setMinimumHeight(45)
        self.btn_exit.setStyleSheet("""
            QPushButton {
                background: #e74c3c;
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover {
                background: #c0392b;
            }
        """)
        self.btn_exit.clicked.connect(self.close)
        sidebar_layout.addWidget(self.btn_exit)
        
        main_layout.addWidget(sidebar)
        
        # Content area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = PageHeader("Education and Research Center", show_background=False, use_header_image=True)
        content_layout.addWidget(header)
        
        # Stack widget for pages
        self.stack = QStackedWidget()
        content_layout.addWidget(self.stack)
        
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
        
        main_layout.addWidget(content_widget)
        
        # Connect signals
        self.btn_vouchers.clicked.connect(lambda: self.stack.setCurrentWidget(self.voucher_page))
        self.btn_reports.clicked.connect(lambda: self.stack.setCurrentWidget(self.report_page))
        self.btn_heads.clicked.connect(lambda: self.stack.setCurrentWidget(self.head_page))
        self.btn_students.clicked.connect(lambda: self.stack.setCurrentWidget(self.student_list_page))
        self.btn_registration.clicked.connect(lambda: self.stack.setCurrentWidget(self.registration_page))
        
        # Set default page
        self.stack.setCurrentWidget(self.voucher_page)

# Main execution block for direct running
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
