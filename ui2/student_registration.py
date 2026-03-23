from PySide6.QtWidgets import *
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
        self.dob = EnhancedDateEdit(QDate.currentDate(), calendarPopup=True)
        style_dateedit(self.dob)
        self.dob.setDisplayFormat("dd/MM/yyyy")
        
        self.join_date = EnhancedDateEdit(QDate.currentDate(), calendarPopup=True)
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
        
        # Academic Year dropdown
        self.academic_year = EnhancedComboBox()
        style_combo(self.academic_year)
        current_year = QDate.currentDate().year()
        academic_years = []
        for year in range(current_year - 2, current_year + 3):
            academic_years.append(f"{year}-{year+1}")
        self.academic_year.addItems(academic_years)
        # Set current academic year (June-May)
        if QDate.currentDate().month() >= 6:
            self.academic_year.setCurrentText(f"{current_year}-{current_year+1}")
        else:
            self.academic_year.setCurrentText(f"{current_year-1}-{current_year}")

        # Add fields to grid
        fields = [
            ("ID", self.student_id), ("Name", self.name),
            ("Father", self.father), ("Aadhaar", self.aadhaar),
            ("DOB", self.dob), ("Join Date", self.join_date),
            ("Class", self.class_combo), ("Phone1", self.phone1),
            ("Phone2", self.phone2), ("Address", self.address),
            ("Location", self.location), ("City", self.city),
            ("Annual Fee", self.annual_fee), ("Academic Year", self.academic_year)
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
            self.annual_fee.text(),
            self.academic_year.currentText()
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
        # Reset academic year to current
        current_year = QDate.currentDate().year()
        if QDate.currentDate().month() >= 6:
            self.academic_year.setCurrentText(f"{current_year}-{current_year+1}")
        else:
            self.academic_year.setCurrentText(f"{current_year-1}-{current_year}")
