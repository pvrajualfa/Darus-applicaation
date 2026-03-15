from ui2.common_table import style_table
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
