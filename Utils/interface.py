from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem


class Interface:
    def __init__(self, parent=None):
        self.parent = parent

    def set_rc(self, row: int, col: int):
        selected_table = self.parent.select_table
        if selected_table and isinstance(selected_table, QTableWidget):
            table = selected_table
            table.setRowCount(row)
            table.setColumnCount(col)
            # 设置进度条最大值，因索引从0开始故-1
            self.parent.progress.setMaximum(row - 1)

    def set_data(self, row: int, col: int, value: str):
        selected_table = self.parent.select_table
        red_color = QColor(255, 255, 255)
        if selected_table and isinstance(selected_table, QTableWidget):
            table = selected_table
            item = QTableWidgetItem()
            item.setText(value)
            if self.parent.menu_bar.data_compare_action.isChecked():
                table_to_check = self.parent.table_compare if selected_table == self.parent.table else self.parent.table
                if table_to_check.rowCount() > row and table_to_check.columnCount() > col:
                    item_compare = table_to_check.item(row, col)
                    if item_compare:
                        if item_compare.text() != value:
                            red_color = QColor(255, 0, 0)
                        item_compare.setBackground(red_color)
                else:
                    red_color = QColor(255, 0, 0)
            item.setBackground(red_color)
            table.setItem(row, col, item)
            self.parent.progress.setValue(row)

    def set_table_title(self, title_list: list):
        selected_table = self.parent.select_table
        if selected_table and isinstance(selected_table, QTableWidget):
            table = selected_table
            table.setHorizontalHeaderLabels(title_list)

    def set_table_color(self):
        # 修改边框颜色为灰色
        self.parent.select_table.setStyleSheet("QTableWidget { border: 1px solid Gray; }")
        if self.parent.select_table is self.parent.table:
            # 修改边框颜色为浅灰色
            self.parent.table_compare.setStyleSheet("QTableWidget { border: 1px solid Gainsboro; }")
        else:
            # 修改边框颜色为浅灰色
            self.parent.table.setStyleSheet("QTableWidget { border: 1px solid Gainsboro; }")
