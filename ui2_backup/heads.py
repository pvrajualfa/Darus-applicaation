from ui2.common_table import style_table
from ui2.common_form import style_label, style_button, style_groupbox, style_lineedit, style_combo
from PySide6.QtWidgets import *
from database import Database
from ui2.header import PageHeader
from PySide6.QtCore import Qt, Signal


class HeadPage(QWidget):
    head_added = Signal()
    subhead_added = Signal()

    def __init__(self):
        super().__init__()
        self.db = Database()
        self.entry_mode = "HEAD"

        layout = QVBoxLayout(self)
        layout.addWidget(PageHeader("Manage Heads"))

        # Create main horizontal layout for two sections
        main_layout = QHBoxLayout()
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # ================= ADD HEAD SECTION (LEFT) =================
        head_widget = QWidget()
        head_widget.setFixedSize(500, 300)
        head_layout = QVBoxLayout(head_widget)
        head_layout.setSpacing(15)
        head_layout.setContentsMargins(10, 10, 10, 10)
        
        head_group = QGroupBox("Add Head")
        head_group_layout = QVBoxLayout()
        head_group_layout.setSpacing(15)
        head_group_layout.setContentsMargins(10, 10, 10, 10)
        
        # Initialize widgets
        self.head_type = QComboBox()
        self.head_type.addItems(["Income", "Expense"])
        self.head_type.setMinimumHeight(35)
        self.head_type.setView(QListView())
        style_combo(self.head_type)
        
        self.head_name = QLineEdit()
        self.head_name.setMinimumHeight(35)
        style_lineedit(self.head_name)
        
        self.btn_add_head = QPushButton("Add Head")
        self.btn_add_head.setFixedWidth(120)
        style_button(self.btn_add_head)
        
        # Type row
        type_row = QHBoxLayout()
        type_label = QLabel("Type:")
        style_label(type_label)
        type_row.addWidget(type_label)
        type_row.addWidget(self.head_type)
        head_group_layout.addLayout(type_row)
        
        # Head Name row
        name_row = QHBoxLayout()
        name_label = QLabel("Head Name:")
        style_label(name_label)
        name_row.addWidget(name_label)
        name_row.addWidget(self.head_name)
        head_group_layout.addLayout(name_row)
        
        # Button
        head_button_layout = QHBoxLayout()
        head_button_layout.addStretch()
        head_button_layout.addWidget(self.btn_add_head)
        head_button_layout.addStretch()
        head_group_layout.addLayout(head_button_layout)
        
        head_group.setLayout(head_group_layout)
        style_groupbox(head_group)
        head_layout.addWidget(head_group)
        
        head_widget.setLayout(head_layout)
        main_layout.addWidget(head_widget)

        # ================= ADD SUBHEAD SECTION (RIGHT) =================
        subhead_widget = QWidget()
        subhead_widget.setFixedSize(500, 300)
        subhead_layout = QVBoxLayout(subhead_widget)
        subhead_layout.setSpacing(15)
        subhead_layout.setContentsMargins(10, 10, 10, 10)
        
        sub_group = QGroupBox("Add Subhead")
        sub_group_layout = QVBoxLayout()
        sub_group_layout.setSpacing(15)
        sub_group_layout.setContentsMargins(10, 10, 10, 10)
        
        # Initialize widgets
        self.sub_type = QComboBox()
        self.sub_type.addItems(["Income", "Expense"])
        self.sub_type.setMinimumHeight(35)
        self.sub_type.setView(QListView())
        style_combo(self.sub_type)
        
        self.sub_head_combo = QComboBox()
        self.sub_head_combo.setMinimumHeight(35)
        self.sub_head_combo.setView(QListView())
        style_combo(self.sub_head_combo)
        
        self.sub_name = QLineEdit()
        self.sub_name.setMinimumHeight(35)
        style_lineedit(self.sub_name)
        
        self.btn_add_sub = QPushButton("Add Subhead")
        self.btn_add_sub.setFixedWidth(120)
        style_button(self.btn_add_sub)
        
        # Type row
        sub_type_row = QHBoxLayout()
        sub_type_label = QLabel("Type:")
        style_label(sub_type_label)
        sub_type_row.addWidget(sub_type_label)
        sub_type_row.addWidget(self.sub_type)
        sub_group_layout.addLayout(sub_type_row)
        
        # Head row
        head_row = QHBoxLayout()
        head_label = QLabel("Head:")
        style_label(head_label)
        head_row.addWidget(head_label)
        head_row.addWidget(self.sub_head_combo)
        sub_group_layout.addLayout(head_row)
        
        # Subhead row
        subhead_row = QHBoxLayout()
        subhead_label = QLabel("Subhead:")
        style_label(subhead_label)
        subhead_row.addWidget(subhead_label)
        subhead_row.addWidget(self.sub_name)
        sub_group_layout.addLayout(subhead_row)
        
        # Button
        sub_button_layout = QHBoxLayout()
        sub_button_layout.addStretch()
        sub_button_layout.addWidget(self.btn_add_sub)
        sub_button_layout.addStretch()
        sub_group_layout.addLayout(sub_button_layout)
        
        sub_group.setLayout(sub_group_layout)
        style_groupbox(sub_group)
        subhead_layout.addWidget(sub_group)
        
        subhead_widget.setLayout(subhead_layout)
        main_layout.addWidget(subhead_widget)
        main_layout.addStretch()
        
        layout.addLayout(main_layout)

        # ================= TABLE =================
        self.table = QTableWidget()
        style_table(self.table)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.cellDoubleClicked.connect(self.select_row)
        layout.addWidget(self.table)

        # ================= DELETE BUTTON =================
        btn_layout = QHBoxLayout()
        self.btn_delete = QPushButton("Delete")
        style_button(self.btn_delete)
        self.btn_delete.setEnabled(False)

        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_delete)
        layout.addLayout(btn_layout)

        # ================= CONNECTIONS =================
        self.btn_add_head.clicked.connect(self.add_head)
        self.btn_add_sub.clicked.connect(self.add_subhead)
        self.btn_delete.clicked.connect(self.delete_selected)
        self.head_type.currentTextChanged.connect(self.load_heads)
        self.sub_type.currentTextChanged.connect(self.load_heads)

        # ================= INITIAL LOAD =================
        self.load_data()

    def add_head(self):
        typ = self.head_type.currentText()
        head = self.head_name.text().strip()

        if not head:
            QMessageBox.warning(self, "Warning", "Enter head name")
            return

        try:
            self.db.add_head(typ, head)
            QMessageBox.information(self, "Success", "Head added successfully")
            self.head_name.clear()
            self.load_data()
            self.head_added.emit()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to add head: {str(e)}")

    def add_subhead(self):
        typ = self.sub_type.currentText()
        head = self.sub_head_combo.currentText()
        sub = self.sub_name.text().strip()

        if not head or head == "Select Head":
            QMessageBox.warning(self, "Warning", "Select head")
            return

        if not sub:
            QMessageBox.warning(self, "Warning", "Enter subhead name")
            return

        try:
            self.db.add_subhead(typ, head, sub)
            QMessageBox.information(self, "Success", "Subhead added successfully")
            self.sub_name.clear()
            self.load_data()
            self.subhead_added.emit()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to add subhead: {str(e)}")

    def load_heads(self):
        self.sub_head_combo.clear()
        self.sub_head_combo.addItem("Select Head", None)
        
        typ = self.sub_type.currentText()
        heads = self.db.get_heads(typ)
        
        for head in heads:
            self.sub_head_combo.addItem(head[1], head[0])

    def load_data(self):
        data = []
        
        heads = self.db.get_all_heads()
        for head in heads:
            data.append(("HEAD", head[1], head[0], "", ""))
        
        for head in heads:
            subheads = self.db.get_subheads_by_headid(head[0])
            for subhead in subheads:
                data.append(("SUBHEAD", subhead[1], head[1], head[0], subhead[0]))
        
        self.table.setRowCount(len(data))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Type", "Name", "Head", "Head ID", "Subhead ID"])
        
        for row, item in enumerate(data):
            for col, value in enumerate(item):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))
        
        self.table.setColumnHidden(3, True)
        self.table.setColumnHidden(4, True)
        style_table(self.table)

    def select_row(self, row, col):
        self.btn_delete.setEnabled(True)

    def delete_selected(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            return

        item_type = self.table.item(current_row, 0).text()
        name = self.table.item(current_row, 1).text()

        reply = QMessageBox.question(self, "Confirm Delete", 
                                   f"Are you sure you want to delete {item_type}: {name}?",
                                   QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                if item_type == "HEAD":
                    head_id = self.table.item(current_row, 3).text()
                    self.delete_head(head_id)
                else:
                    subhead_id = self.table.item(current_row, 4).text()
                    self.delete_subhead(subhead_id)
                
                self.load_data()
                self.btn_delete.setEnabled(False)
                QMessageBox.information(self, "Success", "Deleted successfully")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to delete: {str(e)}")

    def delete_head(self, head_id):
        subheads = self.db.get_subheads_by_headid(head_id)
        for subhead in subheads:
            self.db.conn.execute("DELETE FROM subheads WHERE id = ?", (subhead[0],))
        
        self.db.conn.execute("DELETE FROM heads WHERE id = ?", (head_id,))
        self.db.conn.commit()

    def delete_subhead(self, subhead_id):
        self.db.conn.execute("DELETE FROM subheads WHERE id = ?", (subhead_id,))
        self.db.conn.commit()
