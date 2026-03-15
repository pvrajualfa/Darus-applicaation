from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, Signal
from ui2.student_registration import StudentRegistration
from ui2.student_list import StudentList


class StudentPage(QWidget):
    student_added = Signal()
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        # ===== stacked pages ONLY (no buttons needed now) =====
        self.stack = QStackedWidget()

        self.reg_page = StudentRegistration()
        self.list_page = StudentList()
        self.list_page.registration = self.reg_page
        self.list_page.student_page = self
        self.reg_page.student_added.connect(self.student_added.emit)

        self.stack.addWidget(self.reg_page)
        self.stack.addWidget(self.list_page)

        layout.addWidget(self.stack)

        # =================================================
        # Default Open
        # =================================================
        self.show_registration()

        # =================================================
        # Required Methods (Mainwindow Calls these)
        # =================================================
    def show_registration(self):
        self.stack.setCurrentWidget(self.reg_page)

    def show_list(self):
        self.list_page.refresh()  # ⭐ refresh table first
        self.stack.setCurrentWidget(self.list_page)