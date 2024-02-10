from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTableWidgetItem, QHBoxLayout, QTableWidget
from Ui.menu import MenuBar
from Ui.progress import ProgressBar
from Ui.table import Table


class MyWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Excel工具")

        screen_rect = QApplication.primaryScreen().availableGeometry()

        window_width = screen_rect.width() // 3 * 2
        window_height = screen_rect.height() // 3 * 2

        window_x = (screen_rect.width() - window_width) // 2
        window_y = (screen_rect.height() - window_height) // 2

        self.setGeometry(window_x, window_y, window_width, window_height)

        self.table = Table(self)
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
        self.table.data_count.connect(self.set_rc)
        self.table.table_value.connect(self.set_data)
        self.table.table_title.connect(self.set_table_title)
        self.table_compare.data_count.connect(self.set_rc)
        self.table_compare.table_value.connect(self.set_data)
        self.table_compare.table_title.connect(self.set_table_title)
        self.menu_bar.data_count.connect(self.set_rc)
        self.menu_bar.table_value.connect(self.set_data)
        self.menu_bar.table_title.connect(self.set_table_title)
        self.menu_bar.table_compare.connect(self.table_compare_show)

    @pyqtSlot()
    def table_compare_show(self):
        if self.table_compare.isVisible():
            self.table_compare.hide()
        else:
            self.table_compare.show()
        self.table_compare.clear()
        self.table_compare.setRowCount(1)
        self.table_compare.setColumnCount(1)

    @pyqtSlot(int, int)
    def set_rc(self, row, column):
        selected_table = self.centralWidget().focusWidget()
        if selected_table and isinstance(selected_table, QTableWidget):
            table = selected_table
            table.setRowCount(row)
            table.setColumnCount(column)
            # 设置进度条最大值，因索引从0开始故-1
            self.progress.setMaximum(row - 1)

    @pyqtSlot(int, int, str)
    def set_data(self, row, column, value):
        selected_table = self.centralWidget().focusWidget()
        red_color = QColor(255, 255, 255)
        if selected_table and isinstance(selected_table, QTableWidget):
            table = selected_table
            item = QTableWidgetItem()
            item.setText(value)
            if self.menu_bar.data_compare_action.isChecked():
                table_to_check = self.table_compare if selected_table == self.table else self.table
                if table_to_check.rowCount() > row and table_to_check.columnCount() > column:
                    item_compare = table_to_check.item(row, column)
                    if item_compare:
                        if item_compare.text() != value:
                            red_color = QColor(255, 0, 0)
                        item_compare.setBackground(red_color)
                else:
                    red_color = QColor(255, 0, 0)
            item.setBackground(red_color)
            table.setItem(row, column, item)
            self.progress.setValue(row)

    @pyqtSlot(list)
    def set_table_title(self, title_list):
        selected_table = self.centralWidget().focusWidget()
        if selected_table and isinstance(selected_table, QTableWidget):
            table = selected_table
            table.setHorizontalHeaderLabels(title_list)
