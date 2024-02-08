from PyQt6.QtCore import pyqtSlot, pyqtSignal
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenuBar, QMenu, QFileDialog

from Utils.openfile import OpenFile


class MenuBar(QMenuBar):
    data_count = pyqtSignal(int, int)
    table_value = pyqtSignal(int, int, str)

    def __init__(self, parent=None):
        super().__init__(parent)

        file_menu = QMenu("文件", self)
        self.addMenu(file_menu)

        open_action = QAction("打开", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        self.open_file_action = OpenFile(self)  # 创建线程对象

    def open_file(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)  # 设置文件对话框为打开文件模式
        file_dialog.setNameFilter("Excel文件 (*.xlsx *.xls)")  # 设置过滤器
        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            file_path = file_dialog.selectedFiles()[0]
            if file_path:
                open_file_action = OpenFile(self, file_path)  # 创建线程对象
                open_file_action.data_count.connect(self.set_rc)
                open_file_action.table_value.connect(self.set_data)
                open_file_action.start()

    @pyqtSlot(int, int)
    def set_rc(self, row, col):
        self.data_count.emit(row, col)

    @pyqtSlot(int, int, str)
    def set_data(self, row: int, col: int, value: str):
        self.table_value.emit(row, col, value)
