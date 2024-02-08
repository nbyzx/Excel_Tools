from PyQt6.QtCore import QThread, pyqtSignal
import pandas as pd
from PyQt6.QtWidgets import QTableWidgetItem


class OpenFile(QThread):
    data_count = pyqtSignal(int, int)
    progress = pyqtSignal(int)
    table_value = pyqtSignal(int, int, str)

    def __init__(self, parent=None, file_path=None):
        super().__init__(parent)
        self.file_path = file_path

    def run(self):
        dataframe = pd.read_excel(self.file_path)  # 读取 Excel 文件
        print(dataframe)
        num_rows, num_columns = dataframe.shape
        print(num_rows, num_columns)
        self.data_count.emit(num_rows, num_columns)
        for i in range(dataframe.shape[0]):
            for j in range(dataframe.shape[1]):
                self.table_value.emit(i, j, str(dataframe.iloc[i, j]))
