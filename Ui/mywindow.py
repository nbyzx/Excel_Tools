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
        self.titles = []
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
        menu_bar.table_title.connect(self.set_table_title)

    @pyqtSlot(int, int)
    def set_rc(self, row, column):
        self.table.setRowCount(row)
        self.table.setColumnCount(column)
        self.progress.setMaximum(row-1)     # 设置进度条最大值，因索引从0开始故-1

    @pyqtSlot(int, int, str)
    def set_data(self, row, column, value):
        item = QTableWidgetItem()
        item.setText(value)
        self.table.setItem(row, column, item)
        self.progress.setValue(row)

    @pyqtSlot(list)
    def set_table_title(self, title_list):
        self.table.setHorizontalHeaderLabels(title_list)
