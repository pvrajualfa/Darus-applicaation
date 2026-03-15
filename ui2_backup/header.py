from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt

class PageHeader(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedHeight(45)
        self.setStyleSheet("""
            background:#2F80ED;
            color:white;
            font-size:20px;
            font-weight:bold;
            padding:8px;
        """)
