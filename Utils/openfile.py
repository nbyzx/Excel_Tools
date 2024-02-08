from PyQt6.QtCore import QThread, pyqtSignal
import pandas as pd
from PyQt6.QtWidgets import QTableWidgetItem


class OpenFile(QThread):
    data_count = pyqtSignal(int, int)
    table_title = pyqtSignal(list)
    table_value = pyqtSignal(int, int, str)

    def __init__(self, parent=None, file_path=None):
        super().__init__(parent)
        self.file_path = file_path

    def run(self):
        dataframe = pd.read_excel(self.file_path, header=None)  # 读取 Excel 文件
        num_rows, num_columns = dataframe.shape
        self.data_count.emit(num_rows-1, num_columns)       # 发送行数（-1表示减去标题行）和列数信号
        titles = []
        for i in range(dataframe.shape[1]):
            value = str(dataframe.iloc[0, i])
            if value == 'nan':
                value = ''
            titles.append(value)
        self.table_title.emit(titles)
        for i in range(dataframe.shape[0]-1):       # 遍历表格行（dataframe.shape[0]-1表示减去标题行）
            for j in range(dataframe.shape[1]):
                value = str(dataframe.iloc[i+1, j])
                if value == 'nan':
                    value = ''
                self.table_value.emit(i, j, value)    # str(dataframe.iloc[i+1, j])读取单元格数据并转str类型
