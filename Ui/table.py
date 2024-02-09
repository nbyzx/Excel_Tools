from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QTableWidget, QMenu


class Table(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(1)
        self.setRowCount(1)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

    def showContextMenu(self, pos):
        row = self.currentRow()
        column = self.currentColumn()

        # 创建右键菜单
        menu = QMenu(self)

        # 添加动作
        action1 = QAction("Action 1", self)
        action1.triggered.connect(lambda: self.onContextMenuAction(row, column, "Action 1"))
        menu.addAction(action1)

        action2 = QAction("Action 2", self)
        action2.triggered.connect(lambda: self.onContextMenuAction(row, column, "Action 2"))
        menu.addAction(action2)

        # 显示右键菜单
        menu.exec(self.viewport().mapToGlobal(pos))

    def onContextMenuAction(self, row, column, action):
        item = self.item(row, column)
        if item is not None:
            print(f"选择的行：{row}，选择的列：{column}")
            print(f"选择的内容: {item.text()}")
            print(f"选择的菜单: {action}")
