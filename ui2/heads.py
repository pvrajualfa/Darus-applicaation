from ui2.common_table import style_table
from ui2.common_form import style_label, style_button, style_groupbox, style_lineedit, style_combo
from PySide6.QtWidgets import *
from ui2.database import Database
from ui2.header import PageHeader
from PySide6.QtCore import Qt, Signal


class HeadPage(QWidget):
    head_added = Signal()
    subhead_added = Signal()

    def __init__(self):
        super().__init__()
        self.db = Database()
        self.entry_mode = "HEAD"
        self.selected_section = "ALL"  # Track selected section: "ALL", "HEAD", "SUBHEAD"

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
        
        # Store reference for visual feedback
        self.head_group = head_group
        
        # Make head section clickable
        head_widget.setCursor(Qt.PointingHandCursor)
        head_widget.mousePressEvent = lambda e: self.select_section("HEAD")
        
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
        
        # Store reference for visual feedback
        self.sub_group = sub_group
        
        # Make subhead section clickable
        subhead_widget.setCursor(Qt.PointingHandCursor)
        subhead_widget.mousePressEvent = lambda e: self.select_section("SUBHEAD")
        
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
        
        # Make table clickable to reset filter
        self.table.mousePressEvent = self.table_mouse_press
        layout.addWidget(self.table)
        
        # ================= SELECTION INFO =================
        selection_layout = QHBoxLayout()
        self.selection_label = QLabel("Showing: All Data")
        self.selection_label.setStyleSheet("color: #666; font-size: 12px; padding: 5px;")
        
        self.btn_show_all = QPushButton("Show All")
        self.btn_show_all.setFixedWidth(80)
        self.btn_show_all.setStyleSheet("""
            QPushButton {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        self.btn_show_all.clicked.connect(lambda: self.select_section("ALL"))
        
        selection_layout.addWidget(self.selection_label)
        selection_layout.addStretch()
        selection_layout.addWidget(self.btn_show_all)
        layout.addLayout(selection_layout)

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
        
        # Add type filtering connections
        self.head_type.currentTextChanged.connect(self.filter_by_type)
        self.sub_type.currentTextChanged.connect(self.filter_by_type)
        
        # Add head selection filtering for subheads
        self.sub_head_combo.currentTextChanged.connect(self.filter_by_head)

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
        
        # Get current type filter from either dropdown (they should be in sync)
        current_type = self.head_type.currentText()
        
        # Get selected head for subhead filtering
        selected_head_name = self.sub_head_combo.currentText()
        selected_head_id = None
        
        # Get head ID if a specific head is selected (not "Select Head")
        if selected_head_name != "Select Head":
            current_index = self.sub_head_combo.currentIndex()
            if current_index > 0:  # Skip "Select Head" at index 0
                selected_head_id = self.sub_head_combo.itemData(current_index)
        
        if self.selected_section == "ALL":
            heads = self.db.get_all_heads()
            for head in heads:
                # Filter by type (type is at index 1: id, type, name)
                if head[1] == current_type:
                    data.append(("HEAD", head[2], head[0], "", ""))
            
            for head in heads:
                if head[1] == current_type:  # Filter by type
                    # Additional head filter for subheads
                    if selected_head_id is None or head[0] == selected_head_id:
                        subheads = self.db.get_subheads_by_headid(head[0])
                        for subhead in subheads:
                            data.append(("SUBHEAD", subhead[1], head[2], head[0], subhead[0]))
                    
        elif self.selected_section == "HEAD":
            heads = self.db.get_all_heads()
            for head in heads:
                # Filter by type (type is at index 1: id, type, name)
                if head[1] == current_type:
                    data.append(("HEAD", head[2], head[0], "", ""))
                
        elif self.selected_section == "SUBHEAD":
            heads = self.db.get_all_heads()
            for head in heads:
                if head[1] == current_type:  # Filter by type
                    # Additional head filter for subheads
                    if selected_head_id is None or head[0] == selected_head_id:
                        subheads = self.db.get_subheads_by_headid(head[0])
                        for subhead in subheads:
                            data.append(("SUBHEAD", subhead[1], head[2], head[0], subhead[0]))
        
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
        
    def select_section(self, section):
        """Handle section selection and update table display"""
        self.selected_section = section
        
        # Update selection label with filters
        self.update_selection_label()
        
        # Reload data with filter
        self.load_data()
        
        # Visual feedback - update groupbox styles
        self.update_section_styles()
        
    def filter_by_type(self):
        """Handle type change and update table display"""
        # Reload data when type changes
        self.load_data()
        
        # Update selection label with new type
        self.update_selection_label()
        
    def filter_by_head(self):
        """Handle head selection change and update table display"""
        # Reload data when head selection changes
        self.load_data()
        
        # Update selection label with new head selection
        self.update_selection_label()
        
    def update_selection_label(self):
        """Update selection label based on current filters"""
        current_type = self.head_type.currentText()
        selected_head_name = self.sub_head_combo.currentText()
        
        if self.selected_section == "ALL":
            if selected_head_name == "Select Head":
                self.selection_label.setText(f"Showing: All {current_type} Data")
            else:
                self.selection_label.setText(f"Showing: All {current_type} Data for '{selected_head_name}'")
        elif self.selected_section == "HEAD":
            self.selection_label.setText(f"Showing: {current_type} Heads Only")
        elif self.selected_section == "SUBHEAD":
            if selected_head_name == "Select Head":
                self.selection_label.setText(f"Showing: {current_type} Subheads Only")
            else:
                self.selection_label.setText(f"Showing: {current_type} Subheads for '{selected_head_name}'")
        
    def update_section_styles(self):
        """Update visual styles based on selected section"""
        # Reset both groupboxes to default style
        self.head_group.setStyleSheet("")
        self.sub_group.setStyleSheet("")
        style_groupbox(self.head_group)
        style_groupbox(self.sub_group)
        
        # Highlight selected section
        if self.selected_section == "HEAD":
            self.head_group.setStyleSheet("""
                QGroupBox {
                    border: 2px solid #4CAF50;
                    border-radius: 8px;
                    margin-top: 10px;
                    padding-top: 10px;
                    background-color: #f0f8f0;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                    color: #4CAF50;
                    font-weight: bold;
                }
            """)
        elif self.selected_section == "SUBHEAD":
            self.sub_group.setStyleSheet("""
                QGroupBox {
                    border: 2px solid #2196F3;
                    border-radius: 8px;
                    margin-top: 10px;
                    padding-top: 10px;
                    background-color: #f0f8ff;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                    color: #2196F3;
                    font-weight: bold;
                }
            """)
    
    def table_mouse_press(self, event):
        """Handle mouse press on table to reset filter"""
        if event.button() == Qt.LeftButton:
            self.select_section("ALL")
        # Call the original table mouse press event
        QTableWidget.mousePressEvent(self.table, event)
