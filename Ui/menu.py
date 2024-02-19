import pandas as pd
from PyQt6.QtCore import QStandardPaths
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenuBar, QMenu, QFileDialog, QMessageBox, QTableWidgetItem

from Utils.openfile import OpenFile


class MenuBar(QMenuBar):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.file_menu = QMenu("文件", self)
        self.addMenu(self.file_menu)
        self.data_menu = QMenu("数据", self)
        self.addMenu(self.data_menu)

        open_file_action = QAction("打开", self)
        open_file_action.triggered.connect(self.open_file)
        self.file_menu.addAction(open_file_action)
        save_as_file_action = QAction("另存为...", self)
        save_as_file_action.triggered.connect(self.save_as_file)
        self.file_menu.addAction(save_as_file_action)

        self.data_compare_action = QAction("数据比对", self)
        self.data_compare_action.setCheckable(True)
        self.data_compare_action.triggered.connect(self.data_compare)
        self.data_menu.addAction(self.data_compare_action)

        self.data_sum_action = QAction("数据合计", self)
        self.data_sum_action.triggered.connect(self.data_sum)
        self.data_menu.addAction(self.data_sum_action)

    def data_sum(self):
        table = self.parent.select_table
        rows = table.rowCount()
        cols = table.columnCount()
        table.insertColumn(cols)
        table.insertRow(rows)
        item = QTableWidgetItem('合计')
        table.setHorizontalHeaderItem(cols, item)
        table.setVerticalHeaderItem(rows, item)
        total_sum = 0.0
        for row in range(rows):
            total = 0.0
            for col in range(cols):
                number = table.item(row, col)
                if number is not None and number.text().isdigit():
                    total = self.is_decimal(table.item(rows, col), float(number.text()))
                    rows_item = QTableWidgetItem(str(total))
                    table.setItem(rows, col, rows_item)
                    total = self.is_decimal(table.item(row, cols), float(number.text()))
                    cols_item = QTableWidgetItem(str(total))
                    table.setItem(row, cols, cols_item)
            total_sum += total
        item = QTableWidgetItem(str(self.is_decimal_zero(total_sum)))
        table.setItem(rows, cols, item)

    def is_decimal(self, total, number):
        number_sum = 0
        if total is not None:
            number_sum = float(total.text())
        number_sum += number
        return self.is_decimal_zero(number_sum)

    def is_decimal_zero(self, number):
        if number - int(number) == 0:
            return int(number)
        else:
            return number

    def open_file(self):
        file_dialog = QFileDialog()
        # 设置文件对话框为打开文件模式
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        # 设置过滤器
        file_dialog.setNameFilter("Excel文件 (*.xlsx *.xls)")
        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            file_path = file_dialog.selectedFiles()[0]
            if file_path:
                # 创建线程对象
                open_file_thread = OpenFile(self, file_path)
                # 绑定总行列信号槽
                open_file_thread.data_count.connect(self.parent.interface.set_rc)
                # 绑定数据信号槽
                open_file_thread.table_value.connect(self.parent.interface.set_data)
                # 绑定表头标题信号槽
                open_file_thread.table_title.connect(self.parent.interface.set_table_title)
                open_file_thread.start()

    def save_as_file(self):
        # 获取系统桌面路径
        desktop_path = QStandardPaths.standardLocations(QStandardPaths.StandardLocation.DesktopLocation)[0]
        save_path = QFileDialog.getSaveFileName(self, "另存为", desktop_path, "Excel Files (*.xlsx)")[0]
        if save_path:
            # 提取QTableWidget的数据到二维列表
            data = []
            self.parent.progress.setValue(0)
            self.parent.progress.setMaximum(self.parent.select_table.rowCount())
            for row in range(self.parent.select_table.rowCount()):
                row_data = []
                for column in range(self.parent.select_table.columnCount()):
                    item = self.parent.select_table.item(row, column)
                    if item is not None:
                        row_data.append(item.text())
                    else:
                        row_data.append('')
                self.parent.progress.setValue(row + 1)
                data.append(row_data)

            # 将二维列表转换为DataFrame
            df = pd.DataFrame(data)

            # 将DataFrame保存为Excel文件
            df.to_excel(save_path, index=False)
            # 创建一个信息框
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setWindowTitle("保存完成")
            msg_box.setText("文件已保存！")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()

    def data_compare(self):
        if self.parent.table_compare.isVisible():
            self.parent.table_compare.hide()
        else:
            self.parent.table_compare.show()
        self.parent.table_compare.clear()
        self.parent.table_compare.setRowCount(1)
        self.parent.table_compare.setColumnCount(1)
        self.parent.table_compare.setStyleSheet("QTableWidget { border: 1px solid Gainsboro; }")
