from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, Signal
from database import Database
from ui.header import PageHeader
from ui.helpers import style_table


class HeadPage(QWidget):

    head_added = Signal()
    subhead_added = Signal()

    def _init_(self):
        super()._init_()

        self.db = Database()
        self.entry_mode = "HEAD"

        layout = QVBoxLayout(self)
        layout.addWidget(PageHeader("Manage Heads"))

# ================= ADD HEAD =================
        head_group = QGroupBox("Add Head")
        head_layout = QFormLayout()

        self.head_type = QComboBox()
        self.head_type.addItems(["Income", "Expense"])

        self.head_name = QLineEdit()

        self.btn_add_head = QPushButton("Add Head")

        head_layout.addRow("Type", self.head_type)
        head_layout.addRow("Head Name", self.head_name)
        head_layout.addRow(self.btn_add_head)

        head_group.setLayout(head_layout)
        layout.addWidget(head_group)

# ================= ADD SUBHEAD =================
        sub_group = QGroupBox("Add Subhead")
        sub_layout = QFormLayout()

        self.sub_type = QComboBox()
        self.sub_type.addItems(["Income", "Expense"])

        self.sub_head_combo = QComboBox()

        self.sub_name = QLineEdit()
        self.sub_name.setPlaceholderText("Select Head")
        self.sub_name.setEnabled(False)

        self.btn_add_sub = QPushButton("Add Subhead")

        sub_layout.addRow("Type", self.sub_type)
        sub_layout.addRow("Head", self.sub_head_combo)
        sub_layout.addRow("Subhead", self.sub_name)
        sub_layout.addRow(self.btn_add_sub)

        sub_group.setLayout(sub_layout)
        layout.addWidget(sub_group)

# ================= TABLE =================
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)

# ================= CONNECT =================
        self.btn_add_head.clicked.connect(self.add_head_master)
        self.btn_add_sub.clicked.connect(self.add_sub_master)

        self.head_type.currentTextChanged.connect(self.set_head_mode)
        self.sub_type.currentTextChanged.connect(self.set_subhead_mode)
        self.sub_head_combo.currentIndexChanged.connect(self.head_selected)

# ================= LOAD =================
        self.load_heads_for_sub()
        self.switch_table_mode()

# ================= MODE =================
    def set_head_mode(self):
        self.entry_mode = "HEAD"
        self.switch_table_mode()

    def set_subhead_mode(self):
        self.entry_mode = "SUBHEAD"
        self.load_heads_for_sub()
        self.switch_table_mode()

# ================= LOAD HEADS =================
    def load_heads_for_sub(self):

        self.sub_head_combo.clear()
        self.sub_head_combo.addItem("Select Head")

        rows = self.db.conn.execute(
            "SELECT name FROM heads WHERE type=?",
            (self.sub_type.currentText(),)
        ).fetchall()

        for r in rows:
            self.sub_head_combo.addItem(r[0])

        if self.entry_mode == "SUBHEAD":
            self.switch_table_mode()

# ================= HEAD SELECT =================
    def head_selected(self):

        head = self.sub_head_combo.currentText()

        if head == "Select Head":
            self.sub_name.setEnabled(False)
            self.sub_name.setPlaceholderText("Select Head")
            self.switch_table_mode()
            return

        self.sub_name.setEnabled(True)
        self.sub_name.setPlaceholderText("Enter Subhead")
        self.switch_table_mode()

# ================= SWITCH TABLE =================
    def switch_table_mode(self):

        if self.entry_mode == "HEAD":
            self.show_heads_table()
            return

        head = self.sub_head_combo.currentText()

        if head == "Select Head":
            self.show_heads_table()
        else:
            self.show_subheads_table()

# ================= ADD HEAD =================
    def add_head_master(self):

        typ = self.head_type.currentText()
        head = self.head_name.text().strip()

        if not head:
            QMessageBox.warning(self, "Error", "Enter Head")
            return

        exists = self.db.conn.execute(
            "SELECT id FROM heads WHERE type=? AND name=?",
            (typ, head)
        ).fetchone()

        if exists:
            QMessageBox.warning(self, "Duplicate",
                                f"'{head}' already exists")
            return

        self.db.add_head(typ, head)
        self.head_added.emit()

        QMessageBox.information(self, "Saved", "Head Added")
        self.head_name.clear()

        self.load_heads_for_sub()
        self.set_head_mode()

# ================= ADD SUBHEAD =================
    def add_sub_master(self):

        typ = self.sub_type.currentText()
        head = self.sub_head_combo.currentText()
        sub = self.sub_name.text().strip()

        if not sub:
            QMessageBox.warning(self, "Error", "Enter Subhead")
            return

        self.db.add_subhead(typ, head, sub)
        self.subhead_added.emit()

        QMessageBox.information(self, "Saved", "Subhead Added")
        self.sub_name.clear()

        self.show_subheads_table()
        self.set_subhead_mode()

# ================= SHOW HEADS =================
    def show_heads_table(self):

        typ = self.head_type.currentText() if self.entry_mode == "HEAD" \
              else self.sub_type.currentText()

        self.table.clear()

        headers = ["Head ID", "Type", "Head Name"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        rows = self.db.conn.execute(
            "SELECT id, type, name FROM heads WHERE type=?",
            (typ,)
        ).fetchall()

        self.table.setRowCount(len(rows))

        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(r, c, item)

        self.table.resizeColumnsToContents()
        style_table(self.table)

# ================= SHOW SUBHEADS =================
    def show_subheads_table(self):

        typ = self.sub_type.currentText()
        head = self.sub_head_combo.currentText()

        self.table.clear()

        headers = ["Subhead ID", "Subhead Name"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        rows = self.db.conn.execute("""
            SELECT s.id, s.name
            FROM subheads s
            JOIN heads h ON s.head_id = h.id
            WHERE h.type=? AND h.name=?
        """, (typ, head)).fetchall()

        self.table.setRowCount(len(rows))

        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(r, c, item)

        self.table.resizeColumnsToContents()
        style_table(self.table)