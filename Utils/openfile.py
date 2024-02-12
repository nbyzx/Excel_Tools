import pandas as pd
from PyQt6.QtCore import QThread, pyqtSignal


class OpenFile(QThread):
    data_count = pyqtSignal(int, int)
    table_title = pyqtSignal(list)
    table_value = pyqtSignal(int, int, str)

    def __init__(self, parent=None, file_path: str = None):
        super().__init__(parent)
        self.parent = parent
        self.file_path = file_path

    def run(self):
        if self.parent is self.parent.parent.menu_bar:
            self.parent.menu_bar.file_menu.setEnabled(False)
            self.parent.menu_bar.data_menu.setEnabled(False)
            self.parent.parent.table.setAcceptDrops(False)
            self.parent.parent.table_compare.setAcceptDrops(False)
            self.parent.parent.table.thread_lock = False
            self.parent.parent.table_compare.thread_lock = False
        elif self.parent in [self.parent.parent.table, self.parent.parent.table_compare]:
            self.parent.parent.menu_bar.file_menu.setEnabled(False)
            self.parent.parent.menu_bar.data_menu.setEnabled(False)
            self.parent.parent.table.setAcceptDrops(False)
            self.parent.parent.table_compare.setAcceptDrops(False)
            self.parent.parent.table.thread_lock = False
            self.parent.parent.table_compare.thread_lock = False
        extension = self.file_path.split('.')[-1]
        # 读取 Excel 文件
        if extension == 'xls':
            dataframe = pd.read_excel(self.file_path, header=None, engine='xlrd')
        else:
            dataframe = pd.read_excel(self.file_path, header=None, engine='openpyxl')
        num_rows, num_columns = dataframe.shape
        # 发送行数（-1表示减去标题行）和列数信号
        self.data_count.emit(int(num_rows - 1), int(num_columns))
        titles = []
        for i in range(dataframe.shape[1]):
            value = str(dataframe.iloc[0, i])
            if value == 'nan':
                value = ''
            titles.append(value)
        self.table_title.emit(titles)
        # 遍历表格行（dataframe.shape[0]-1表示减去标题行）
        for i in range(dataframe.shape[0] - 1):
            for j in range(dataframe.shape[1]):
                # str(dataframe.iloc[i+1, j])读取单元格数据并转str类型
                value = str(dataframe.iloc[i + 1, j])
                if value == 'nan':
                    value = ''
                self.table_value.emit(i, j, value)
        if self.parent is self.parent.parent.menu_bar:
            self.parent.menu_bar.file_menu.setEnabled(True)
            self.parent.menu_bar.data_menu.setEnabled(True)
            self.parent.parent.table.setAcceptDrops(True)
            self.parent.parent.table_compare.setAcceptDrops(True)
            self.parent.parent.table.thread_lock = True
            self.parent.parent.table_compare.thread_lock = True
        elif self.parent in [self.parent.parent.table, self.parent.parent.table_compare]:
            self.parent.parent.menu_bar.file_menu.setEnabled(True)
            self.parent.parent.menu_bar.data_menu.setEnabled(True)
            self.parent.parent.table.setAcceptDrops(True)
            self.parent.parent.table_compare.setAcceptDrops(True)
            self.parent.parent.table.thread_lock = True
            self.parent.parent.table_compare.thread_lock = True
