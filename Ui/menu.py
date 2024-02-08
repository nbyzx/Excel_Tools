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

        edit_menu = QMenu("编辑", self)
        self.addMenu(edit_menu)

    def open_file(self):
        file_dialog = QFileDialog()
        file_path = file_dialog.getOpenFileName(self, "打开文件")[0]
        print("打开文件:", file_path)
