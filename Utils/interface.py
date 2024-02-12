from datetime import datetime
import re

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem


class Interface:
    def __init__(self, parent=None):
        self.parent = parent

    def get_gender(self):
        table = self.parent.select_table
        col = table.currentColumn()
        table.insertColumn(col + 1)
        table.setHorizontalHeaderItem(col + 1, QTableWidgetItem("年龄"))
        row_count = table.rowCount()
        for i in range(row_count):
            item = table.item(i, col)
            if item is not None:
                text = item.text()
                pattern = r'\d{17}[\dXx]'
                match = re.search(pattern, text)
                if match:
                    id_number = match.group()
                    gender_code = int(id_number[-2])
                    if gender_code % 2 == 0:
                        gender = "女性"
                    else:
                        gender = "男性"
                else:
                    gender = ''
                item = QTableWidgetItem()
                item.setText(str(gender))
                table.setItem(i, col + 1, item)


    def get_age(self):
        table = self.parent.select_table
        col = table.currentColumn()
        table.insertColumn(col + 1)
        table.setHorizontalHeaderItem(col + 1, QTableWidgetItem("年龄"))
        row_count = table.rowCount()
        for i in range(row_count):
            item = table.item(i, col)
            if item is not None:
                text = item.text()
                date = self.contains_pattern(text)
                if date:
                    today = datetime.today()
                    age = today.year - date.year
                    # 如果出生月份大于当前月份，或者出生月份等于当前月份但出生日期大于当前日期，则年龄减一
                    if date.month > today.month or (
                            date.month == today.month and date.day > today.day):
                        age -= 1
                else:
                    age = ''
                item = QTableWidgetItem()
                item.setText(str(age))
                table.setItem(i, col + 1, item)

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

    # 判断是否包含年月日内容
    import re
    from datetime import datetime

    def contains_pattern(self, input_text):
        patterns = [
            r'\d{17}[\dXx]',  # 身份证号码的正则表达式
            r'(19|20)\d{2}-([1-9]|0[1-9]|1[0-2])-([1-9]|0[1-9]|[12]\d|3[01])',  # 年月日日期的正则表达式
            r'(19|20)\d{2}'  # 年份的正则表达式
        ]

        for pattern in patterns:
            match = re.search(pattern, input_text)
            if match:
                if re.match(r'\d{17}[\dXx]', match.group()):
                    # 如果匹配到身份证号码，则返回其年月日部分
                    birth_date_str = match.group()[6:14]
                    try:
                        birth_date = datetime.strptime(birth_date_str, '%Y%m%d')
                        return birth_date
                    except ValueError:
                        continue
                elif re.match(r'(19|20)\d{2}-([1-9]|0[1-9]|1[0-2])-([1-9]|0[1-9]|[12]\d|3[01])', match.group()):
                    # 如果匹配到年月日日期，则返回日期对应的时间对象
                    birth_date_str = match.group()
                    try:
                        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d')
                        return birth_date
                    except ValueError:
                        continue
                else:
                    # 否则返回匹配到的年份对应的时间对象
                    birth_year_str = match.group()
                    try:
                        birth_year = datetime.strptime(birth_year_str, '%Y')
                        return birth_year
                    except ValueError:
                        continue
        return False
