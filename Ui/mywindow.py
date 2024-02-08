from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTableWidgetItem
from Ui.menu import MenuBar
from Ui.progress import ProgressBar
from Ui.table import Table


class MyWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Excel工具")

        screen_rect = QApplication.primaryScreen().availableGeometry()

        window_width = screen_rect.width() // 2
        window_height = screen_rect.height() // 2

        window_x = (screen_rect.width() - window_width) // 2
        window_y = (screen_rect.height() - window_height) // 2

        self.setGeometry(window_x, window_y, window_width, window_height)

        self.table = Table(self)
        self.progress = ProgressBar(self)

        layout = QVBoxLayout()
        layout.addWidget(self.table, 1)
        layout.addWidget(self.progress)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        menu_bar = MenuBar(self)
        self.setMenuBar(menu_bar)

        menu_bar.data_count.connect(self.set_rc)
        menu_bar.table_value.connect(self.set_data)

    @pyqtSlot(int, int)
    def set_rc(self, row, column):
        print(row,column)
        self.table.setRowCount(row)
        self.table.setColumnCount(column)
        self.progress.setMaximum(row)

    @pyqtSlot(int, int, str)
    def set_data(self, row, column, value):
        item = QTableWidgetItem()
        item.setText(value)
        self.table.setItem(row, column, item)
        self.progress.setValue(row+1)
