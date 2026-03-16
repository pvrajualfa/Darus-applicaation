from PySide6.QtWidgets import QLabel, QHBoxLayout, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
import os

class PageHeader(QWidget):
    def __init__(self, text, show_background=True, use_header_image=False):
        super().__init__()
        self.setFixedHeight(55)
        
        # Create layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Use header image instead of text
        if use_header_image:
            header_label = QLabel()
            # Get the correct path to header.png
            current_dir = os.path.dirname(os.path.abspath(__file__))
            header_path = os.path.join(current_dir, "..", "icons", "header.png")
            header_pixmap = QPixmap(header_path)
            if not header_pixmap.isNull():
                # Get available width and scale image to fill header area
                available_width = 1200 - 40  # Account for margins
                header_pixmap = header_pixmap.scaled(available_width, 55, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
                header_label.setPixmap(header_pixmap)
                header_label.setAlignment(Qt.AlignCenter)
                
                # Print optimal size for PNG creation
                print(f"Optimal header PNG size: {available_width}x55 pixels")
                print(f"Current image size: {header_pixmap.width()}x{header_pixmap.height()} pixels")
                
            layout.addWidget(header_label)
        else:
            # Add text
            text_label = QLabel(text)
            if show_background:
                text_label.setStyleSheet("""
                    background:#38b6ff;
                    color:white;
                    font-size:20px;
                    font-weight:bold;
                    padding:5px 15px;
                    border-radius:12px;
                """)
                text_label.setAlignment(Qt.AlignCenter) # Center align when background is shown
            else:
                text_label.setStyleSheet("""
                    background:#2F80ED;
                    color:white;
                    font-size:20px;
                    font-weight:bold;
                    padding:5px 15px;
                """)
                text_label.setAlignment(Qt.AlignCenter) # Center align when no background
                
            layout.addStretch()
            layout.addWidget(text_label)
            layout.addStretch()
