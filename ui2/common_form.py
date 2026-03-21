from PySide6.QtWidgets import QLineEdit, QComboBox, QPushButton, QDateEdit, QLabel, QGroupBox
from PySide6.QtCore import Qt, Signal, QObject
from PySide6.QtGui import QIcon

class DataManager(QObject):
    student_updated = Signal()
    class_updated = Signal()

data_manager = DataManager()

def format_text_for_db(text):
    return text.strip().replace("'", "''")

# Enhanced widgets
class EnhancedLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(34)

class EnhancedComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(34)

class EnhancedDateEdit(QDateEdit):
    def __init__(self, date, parent=None, calendarPopup=False):
        super().__init__(date, parent)
        self.setCalendarPopup(calendarPopup)

# Styling functions
def style_lineedit(widget):
    widget.setMinimumHeight(34)
    widget.setStyleSheet("""
        QLineEdit {
            border:1px solid #d0d0d0;
            border-radius:6px;
            padding-left:6px;
            background:white;
            color: #333333;
        }
        QLineEdit:focus {
            border:2px solid #2F80ED;
        }
    """)

def style_combo(widget):
    widget.setMinimumHeight(34)
    widget.setStyleSheet("""
        QComboBox {
            border:1px solid #d0d0d0;
            border-radius:6px;
            padding-left:6px;
            background:white;
            color: #333333;
            min-height: 34px;
        }
        QComboBox:focus {
            border:2px solid #2F80ED;
        }
        QComboBox QAbstractItemView {
            background-color: white;
            border: 1px solid #d0d0d0;
            selection-background-color: #e3f2fd;
            selection-color: #1976d2;
            color: #333333;
        }
        QComboBox QAbstractItemView::item {
            padding: 5px;
            border: none;
            min-height: 20px;
        }
        QComboBox QAbstractItemView::item:selected {
            background-color: #e3f2fd;
            color: #1976d2;
        }
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left: 1px solid #d0d0d0;
        }
        QComboBox::down-arrow {
            width: 8px;
            height: 8px;
            background-color: #36ABD6;
        }
        QComboBox::down-arrow:hover,
        QComboBox::down-arrow:pressed {
            background-color: #1D4ED8;
        }
    """)

def style_button(btn):
    btn.setMinimumHeight(40)
    btn.setMinimumWidth(160)
    # Explicitly remove any icons
    btn.setIcon(QIcon())
    btn.setText(btn.text().replace("📝", "").replace("📊", "").replace("🎓", "").replace("👨‍🎓", "").replace("📈", "").replace("🏷️", "").strip())
    btn.setStyleSheet("""
        QPushButton {
            background: #00B4DB;
            color: #FFFFFF;
            border: none;
            border-radius: 10px;
            font-weight: bold;
            font-size: 15px;
            font-family: Helvetica;
            padding: 10px 15px;
            margin: 2px 0px;
            text-align: center;
        }
        QPushButton:hover {
            background: #0083B0;
        }
        QPushButton:pressed {
            background: #006A8C;
        }
    """)

def style_dateedit(widget):
    widget.setMinimumHeight(34)
    widget.setMinimumWidth(120)  # Add minimum width to prevent cutoff
    widget.setStyleSheet("""
        QDateEdit {
            border:1px solid #d0d0d0;
            border-radius:6px;
            padding-left:6px;
            background:white;
            color: #333333;
        }
        QDateEdit:focus {
            border:2px solid #2F80ED;
        }
        QDateEdit::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left: 1px solid #d0d0d0;
        }
        QDateEdit::down-arrow {
            width: 8px;
            height: 8px;
            background-color: #36ABD6;
        }
        QDateEdit::down-arrow:hover,
        QDateEdit::down-arrow:pressed {
            background-color: #1D4ED8;
        }
        QCalendarWidget {
            background-color: white;
            color: #333333;
            font-size: 12px;
        }
        QCalendarWidget QAbstractItemView {
            background-color: white;
            color: #333333;
            selection-background-color: #36ABD6;
            selection-color: white;
        }
        QCalendarWidget QToolButton {
            background-color: #f8f9fa;
            color: #333333;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            padding: 4px 8px;
            font-weight: bold;
            min-width: 80px;
        }
        QCalendarWidget QToolButton:hover {
            background-color: #e3f2fd;
            color: #1976d2;
        }
        QCalendarWidget QToolButton::menu-indicator {
            width: 0px;
        }
        QCalendarWidget QSpinBox {
            background-color: white;
            color: #333333;
            border: 1px solid #d0d0d0;
            border-radius: 4px;
            padding: 2px 4px;
        }
        QCalendarWidget QSpinBox::up-button,
        QCalendarWidget QSpinBox::down-button {
            width: 20px;
            background-color: #f8f9fa;
            border-left: 1px solid #d0d0d0;
        }
        QCalendarWidget QSpinBox::up-button:hover,
        QCalendarWidget QSpinBox::down-button:hover {
            background-color: #e3f2fd;
        }
    """)

def style_label(widget):
    widget.setStyleSheet("""
        QLabel {
            font-weight:bold;
            color: #36ABD6;
            font-size: 13px;
            padding: 2px 0px;
        }
    """)

def style_groupbox(box):
    box.setStyleSheet("""
        QGroupBox {
            background:white;
            border:1px solid #e5e7eb;
            border-radius:10px;
            margin-top:10px;
            padding:10px;
            font-weight:bold;
            color: #333333;
        }
        QGroupBox:title {
            subcontrol-origin: margin;
            left:10px;
            padding:0 3px;
            color: #36ABD6;
            font-weight: bold;
        }
    """)

# Data loading functions
def load_students_into_combo(combo, db):
    combo.clear()
    combo.addItem("Select Student", None)
    students = db.get_students()
    for student in students:
        combo.addItem(f"{student[1]} - {student[2]}", student)

def load_heads_into_combo(combo, db, typ=None):
    combo.clear()
    combo.addItem("Select Head", None)
    heads = db.get_heads(typ) if typ else db.get_all_heads()
    for head in heads:
        combo.addItem(head[1], head[0])

def load_subheads_into_combo(combo, db, head_id):
    combo.clear()
    combo.addItem("Select Subhead", None)
    if head_id:
        subheads = db.get_subheads_by_headid(head_id)
        for subhead in subheads:
            combo.addItem(subhead[1], subhead[0])

def load_payment_modes_into_combo(combo):
    combo.clear()
    combo.addItems(["Cash", "Bank", "UPI", "Cheque"])

def load_classes_into_combo(combo):
    combo.clear()
    combo.addItems(["6th", "7th", "8th", "9th", "10th"])
