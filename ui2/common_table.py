from PySide6.QtWidgets import QHeaderView, QAbstractItemView
from PySide6.QtCore import Qt

def style_table(table):
    header = table.horizontalHeader()
    header.setSectionResizeMode(QHeaderView.Stretch)
    header.setStyleSheet("""
        QHeaderView::section {
            font-weight: bold;
            padding: 8px;
            background-color: #f8f9fa;
            border: 1px solid #e0e0e0;
            color: #333333;
        }
    """)

    table.verticalHeader().setVisible(False)
    table.setAlternatingRowColors(True)
    table.setSortingEnabled(True)
    table.setEditTriggers(QAbstractItemView.NoEditTriggers)
    table.horizontalHeader().setSortIndicatorShown(True)
    table.setSelectionBehavior(QAbstractItemView.SelectRows)

    table.setStyleSheet("""
        QTableWidget {
            background-color: white;
            alternate-background-color: #f8f9fa;
            gridline-color: #e0e0e0;
            color: #333333;
            border: 1px solid #e0e0e0;
        }
        QTableWidget::item {
            padding: 5px;
            border-bottom: 1px solid #e0e0e0;
        }
        QTableWidget::item:selected {
            background-color: #e3f2fd;
            color: #1976d2;
        }
        QTableWidget::item:hover {
            background-color: #f5f5f5;
        }
    """)

    for r in range(table.rowCount()):
        for c in range(table.columnCount()):
            it = table.item(r, c)
            if it:
                it.setTextAlignment(Qt.AlignCenter)
