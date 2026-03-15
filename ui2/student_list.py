from PySide6.QtWidgets import *
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
