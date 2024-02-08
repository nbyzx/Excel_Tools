from PyQt6.QtWidgets import QTableWidget


class Table(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
