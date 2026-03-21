from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QDate, Signal
from PySide6.QtGui import QTextDocument
from PySide6.QtPrintSupport import QPrintDialog
from ui2.database import Database
from ui2.header import PageHeader
from ui2.common_table import style_table
from ui2.vouchers import VoucherPage
from ui2.common_form import (style_lineedit, style_combo, style_button, style_dateedit, style_label, 
                              EnhancedLineEdit, EnhancedComboBox, EnhancedDateEdit,
                              load_heads_into_combo, load_subheads_into_combo, load_payment_modes_into_combo)

class VoucherListPage(QWidget):
    voucher_updated = Signal()
    
    def __init__(self):
        super().__init__()
        self.db = Database()
        
        layout = QVBoxLayout(self)
        layout.addWidget(PageHeader("Voucher List"))
        
        # Action buttons
        action_layout = QHBoxLayout()
        self.btn_new_voucher = QPushButton("Add New Voucher")
        self.btn_refresh = QPushButton("Refresh")
        self.btn_print = QPushButton("Print List")
        self.btn_print_receipt = QPushButton("Print Receipt")
        self.btn_print_receipt.setEnabled(False)
        self.btn_delete = QPushButton("Delete Selected")
        self.btn_delete.setEnabled(False)
        
        # Connect signals
        self.btn_refresh.clicked.connect(self.load_data)
        self.btn_new_voucher.clicked.connect(self.open_new_voucher_form)
        self.btn_print.clicked.connect(self.print_voucher_list)
        self.btn_print_receipt.clicked.connect(self.print_single_receipt)
        self.btn_delete.clicked.connect(self.delete_selected_voucher)
        
        action_layout.addWidget(self.btn_new_voucher)
        action_layout.addWidget(self.btn_refresh)
        action_layout.addWidget(self.btn_print)
        action_layout.addWidget(self.btn_print_receipt)
        action_layout.addStretch()
        action_layout.addWidget(self.btn_delete)
        layout.addLayout(action_layout)
        
        # Table
        self.table = QTableWidget()
        style_table(self.table)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSortingEnabled(True)
        self.table.cellDoubleClicked.connect(self.edit_voucher)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        layout.addWidget(self.table)
        
        self.load_data()
    
    def on_selection_changed(self):
        """Enable/disable buttons based on selection"""
        has_selection = bool(self.table.selectedItems())
        self.btn_delete.setEnabled(has_selection)
        self.btn_print_receipt.setEnabled(has_selection)
    
    def edit_voucher(self, row, column):
        """Open voucher edit form with selected voucher data"""
        voucher_data = []
        for col in range(self.table.columnCount()):
            item = self.table.item(row, col)
            voucher_data.append(item.text() if item else "")
        
        # Open voucher edit dialog
        dialog = VoucherEditDialog(voucher_data, self)
        if dialog.exec() == QDialog.Accepted:
            self.load_data()
            self.voucher_updated.emit()
    
    def open_new_voucher_form(self):
        """Open new voucher entry form"""
        dialog = VoucherEditDialog([], self)
        if dialog.exec() == QDialog.Accepted:
            self.load_data()
            self.voucher_updated.emit()
    
    def delete_selected_voucher(self):
        """Delete the selected voucher"""
        current_row = self.table.currentRow()
        if current_row < 0:
            return
        
        voucher_id_item = self.table.item(current_row, 0)  # ID column
        voucher_type_item = self.table.item(current_row, 2)  # Type column
        voucher_amount_item = self.table.item(current_row, 7)  # Amount column
        
        if not voucher_id_item or not voucher_type_item or not voucher_amount_item:
            return
        
        voucher_id = voucher_id_item.text()
        voucher_type = voucher_type_item.text()
        voucher_amount = voucher_amount_item.text()
        
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete this {voucher_type} voucher of Rs.{voucher_amount}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.db.conn.execute("DELETE FROM vouchers WHERE id=?", (voucher_id,))
                self.db.conn.commit()
                QMessageBox.information(self, "Success", "Voucher deleted successfully")
                self.load_data()
                self.voucher_updated.emit()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to delete voucher: {str(e)}")
    
    def load_data(self):
        """Load all vouchers from database"""
        try:
            # Get all vouchers ordered by date DESC
            vouchers = self.db.conn.execute("SELECT * FROM vouchers ORDER BY date DESC").fetchall()
            
            self.table.setRowCount(len(vouchers))
            self.table.setColumnCount(11)  # Add one more column for months paid
            self.table.setHorizontalHeaderLabels(["ID", "Date", "Type", "Head", "Subhead", "Student", "Class", "Amount", "Mode", "Months Paid", "Note"])
            
            for row, voucher in enumerate(vouchers):
                # Get basic voucher data
                for col in range(8):  # ID, Date, Type, Head, Subhead, Student, Class, Amount, Mode
                    self.table.setItem(row, col, QTableWidgetItem(str(voucher[col])))
                
                # Calculate months paid for fee payments
                months_paid = ""
                if voucher[2] == "Income" and "fees" in voucher[3].lower() and voucher[5]:  # Income, Fees head, and has student
                    annual_fee = self.get_student_annual_fee(voucher[5])
                    if annual_fee > 0:
                        monthly_fee = annual_fee / 12.0
                        amount = float(voucher[7])
                        months = amount / monthly_fee
                        months_paid = f"{months:.1f} months"
                    else:
                        months_paid = "N/A"
                else:
                    months_paid = "N/A"
                
                self.table.setItem(row, 8, QTableWidgetItem(months_paid))
                self.table.setItem(row, 9, QTableWidgetItem(str(voucher[9]) if voucher[9] else ""))  # Note
            
            # Adjust column widths
            self.table.resizeColumnsToContents()
            style_table(self.table)
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load vouchers: {str(e)}")
    
    def get_student_annual_fee(self, student_id):
        """Get annual fee for a student"""
        try:
            result = self.db.conn.execute(
                "SELECT annual_fee FROM students WHERE student_id=?",
                (student_id,)
            ).fetchone()
            return float(result[0]) if result and result[0] else 0.0
        except:
            return 0.0
    
    def print_single_receipt(self):
        """Print receipt for selected voucher"""
        try:
            current_row = self.table.currentRow()
            if current_row < 0:
                return
            
            # Get selected voucher data
            voucher_data = []
            for col in range(self.table.columnCount()):
                item = self.table.item(current_row, col)
                voucher_data.append(item.text() if item else "")
            
            # Create print dialog
            print_dialog = QPrintDialog(self)
            print_dialog.setOption(QPrintDialog.PrintSelection, False)
            
            if print_dialog.exec() == QDialog.Accepted:
                printer = print_dialog.printer()
                
                # Create document for printing
                document = QTextDocument()
                document.setPageSize(printer.pageRect().size())
                
                # Build HTML content for receipt
                html_content = self.generate_receipt_html(voucher_data)
                document.setHtml(html_content)
                
                # Print
                document.print(printer)
                
                QMessageBox.information(self, "Success", "Receipt sent to printer successfully!")
                
        except Exception as e:
            QMessageBox.warning(self, "Print Error", f"Failed to print receipt: {str(e)}")
    
    def generate_receipt_html(self, voucher_data):
        """Generate HTML content for single voucher receipt"""
        if len(voucher_data) < 11:
            return "<html><body><p>Error: Invalid voucher data</p></body></html>"
        
        # Extract voucher information
        voucher_id = voucher_data[0]
        date = voucher_data[1]
        typ = voucher_data[2]
        head = voucher_data[3]
        subhead = voucher_data[4]
        student = voucher_data[5]
        class_name = voucher_data[6]
        amount = float(voucher_data[7])
        mode = voucher_data[8]
        months_paid = voucher_data[9]  # New months paid column
        note = voucher_data[10] if len(voucher_data) > 10 else ""
        
        # Generate HTML
        html = f"""
        <html>
        <head>
            <style>
                body {{ 
                    font-family: Arial, sans-serif; 
                    margin: 40px; 
                    line-height: 1.6;
                }}
                .receipt-header {{ 
                    text-align: center; 
                    border-bottom: 3px double #333; 
                    padding-bottom: 20px; 
                    margin-bottom: 30px;
                }}
                .receipt-title {{ 
                    font-size: 24px; 
                    font-weight: bold; 
                    color: #2c3e50; 
                    margin-bottom: 10px;
                }}
                .receipt-subtitle {{ 
                    font-size: 14px; 
                    color: #7f8c8d; 
                    margin-bottom: 5px;
                }}
                .receipt-body {{ 
                    margin: 20px 0; 
                }}
                .receipt-field {{ 
                    margin: 10px 0; 
                    display: flex; 
                    justify-content: space-between;
                }}
                .field-label {{ 
                    font-weight: bold; 
                    color: #34495e; 
                    min-width: 120px;
                }}
                .field-value {{ 
                    color: #2c3e50; 
                }}
                .amount-section {{ 
                    background-color: #ecf0f1; 
                    padding: 20px; 
                    border-radius: 8px; 
                    margin: 20px 0; 
                    text-align: center;
                }}
                .amount {{ 
                    font-size: 28px; 
                    font-weight: bold; 
                    color: {'#27ae60' if typ == 'Income' else '#e74c3c'};
                }}
                .note-section {{ 
                    margin-top: 30px; 
                    padding: 15px; 
                    background-color: #f8f9fa; 
                    border-left: 4px solid #3498db; 
                    border-radius: 4px;
                }}
                .footer {{ 
                    text-align: center; 
                    margin-top: 40px; 
                    color: #95a5a6; 
                    font-size: 12px;
                }}
                .income {{ color: #27ae60; }}
                .expense {{ color: #e74c3c; }}
                .highlight {{ 
                    background-color: #fff3cd; 
                    padding: 2px 6px; 
                    border-radius: 4px; 
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <div class="receipt-header">
                <div class="receipt-title">Darus Salah - Education Center</div>
                <div class="receipt-subtitle">Voucher Receipt</div>
                <div class="receipt-subtitle">Receipt No: {voucher_id}</div>
            </div>
            
            <div class="receipt-body">
                <div class="receipt-field">
                    <span class="field-label">Date:</span>
                    <span class="field-value">{date}</span>
                </div>
                
                <div class="receipt-field">
                    <span class="field-label">Type:</span>
                    <span class="field-value {typ.lower()}">{typ}</span>
                </div>
                
                <div class="receipt-field">
                    <span class="field-label">Category:</span>
                    <span class="field-value">{head} - {subhead}</span>
                </div>
                
                {f'''<div class="receipt-field">
                    <span class="field-label">Student:</span>
                    <span class="field-value">{student} (Class: {class_name})</span>
                </div>''' if student else ''}
                
                <div class="receipt-field">
                    <span class="field-label">Payment Mode:</span>
                    <span class="field-value">{mode}</span>
                </div>
                
                {f'''<div class="receipt-field">
                    <span class="field-label">Months Paid:</span>
                    <span class="field-value highlight">{months_paid}</span>
                </div>''' if months_paid and months_paid != "N/A" else ''}
                
                <div class="amount-section">
                    <div class="field-label">Amount:</div>
                    <div class="amount">Rs.{amount:,.2f}</div>
                </div>
                
                {f'''<div class="note-section">
                    <div class="field-label">Note:</div>
                    <div class="field-value">{note}</div>
                </div>''' if note else ''}
            </div>
            
            <div class="footer">
                <p>Generated on: {QDate.currentDate().toString('dd/MM/yyyy HH:mm')}</p>
                <p>Darus Salah Management System</p>
                <p>Thank you for your payment!</p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def print_voucher_list(self):
        """Print the current voucher list"""
        try:
            # Get all vouchers for printing
            vouchers = self.db.conn.execute("SELECT * FROM vouchers ORDER BY date DESC").fetchall()
            
            # Create print dialog
            print_dialog = QPrintDialog(self)
            print_dialog.setOption(QPrintDialog.PrintSelection, False)
            
            if print_dialog.exec() == QDialog.Accepted:
                printer = print_dialog.printer()
                
                # Create document for printing
                document = QTextDocument()
                document.setPageSize(printer.pageRect().size())
                
                # Build HTML content
                html_content = self.generate_print_html(vouchers)
                document.setHtml(html_content)
                
                # Print
                document.print(printer)
                
                QMessageBox.information(self, "Success", "Voucher list sent to printer successfully!")
                
        except Exception as e:
            QMessageBox.warning(self, "Print Error", f"Failed to print voucher list: {str(e)}")
    
    def generate_print_html(self, vouchers):
        """Generate HTML content for printing"""
        # Calculate totals
        income_total = sum(float(v[7]) for v in vouchers if v[2] == "Income")
        expense_total = sum(float(v[7]) for v in vouchers if v[2] == "Expense")
        net_total = income_total - expense_total
        
        # Generate HTML
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ text-align: center; color: #2c3e50; }}
                h2 {{ color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 5px; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th {{ background-color: #3498db; color: white; padding: 8px; text-align: left; font-weight: bold; }}
                td {{ padding: 6px; border: 1px solid #ddd; }}
                tr:nth-child(even) {{ background-color: #f2f2f2; }}
                .income {{ color: #27ae60; font-weight: bold; }}
                .expense {{ color: #e74c3c; font-weight: bold; }}
                .totals {{ margin-top: 30px; padding: 15px; background-color: #ecf0f1; border-radius: 5px; }}
                .total-row {{ margin: 5px 0; font-weight: bold; }}
                .header-info {{ margin-bottom: 20px; color: #7f8c8d; }}
            </style>
        </head>
        <body>
            <h1>Darus Salah - Education and Research Center</h1>
            
            <div class="header-info">
                <h2>Complete Voucher List</h2>
                <p><strong>Generated on:</strong> {QDate.currentDate().toString('dd/MM/yyyy')}</p>
                <p><strong>Total Records:</strong> {len(vouchers)}</p>
            </div>
            
            <table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Type</th>
                        <th>Head</th>
                        <th>Subhead</th>
                        <th>Student</th>
                        <th>Class</th>
                        <th>Amount</th>
                        <th>Mode</th>
                        <th>Note</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        # Add voucher rows
        for voucher in vouchers:
            row_class = "income" if voucher[2] == "Income" else "expense"
            html += f"""
                    <tr>
                        <td>{voucher[1]}</td>
                        <td class="{row_class}">{voucher[2]}</td>
                        <td>{voucher[3]}</td>
                        <td>{voucher[4]}</td>
                        <td>{voucher[5]}</td>
                        <td>{voucher[6]}</td>
                        <td class="{row_class}">Rs.{float(voucher[7]):,.2f}</td>
                        <td>{voucher[8]}</td>
                        <td>{voucher[9]}</td>
                    </tr>
            """
        
        html += f"""
                </tbody>
            </table>
            
            <div class="totals">
                <div class="total-row">Total Income: <span class="income">Rs.{income_total:,.2f}</span></div>
                <div class="total-row">Total Expenses: <span class="expense">Rs.{expense_total:,.2f}</span></div>
                <div class="total-row" style="font-size: 1.2em; border-top: 2px solid #34495e; padding-top: 10px; margin-top: 15px;">
                    Net Balance: <span style="color: {'#27ae60' if net_total >= 0 else '#e74c3c'};">Rs.{net_total:,.2f}</span>
                </div>
            </div>
            
            <div style="margin-top: 50px; text-align: center; color: #95a5a6; font-size: 0.9em;">
                <p>Generated by Darus Salah Management System</p>
            </div>
        </body>
        </html>
        """
        
        return html


class VoucherEditDialog(QDialog):
    def __init__(self, voucher_data, parent=None):
        super().__init__(parent)
        self.db = Database()
        self.voucher_data = voucher_data
        self.setWindowTitle("Edit Voucher" if voucher_data else "Add New Voucher")
        self.setFixedSize(600, 500)
        
        # Apply light theme like StudentRegistration
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
        layout.setSpacing(15)
        
        layout.addWidget(PageHeader("Voucher Registration"))
        
        # Form card
        card = QFrame()
        grid = QGridLayout(card)
        grid.setSpacing(12)
        
        # Create form fields with enhanced widgets
        self.date = EnhancedDateEdit(QDate.currentDate(), calendarPopup=True)
        self.date.setDisplayFormat("dd/MM/yyyy")
        style_dateedit(self.date)
        
        self.type_combo = EnhancedComboBox()
        self.type_combo.addItems(["Select Income/Expense", "Income", "Expense"])
        style_combo(self.type_combo)
        
        self.head = EnhancedComboBox()
        style_combo(self.head)
        
        self.subhead = EnhancedComboBox()
        style_combo(self.subhead)
        
        self.student_lbl = QLabel("Student:")
        style_label(self.student_lbl)
        self.student_combo = EnhancedComboBox()
        style_combo(self.student_combo)
        
        self.class_lbl = QLabel("Class:")
        style_label(self.class_lbl)
        self.class_edit = EnhancedLineEdit()
        self.class_edit.setReadOnly(True)
        style_lineedit(self.class_edit)
        
        self.amount = EnhancedLineEdit()
        style_lineedit(self.amount)
        
        self.mode = EnhancedComboBox()
        style_combo(self.mode)
        
        self.note = EnhancedLineEdit()
        style_lineedit(self.note)
        
        # Add fields to grid with styled labels
        date_lbl = QLabel("Date:")
        style_label(date_lbl)
        grid.addWidget(date_lbl, 0, 0)
        grid.addWidget(self.date, 0, 1)
        
        type_lbl = QLabel("Type:")
        style_label(type_lbl)
        grid.addWidget(type_lbl, 1, 0)
        grid.addWidget(self.type_combo, 1, 1)
        
        head_lbl = QLabel("Head:")
        style_label(head_lbl)
        grid.addWidget(head_lbl, 2, 0)
        grid.addWidget(self.head, 2, 1)
        
        subhead_lbl = QLabel("Subhead:")
        style_label(subhead_lbl)
        grid.addWidget(subhead_lbl, 3, 0)
        grid.addWidget(self.subhead, 3, 1)
        
        grid.addWidget(self.student_lbl, 4, 0)
        grid.addWidget(self.student_combo, 4, 1)
        
        grid.addWidget(self.class_lbl, 5, 0)
        grid.addWidget(self.class_edit, 5, 1)
        
        amount_lbl = QLabel("Amount:")
        style_label(amount_lbl)
        grid.addWidget(amount_lbl, 6, 0)
        grid.addWidget(self.amount, 6, 1)
        
        mode_lbl = QLabel("Payment Mode:")
        style_label(mode_lbl)
        grid.addWidget(mode_lbl, 7, 0)
        grid.addWidget(self.mode, 7, 1)
        
        note_lbl = QLabel("Note:")
        style_label(note_lbl)
        grid.addWidget(note_lbl, 8, 0)
        grid.addWidget(self.note, 8, 1)
        
        layout.addWidget(card)
        
        # Dialog buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        # Style the dialog buttons
        for button in button_box.buttons():
            style_button(button)
        button_box.accepted.connect(self.save_voucher)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        # Initialize data
        self.load_initial_data()
        
        # If editing, populate the form with existing data
        if voucher_data:
            self.populate_form()
        
        # Connect signals
        self.type_combo.currentTextChanged.connect(self.load_heads)
        self.head.currentIndexChanged.connect(self.load_subheads)
        self.student_combo.currentIndexChanged.connect(self.load_student_class)
        
        # Hide student section initially
        self.student_lbl.setVisible(False)
        self.student_combo.setVisible(False)
        self.class_lbl.setVisible(False)
        self.class_edit.setVisible(False)
    
    def load_initial_data(self):
        """Load initial data for combos"""
        # Load students
        students = self.db.get_students()
        self.student_combo.clear()
        self.student_combo.addItem("Select Student", None)
        for student in students:
            display_name = f"{student[2]} ({student[1]})"  # Name (Student ID)
            self.student_combo.addItem(display_name, student[1])  # Store student_id as data
        
        # Load payment modes
        self.mode.clear()
        self.mode.addItems(["Cash", "Bank Transfer", "Cheque", "Online Payment", "UPI"])
        
        # Load heads
        self.load_heads()
    
    def load_heads(self):
        """Load heads based on selected type"""
        self.head.clear()
        self.head.addItem("Select Head", None)
        
        type_text = self.type_combo.currentText()
        if type_text in ["Income", "Expense"]:
            heads = self.db.get_heads(type_text)
            for head in heads:
                self.head.addItem(head[1], head[0])  # Store head_id as data
    
    def load_subheads(self):
        """Load subheads based on selected head"""
        self.subhead.clear()
        self.subhead.addItem("Select Subhead", None)
        
        head_id = self.head.currentData()
        if head_id:
            subheads = self.db.get_subheads_by_headid(head_id)
            for subhead in subheads:
                self.subhead.addItem(subhead[1], subhead[0])  # Store subhead_id as data
        
        # Show/hide student section based on head
        head_text = self.head.currentText().lower()
        show_student = "fees" in head_text
        self.student_lbl.setVisible(show_student)
        self.student_combo.setVisible(show_student)
        self.class_lbl.setVisible(show_student)
        self.class_edit.setVisible(show_student)
    
    def load_student_class(self):
        """Load student class when student is selected"""
        student_id = self.student_combo.currentData()
        if student_id:
            student = self.db.conn.execute(
                "SELECT class FROM students WHERE student_id=?", 
                (student_id,)
            ).fetchone()
            if student:
                self.class_edit.setText(student[0])
        else:
            self.class_edit.clear()
    
    def populate_form(self):
        """Populate the form with existing voucher data"""
        if len(self.voucher_data) >= 10:
            self.date.setDate(QDate.fromString(self.voucher_data[1], "dd/MM/yyyy"))
            
            # Set type
            type_index = self.type_combo.findText(self.voucher_data[2])
            if type_index >= 0:
                self.type_combo.setCurrentIndex(type_index)
            
            # Load heads and subheads based on type
            self.load_heads()
            
            # Set head
            head_index = self.head.findText(self.voucher_data[3])
            if head_index >= 0:
                self.head.setCurrentIndex(head_index)
            
            # Load subheads
            self.load_subheads()
            
            # Set subhead
            subhead_index = self.subhead.findText(self.voucher_data[4])
            if subhead_index >= 0:
                self.subhead.setCurrentIndex(subhead_index)
            
            # Set student
            student_index = self.student_combo.findText(self.voucher_data[5])
            if student_index >= 0:
                self.student_combo.setCurrentIndex(student_index)
            
            self.class_edit.setText(self.voucher_data[6])
            self.amount.setText(self.voucher_data[7])
            
            # Set mode
            mode_index = self.mode.findText(self.voucher_data[8])
            if mode_index >= 0:
                self.mode.setCurrentIndex(mode_index)
            
            self.note.setText(self.voucher_data[9])
    
    def save_voucher(self):
        """Save voucher data"""
        # Validate required fields
        if not self.type_combo.currentText() or self.type_combo.currentText() == "Select Income/Expense":
            QMessageBox.warning(self, "Validation Error", "Please select voucher type")
            return
        
        if not self.head.currentText() or not self.subhead.currentText():
            QMessageBox.warning(self, "Validation Error", "Please select head and subhead")
            return
        
        if not self.amount.text():
            QMessageBox.warning(self, "Validation Error", "Please enter amount")
            return
        
        try:
            # Delete existing voucher if editing
            if self.voucher_data:
                old_voucher_id = self.voucher_data[0]
                self.db.conn.execute("DELETE FROM vouchers WHERE id=?", (old_voucher_id,))
            
            # Save new/updated voucher
            date_str = self.date.date().toString("dd/MM/yyyy")
            typ = self.type_combo.currentText()
            head = self.head.currentText()
            subhead = self.subhead.currentText()
            student_name = self.student_combo.currentText().split(" (")[0] if self.student_combo.currentData() else ""
            class_name = self.class_edit.text()
            amount = float(self.amount.text())
            mode = self.mode.currentText()
            note = self.note.text()
            
            self.db.add_voucher(date_str, typ, head, subhead, student_name, class_name, amount, mode, note)
            self.accept()
            
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter a valid amount")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save voucher: {str(e)}")
