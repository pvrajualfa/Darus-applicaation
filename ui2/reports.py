from ui2.common_table import style_table
from PySide6.QtWidgets import *
from PySide6.QtCore import QDate, Qt
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
       QTabWidget::pane {
           border: 2px solid #E1E8ED;
           background-color: #FFFFFF;
           border-radius: 8px;
           margin-top: -1px;
       }
       QTabBar::tab {
           background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                                stop:0 #F8F9FA, stop:1 #E9ECEF);
           border: 2px solid #E1E8ED;
           border-bottom: none;
           border-radius: 8px 8px 0 0;
           padding: 12px 24px;
           margin-right: 4px;
           font-weight: 600;
           font-size: 14px;
           color: #495057;
           min-width: 100px;
       }
       QTabBar::tab:selected {
           background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                                stop:0 #FFFFFF, stop:1 #F8F9FA);
           border: 2px solid #4285F4;
           border-bottom: 2px solid #FFFFFF;
           color: #4285F4;
           margin-top: -2px;
       }
       QTabBar::tab:hover:!selected {
           background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                                stop:0 #FFFFFF, stop:1 #E8F0FE);
           border-color: #4285F4;
           color: #1A73E8;
       }
       QTabBar::tab:first {
           margin-left: 8px;
       }
       QTabBar::tab:last {
           margin-right: 8px;
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

       # Balance Summary Card
       balance_card = QFrame()
       balance_layout = QVBoxLayout(balance_card)
       balance_layout.setSpacing(12)
       balance_layout.setContentsMargins(15, 15, 15, 15)
       
       self.balance_summary = QLabel("")
       self.balance_summary.setStyleSheet("""
           font-weight:bold;
           font-size:16px;
           padding:15px;
           background:#E8F5E8;
           border-radius:8px;
           color: #2E7D32;
           border: 2px solid #4CAF50;
       """)
       balance_layout.addWidget(self.balance_summary)
       layout.addWidget(balance_card)

       # Table
       self.table = QTableWidget()
       style_table(self.table)
       layout.addWidget(self.table)
       self.load_report()

   def load_report(self):
       # Get vouchers with date filtering
       from_date = self.from_date.date().toString("dd/MM/yyyy")
       to_date = self.to_date.date().toString("dd/MM/yyyy")
       type_filter = self.type_combo.currentText()
       
       # Build query
       query = "SELECT * FROM vouchers WHERE date BETWEEN ? AND ?"
       params = [from_date, to_date]
       
       if type_filter != "All":
           query += " AND type = ?"
           params.append(type_filter)
       
       query += " ORDER BY date DESC"
       vouchers = self.db.conn.execute(query, params).fetchall()
       
       # Handle empty data case
       if not vouchers:
           self.table.setRowCount(0)
           self.table.setColumnCount(10)
           self.table.setHorizontalHeaderLabels(["ID", "Date", "Type", "Head", "Subhead", "Student", "Class", "Amount", "Mode", "Note"])
           
           # Show empty state message
           self.balance_summary.setText("""
           <div style="text-align: center;">
               <div style="margin: 10px 0; color: #666;">No records found for the selected criteria</div>
               <div style="margin: 5px 0;">Bank Balance: Rs.0.00</div>
               <div style="margin: 5px 0; color: #666;">Cash Balance: Rs.0.00</div>
               <div style="margin: 10px 0; border-top: 1px solid #4CAF50; padding-top: 10px;">
                   Total Income: Rs.0.00 | Total Expense: Rs.0.00
               </div>
           </div>
           """)
           style_table(self.table)
           return
       
       self.table.setRowCount(len(vouchers))
       self.table.setColumnCount(10)
       self.table.setHorizontalHeaderLabels(["ID", "Date", "Type", "Head", "Subhead", "Student", "Class", "Amount", "Mode", "Note"])
       
       # Calculate balances (treat all cash as bank)
       total_income = 0.0
       total_expense = 0.0
       
       for row, voucher in enumerate(vouchers):
           amount = float(voucher[7])
           mode = voucher[8].lower()
           
           # Treat all cash as bank
           if mode == "cash":
               mode = "bank"
           
           for col, data in enumerate(voucher):
               if col == 8:  # Mode column
                   self.table.setItem(row, col, QTableWidgetItem(mode))
               else:
                   self.table.setItem(row, col, QTableWidgetItem(str(data)))
           
           # Calculate totals
           if voucher[2] == "Income":
               total_income += amount
           else:
               total_expense += amount
       
       # Calculate balances (all treated as bank)
       bank_balance = total_income - total_expense
       cash_balance = 0.0  # All cash treated as bank
       
       # Update balance summary
       balance_text = f"""
       <div style="text-align: center;">
           <div style="margin: 5px 0;"><strong>Bank Balance:</strong> Rs.{bank_balance:,.2f}</div>
           <div style="margin: 5px 0; color: #666;"><strong>Cash Balance:</strong> Rs.{cash_balance:,.2f} (All cash treated as bank)</div>
           <div style="margin: 10px 0; border-top: 1px solid #4CAF50; padding-top: 10px;">
               <strong>Total Income:</strong> Rs.{total_income:,.2f} | 
               <strong>Total Expense:</strong> Rs.{total_expense:,.2f}
           </div>
       </div>
       """
       self.balance_summary.setText(balance_text)
       
       style_table(self.table)

class FeePage(QWidget):
   def __init__(self):
       super().__init__()
       print("FeePage initialized - content should be visible")
       self.db = Database()
       layout = QVBoxLayout(self)
       layout.setSpacing(12)

       # Filter card
       filter_card = QFrame()
       filter_layout = QVBoxLayout(filter_card)
       filter_layout.setSpacing(12)
       filter_layout.setContentsMargins(15, 15, 15, 15)
       
       top = QHBoxLayout()
       self.class_combo = QComboBox()
       self.class_combo.addItems(["All","6th","7th","8th","9th","10th"])
       style_combo(self.class_combo)

       self.academic_year = QComboBox()
       current_year = QDate.currentDate().year()
       academic_years = []
       for year in range(current_year - 2, current_year + 2):
           academic_years.append(f"{year}-{year+1}")
       self.academic_year.addItems(academic_years)
       # Set current academic year (June-May)
       if QDate.currentDate().month() >= 6:
           self.academic_year.setCurrentText(f"{current_year}-{current_year+1}")
       else:
           self.academic_year.setCurrentText(f"{current_year-1}-{current_year}")
       style_combo(self.academic_year)

       btn_load = QPushButton("Load Report")
       style_button(btn_load)
       btn_load.clicked.connect(self.load_report)

       btn_pending = QPushButton("Pending Fees")
       style_button(btn_pending)
       btn_pending.clicked.connect(self.show_pending_fees)

       class_label = QLabel("Select Class")
       style_label(class_label)
       year_label = QLabel("Academic Year")
       style_label(year_label)

       top.addWidget(class_label)
       top.addWidget(self.class_combo)
       top.addWidget(year_label)
       top.addWidget(self.academic_year)
       top.addWidget(btn_load)
       top.addWidget(btn_pending)
       top.addStretch()

       filter_layout.addLayout(top)
       layout.addWidget(filter_card)

       # Summary
       self.summary = QLabel("")
       self.summary.setStyleSheet("""
           font-weight:bold;
           font-size:15px;
           padding:10px;
           background:#FFF3CD;
           border-radius:6px;
           color: #856404;
           border: 2px solid #FFEAA7;
       """)
       layout.addWidget(self.summary)

       # Table
       self.table = QTableWidget()
       style_table(self.table)
       print("FeePage: Table widget created")
       layout.addWidget(self.table)
       print("FeePage: Table added to layout")
       # Don't auto-load - user will click "Load Report" button
       print("FeePage: setup complete - waiting for user to click Load Report")

   def load_report(self):
       # Get students for selected academic year
       selected_academic_year = self.academic_year.currentText()
       students = self.db.get_students_by_academic_year(selected_academic_year)
       
       # Filter by class if selected
       selected_class = self.class_combo.currentText()
       if selected_class != "All":
           students = [s for s in students if s[7] == selected_class]
       
       # Handle empty data case
       if not students:
           self.table.setRowCount(0)
           self.table.setColumnCount(9)
           self.table.setHorizontalHeaderLabels([
               "Student ID", "Name", "Father", "Mobile No", "Annual Fee", 
               "Paid Amount", "Paid Installments", "Pending Amount", "Due Months"
           ])
           
           # Show empty state message
           if selected_class == "All":
               class_text = "All Classes"
           else:
               class_text = f"Class {selected_class}"
               
           summary_text = f"""
           <div style="text-align: center;">
               <div style="margin: 10px 0; color: #666;">No students found in {class_text}</div>
               <div style="margin: 5px 0;">Total Students: 0</div>
               <div style="margin: 5px 0;">Total Pending Fees: Rs.0.00</div>
               <div style="margin: 5px 0; color: #666;">Academic Year: {self.academic_year.currentText()} (June-May)</div>
           </div>
           """
           self.summary.setText(summary_text)
           style_table(self.table)
           return
       
       # Calculate fee information
       fee_data = []
       total_pending = 0.0
       total_students = len(students)  # This should be correct after filtering
       
       # Debug: Print to verify filtering
       print(f"Selected class: {selected_class}")
       print(f"Total students after filtering: {total_students}")
       for student in students:
           print(f"Student: {student[2]}, Class: {student[7]}")
       
       for student in students:
           student_id = student[1]
           name = student[2]
           father = student[3]
           phone1 = student[8]
           phone2 = student[9]
           annual_fee = float(student[13]) if student[13] else 0.0
           
           # Get paid amount from income vouchers (fees)
           paid_amount = self.get_total_paid(student_id)
           
           # Calculate monthly fee
           monthly_fee = annual_fee / 12.0
           
           # Calculate paid installments
           paid_installments = paid_amount / monthly_fee if monthly_fee > 0 else 0
           
           # Calculate pending amount
           pending_amount = annual_fee - paid_amount
           if pending_amount < 0:
               pending_amount = 0
           
           # Calculate due months
           due_months = pending_amount / monthly_fee if monthly_fee > 0 else 0
           
           fee_data.append({
               'student_id': student_id,
               'name': name,
               'father': father,
               'phone1': phone1,
               'phone2': phone2,
               'annual_fee': annual_fee,
               'monthly_fee': monthly_fee,
               'paid_amount': paid_amount,
               'paid_installments': paid_installments,
               'pending_amount': pending_amount,
               'due_months': due_months
           })
           
           total_pending += pending_amount
       
       # Display in table
       self.table.setRowCount(len(fee_data))
       self.table.setColumnCount(9)
       self.table.setHorizontalHeaderLabels([
           "Student ID", "Name", "Father", "Mobile No", "Annual Fee", 
           "Paid Amount", "Paid Installments", "Pending Amount", "Due Months"
       ])
       
       for row, data in enumerate(fee_data):
           self.table.setItem(row, 0, QTableWidgetItem(data['student_id']))
           self.table.setItem(row, 1, QTableWidgetItem(data['name']))
           self.table.setItem(row, 2, QTableWidgetItem(data['father']))
           
           # Combine phone numbers
           phones = f"{data['phone1']}"
           if data['phone2']:
               phones += f", {data['phone2']}"
           self.table.setItem(row, 3, QTableWidgetItem(phones))
           
           self.table.setItem(row, 4, QTableWidgetItem(f"Rs.{data['annual_fee']:,.2f}"))
           self.table.setItem(row, 5, QTableWidgetItem(f"Rs.{data['paid_amount']:,.2f}"))
           self.table.setItem(row, 6, QTableWidgetItem(f"{data['paid_installments']:.1f}"))
           self.table.setItem(row, 7, QTableWidgetItem(f"Rs.{data['pending_amount']:,.2f}"))
           self.table.setItem(row, 8, QTableWidgetItem(f"{data['due_months']:.1f}"))
       
       # Update summary
       if selected_class == "All":
           class_text = "All Classes"
       else:
           class_text = f"Class {selected_class}"
           
       summary_text = f"""
       <div style="text-align: center;">
           <div style="margin: 5px 0;"><strong>Total Students in {class_text}:</strong> {total_students}</div>
           <div style="margin: 5px 0;"><strong>Total Pending Fees:</strong> Rs.{total_pending:,.2f}</div>
           <div style="margin: 5px 0; color: #666;">Academic Year: {self.academic_year.currentText()} (June-May)</div>
       </div>
       """
       self.summary.setText(summary_text)
       
       style_table(self.table)

   def get_academic_year_dates(self):
       """Get start and end dates for the selected academic year"""
       selected_year = self.academic_year.currentText()
       start_year, end_year = map(int, selected_year.split('-'))
       
       # Academic year runs from June to May
       start_date = f"01/06/{start_year}"
       end_date = f"31/05/{end_year}"
       
       return start_date, end_date

   def get_total_paid(self, student_id):
       """Get total amount paid by student from income vouchers for selected academic year"""
       start_date, end_date = self.get_academic_year_dates()
       
       result = self.db.conn.execute(
           "SELECT COALESCE(SUM(amount), 0) FROM vouchers WHERE student_name=? AND type='Income' AND date BETWEEN ? AND ?",
           (student_id, start_date, end_date)
       ).fetchone()
       return float(result[0]) if result and result[0] else 0.0

   def show_pending_fees(self):
       """Show only students with pending fees"""
       # Get students for selected academic year
       selected_academic_year = self.academic_year.currentText()
       students = self.db.get_students_by_academic_year(selected_academic_year)
       
       # Filter by class if selected
       selected_class = self.class_combo.currentText()
       if selected_class != "All":
           students = [s for s in students if s[7] == selected_class]
       
       # Get only students with pending fees
       pending_students = []
       total_pending = 0.0
       
       for student in students:
           student_id = student[1]
           name = student[2]
           father = student[3]
           phone1 = student[8]
           phone2 = student[9]
           annual_fee = float(student[13]) if student[13] else 0.0
           
           paid_amount = self.get_total_paid(student_id)
           pending_amount = annual_fee - paid_amount
           
           if pending_amount > 0:
               monthly_fee = annual_fee / 12.0
               paid_installments = paid_amount / monthly_fee if monthly_fee > 0 else 0
               due_months = pending_amount / monthly_fee if monthly_fee > 0 else 0
               
               pending_students.append({
                   'student_id': student_id,
                   'name': name,
                   'father': father,
                   'phone1': phone1,
                   'phone2': phone2,
                   'annual_fee': annual_fee,
                   'monthly_fee': monthly_fee,
                   'paid_amount': paid_amount,
                   'paid_installments': paid_installments,
                   'pending_amount': pending_amount,
                   'due_months': due_months
               })
               total_pending += pending_amount
       
       # Handle empty data case
       if not pending_students:
           self.table.setRowCount(0)
           self.table.setColumnCount(9)
           self.table.setHorizontalHeaderLabels([
               "Student ID", "Name", "Father", "Mobile No", "Annual Fee", 
               "Paid Amount", "Paid Installments", "Pending Amount", "Due Months"
           ])
           
           # Show empty state message
           if selected_class == "All":
               class_text = "All Classes"
           else:
               class_text = f"Class {selected_class}"
               
           summary_text = f"""
           <div style="text-align: center;">
               <div style="margin: 10px 0; color: #28a745;"><strong>No pending fees found in {class_text}</strong></div>
               <div style="margin: 5px 0;">All students have paid their fees</div>
               <div style="margin: 5px 0; color: #666;">Academic Year: {self.academic_year.currentText()} (June-May)</div>
           </div>
           """
           self.summary.setText(summary_text)
           style_table(self.table)
           return
       
       # Display pending fees in table
       self.table.setRowCount(len(pending_students))
       self.table.setColumnCount(9)
       self.table.setHorizontalHeaderLabels([
           "Student ID", "Name", "Father", "Mobile No", "Annual Fee", 
           "Paid Amount", "Paid Installments", "Pending Amount", "Due Months"
       ])
       
       for row, data in enumerate(pending_students):
           self.table.setItem(row, 0, QTableWidgetItem(data['student_id']))
           self.table.setItem(row, 1, QTableWidgetItem(data['name']))
           self.table.setItem(row, 2, QTableWidgetItem(data['father']))
           
           # Combine phone numbers
           phones = f"{data['phone1']}"
           if data['phone2']:
               phones += f", {data['phone2']}"
           self.table.setItem(row, 3, QTableWidgetItem(phones))
           
           self.table.setItem(row, 4, QTableWidgetItem(f"Rs.{data['annual_fee']:,.2f}"))
           self.table.setItem(row, 5, QTableWidgetItem(f"Rs.{data['paid_amount']:,.2f}"))
           self.table.setItem(row, 6, QTableWidgetItem(f"{data['paid_installments']:.1f}"))
           self.table.setItem(row, 7, QTableWidgetItem(f"Rs.{data['pending_amount']:,.2f}"))
           self.table.setItem(row, 8, QTableWidgetItem(f"{data['due_months']:.1f}"))
       
       # Update summary for pending fees
       if selected_class == "All":
           class_text = "All Classes"
       else:
           class_text = f"Class {selected_class}"
           
       summary_text = f"""
       <div style="text-align: center;">
           <div style="margin: 5px 0; color: #D32F2F;"><strong>Students with Pending Fees in {class_text}:</strong> {len(pending_students)}</div>
           <div style="margin: 5px 0; color: #D32F2F;"><strong>Total Pending Amount:</strong> Rs.{total_pending:,.2f}</div>
           <div style="margin: 5px 0; color: #666;">Academic Year: {self.academic_year.currentText()} (June-May)</div>
       </div>
       """
       self.summary.setText(summary_text)
       
       style_table(self.table)
