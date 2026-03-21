from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QDate
from ui2.database import Database
from ui2.header import PageHeader
from ui2.common_table import style_table
from ui2.student_registration import StudentRegistration

class StudentListPage(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        
        layout = QVBoxLayout(self)
        layout.addWidget(PageHeader("Student List"))
        
        # Buttons
        button_layout = QHBoxLayout()
        self.btn_refresh = QPushButton("Refresh")
        self.btn_new_student = QPushButton("Add New Student")
        self.btn_delete = QPushButton("Delete Selected")
        self.btn_delete.setEnabled(False)
        
        self.btn_refresh.clicked.connect(self.load_data)
        self.btn_new_student.clicked.connect(self.open_new_student_form)
        self.btn_delete.clicked.connect(self.delete_selected_student)
        
        button_layout.addWidget(self.btn_refresh)
        button_layout.addWidget(self.btn_new_student)
        button_layout.addStretch()
        button_layout.addWidget(self.btn_delete)
        layout.addLayout(button_layout)
        
        # Table
        self.table = QTableWidget()
        style_table(self.table)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSortingEnabled(True)
        self.table.cellDoubleClicked.connect(self.edit_student)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        layout.addWidget(self.table)
        
        self.load_data()
    
    def on_selection_changed(self):
        """Enable/disable delete button based on selection"""
        has_selection = bool(self.table.selectedItems())
        self.btn_delete.setEnabled(has_selection)
    
    def edit_student(self, row, column):
        """Open student registration form with selected student data"""
        student_data = []
        for col in range(self.table.columnCount()):
            item = self.table.item(row, col)
            student_data.append(item.text() if item else "")
        
        # Open registration dialog with student data
        dialog = StudentEditDialog(student_data, self)
        if dialog.exec() == QDialog.Accepted:
            self.load_data()
    
    def open_new_student_form(self):
        """Open new student registration form"""
        dialog = StudentEditDialog([], self)
        if dialog.exec() == QDialog.Accepted:
            self.load_data()
    
    def delete_selected_student(self):
        """Delete the selected student"""
        current_row = self.table.currentRow()
        if current_row < 0:
            return
        
        student_id_item = self.table.item(current_row, 1)  # Student ID column
        student_name_item = self.table.item(current_row, 2)  # Name column
        
        if not student_id_item or not student_name_item:
            return
        
        student_id = student_id_item.text()
        student_name = student_name_item.text()
        
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete student {student_name} (ID: {student_id})?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.db.conn.execute("DELETE FROM students WHERE student_id=?", (student_id,))
                self.db.conn.commit()
                QMessageBox.information(self, "Success", "Student deleted successfully")
                self.load_data()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to delete student: {str(e)}")
    
    def load_data(self):
        students = self.db.get_students()
        self.table.setRowCount(len(students))
        self.table.setColumnCount(14)
        self.table.setHorizontalHeaderLabels(["ID", "Student ID", "Name", "Father", "Aadhaar", "DOB", "Join Date", "Class", "Phone1", "Phone2", "Location", "City", "Address", "Annual Fee"])
        
        for row, student in enumerate(students):
            for col, data in enumerate(student):
                self.table.setItem(row, col, QTableWidgetItem(str(data)))
        
        # Adjust column widths
        self.table.resizeColumnsToContents()
        style_table(self.table)


class StudentEditDialog(QDialog):
    def __init__(self, student_data, parent=None):
        super().__init__(parent)
        self.db = Database()
        self.student_data = student_data
        self.setWindowTitle("Edit Student" if student_data else "Add New Student")
        self.setFixedSize(600, 500)
        
        layout = QVBoxLayout(self)
        
        # Create registration form
        self.registration_form = StudentRegistration()
        
        # If editing, populate the form with existing data
        if student_data:
            self.populate_form()
        
        layout.addWidget(self.registration_form)
        
        # Dialog buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.save_student)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def populate_form(self):
        """Populate the form with existing student data"""
        if len(self.student_data) >= 14:
            self.registration_form.student_id.setText(self.student_data[1])
            self.registration_form.name.setText(self.student_data[2])
            self.registration_form.father.setText(self.student_data[3])
            self.registration_form.aadhaar.setText(self.student_data[4])
            self.registration_form.dob.setDate(QDate.fromString(self.student_data[5], "dd/MM/yyyy"))
            self.registration_form.join_date.setDate(QDate.fromString(self.student_data[6], "dd/MM/yyyy"))
            
            # Set class
            class_index = self.registration_form.class_combo.findText(self.student_data[7])
            if class_index >= 0:
                self.registration_form.class_combo.setCurrentIndex(class_index)
            
            self.registration_form.phone1.setText(self.student_data[8])
            self.registration_form.phone2.setText(self.student_data[9])
            self.registration_form.location.setText(self.student_data[10])
            self.registration_form.city.setText(self.student_data[11])
            self.registration_form.address.setText(self.student_data[12])
            self.registration_form.annual_fee.setText(self.student_data[13])
    
    def save_student(self):
        """Save student data"""
        if self.registration_form.name.text():
            # Delete existing student if editing
            if self.student_data:
                old_student_id = self.student_data[1]
                self.db.conn.execute("DELETE FROM students WHERE student_id=?", (old_student_id,))
            
            # Save new/updated student
            self.registration_form.save_student()
            self.accept()
