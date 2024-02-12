from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTableWidgetItem, QHBoxLayout, QTableWidget
from Ui.menu import MenuBar
from Ui.progress import ProgressBar
from Ui.table import Table
from Utils.interface import Interface


class MyWindow(QMainWindow):
    select_table: QTableWidget = None

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Excel工具")

        screen_rect = QApplication.primaryScreen().availableGeometry()

        window_width = screen_rect.width() // 3 * 2
        window_height = screen_rect.height() // 3 * 2

        window_x = (screen_rect.width() - window_width) // 2
        window_y = (screen_rect.height() - window_height) // 2

        self.setGeometry(window_x, window_y, window_width, window_height)
        self.interface = Interface(self)
        self.table = Table(self)
        self.select_table = self.table

        self.table_compare = Table(self)
        self.table_compare.hide()
        self.progress = ProgressBar(self)

        layout = QVBoxLayout()
        data_layout = QHBoxLayout()
        data_layout.addWidget(self.table, 1)
        data_layout.addWidget(self.table_compare, 1)
        layout.addLayout(data_layout)
        layout.addWidget(self.progress)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)
