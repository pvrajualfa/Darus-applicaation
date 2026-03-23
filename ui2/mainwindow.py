import sys
import os
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

# Add parent directory to path for direct execution
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui2.header import PageHeader
from ui2.vouchers import VoucherPage
from ui2.voucher_list import VoucherListPage
from ui2.reports import ReportPage
from ui2.heads import HeadPage
from ui2.student_list import StudentListPage
from ui2.student_registration import StudentRegistration
from ui2.common_form import style_button

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
        sidebar_layout.setContentsMargins(15, 20, 15, 20)
        sidebar_layout.setSpacing(5)
        
        # Sidebar title
        title_label = QLabel("MENU")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: bold;
                color: #1B3C5A;
                font-family: Helvetica;
                padding: 15px;
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                border-radius: 10px;
                border: 2px solid #dee2e6;
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(title_label)
        
        # Navigation buttons
        # Voucher section
        self.voucher_group = QWidget()
        voucher_group_layout = QVBoxLayout(self.voucher_group)
        voucher_group_layout.setContentsMargins(0, 12, 0, 12)
        voucher_group_layout.setSpacing(5)
        
        voucher_label = QLabel("VOUCHER")
        voucher_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #1B3C5A;
                font-family: Arial;
                padding: 8px 0px;
                background: transparent;
                margin-bottom: 8px;
            }
        """)
        
        self.btn_vouchers = QPushButton("New Voucher")
        self.btn_vouchers.setFixedWidth(160)
        self.btn_voucher_list = QPushButton("Voucher List")
        self.btn_voucher_list.setFixedWidth(160)
        
        voucher_group_layout.addWidget(voucher_label)
        voucher_group_layout.addWidget(self.btn_vouchers)
        voucher_group_layout.addWidget(self.btn_voucher_list)
        
        # Add separator
        separator1 = QFrame()
        separator1.setFrameShape(QFrame.HLine)
        separator1.setStyleSheet("QFrame { background-color: #e0e0e0; max-height: 1px; }")
        voucher_group_layout.addWidget(separator1)
        
        # Student section
        self.student_group = QWidget()
        student_group_layout = QVBoxLayout(self.student_group)
        student_group_layout.setContentsMargins(0, 12, 0, 12)
        student_group_layout.setSpacing(5)
        
        student_label = QLabel("STUDENT")
        student_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #1B3C5A;
                font-family: Arial;
                padding: 8px 0px;
                background: transparent;
                margin-bottom: 8px;
            }
        """)
        
        self.btn_registration = QPushButton("New Registration")
        self.btn_registration.setFixedWidth(160)
        self.btn_students = QPushButton("Student List")
        self.btn_students.setFixedWidth(160)
        
        student_group_layout.addWidget(student_label)
        student_group_layout.addWidget(self.btn_registration)
        student_group_layout.addWidget(self.btn_students)
        
        # Add separator
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.HLine)
        separator2.setStyleSheet("QFrame { background-color: #e0e0e0; max-height: 1px; }")
        student_group_layout.addWidget(separator2)
        
        # Management section
        self.management_group = QWidget()
        management_group_layout = QVBoxLayout(self.management_group)
        management_group_layout.setContentsMargins(0, 12, 0, 12)
        management_group_layout.setSpacing(5)
        
        management_label = QLabel("MANAGEMENT")
        management_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #1B3C5A;
                font-family: Arial;
                padding: 8px 0px;
                background: transparent;
                margin-bottom: 8px;
            }
        """)
        
        self.btn_reports = QPushButton("Reports")
        self.btn_reports.setFixedWidth(160)
        self.btn_heads = QPushButton("Manage Heads")
        self.btn_heads.setFixedWidth(160)
        
        management_group_layout.addWidget(management_label)
        management_group_layout.addWidget(self.btn_reports)
        management_group_layout.addWidget(self.btn_heads)
        
        # Style sidebar buttons with common_form theme
        for btn in [self.btn_vouchers, self.btn_voucher_list, self.btn_registration, self.btn_students, self.btn_reports, self.btn_heads]:
            style_button(btn)
        
        # Add groups to sidebar with proper spacing
        sidebar_layout.addWidget(self.voucher_group)
        sidebar_layout.addWidget(self.student_group)
        sidebar_layout.addWidget(self.management_group)
        sidebar_layout.addStretch()
        
        # Exit button
        self.btn_exit = QPushButton("Exit")
        self.btn_exit.setFixedWidth(160)
        self.btn_exit.setMinimumHeight(45)
        self.btn_exit.setStyleSheet("""
            QPushButton {
                background: #e74c3c;
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-weight: bold;
                font-size: 14px;
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
        self.voucher_list_page = VoucherListPage()
        self.report_page = ReportPage()
        self.head_page = HeadPage()
        self.student_list_page = StudentListPage()
        self.registration_page = StudentRegistration()
        
        # Add pages to stack
        self.stack.addWidget(self.voucher_page)
        self.stack.addWidget(self.voucher_list_page)
        self.stack.addWidget(self.report_page)
        self.stack.addWidget(self.head_page)
        self.stack.addWidget(self.student_list_page)
        self.stack.addWidget(self.registration_page)
        
        main_layout.addWidget(content_widget)
        
        # Connect signals
        self.btn_vouchers.clicked.connect(lambda: self.switch_to_tab(self.voucher_page))
        self.btn_voucher_list.clicked.connect(lambda: self.switch_to_tab(self.voucher_list_page))
        self.btn_reports.clicked.connect(lambda: self.switch_to_tab(self.report_page))
        self.btn_heads.clicked.connect(lambda: self.switch_to_tab(self.head_page))
        self.btn_students.clicked.connect(lambda: self.switch_to_tab(self.student_list_page))
        self.btn_registration.clicked.connect(lambda: self.switch_to_tab(self.registration_page))
        
        # Set default page
        self.set_default_page()
        
    def switch_to_tab(self, page):
        """Switch to specific tab with debugging"""
        print(f"Switching to tab: {page.__class__.__name__}")
        self.stack.setCurrentWidget(page)
        print(f"Current widget is now: {self.stack.currentWidget().__class__.__name__}")
        
    # Set default page
    def set_default_page(self):
        self.stack.setCurrentWidget(self.voucher_page)

# Main execution block for direct running
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
