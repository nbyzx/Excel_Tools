from PyQt6.QtCore import pyqtSlot, pyqtSignal
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenuBar, QMenu, QFileDialog

from Utils.openfile import OpenFile


class MenuBar(QMenuBar):
    data_count = pyqtSignal(int, int)
    table_title = pyqtSignal(list)
    table_value = pyqtSignal(int, int, str)
    table_compare = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        file_menu = QMenu("文件", self)
        self.addMenu(file_menu)
        data_menu = QMenu("数据", self)
        self.addMenu(data_menu)

        open_file_action = QAction("打开", self)
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)
        data_compare_action = QAction("比较", self)
        data_compare_action.setCheckable(True)
        data_compare_action.triggered.connect(self.data_compare)
        data_menu.addAction(data_compare_action)

        # 创建打开线程对象
        self.open_file_action = OpenFile(self)

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
                open_file_action = OpenFile(self, file_path)
                # 绑定总行列信号槽
                open_file_action.data_count.connect(self.set_rc)
                # 绑定数据信号槽
                open_file_action.table_value.connect(self.set_data)
                # 绑定表头标题信号槽
                open_file_action.table_title.connect(self.set_table_title)
                open_file_action.start()

    def data_compare(self):
        self.table_compare.emit()

    @pyqtSlot(int, int)
    def set_rc(self, row, col):
        self.data_count.emit(row, col)

    @pyqtSlot(int, int, str)
    def set_data(self, row: int, col: int, value: str):
        self.table_value.emit(row, col, value)

    @pyqtSlot(list)
    def set_table_title(self, title_list):
        self.table_title.emit(title_list)
