from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenuBar, QMenu, QFileDialog


class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        file_menu = QMenu("文件", self)
        self.addMenu(file_menu)

        open_action = QAction("打开", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

    def open_file(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)  # 设置文件对话框为打开文件模式
        file_dialog.setNameFilter("Excel文件 (*.xlsx *.xls)")  # 设置过滤器
        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            file_path = file_dialog.selectedFiles()[0]
            if file_path:
                print("打开文件:", file_path)
