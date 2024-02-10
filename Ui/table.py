from PyQt6.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt6.QtGui import QAction, QDragEnterEvent
from PyQt6.QtWidgets import QTableWidget, QMenu

from Utils.openfile import OpenFile


class Table(QTableWidget):
    data_count = pyqtSignal(int, int)
    table_title = pyqtSignal(list)
    table_value = pyqtSignal(int, int, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)  # 允许拖动
        self.setColumnCount(1)
        self.setRowCount(1)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():  # 判断是否包含URL
            event.acceptProposedAction()  # 接受拖放事件

    def dragMoveEvent(self, event: QDragEnterEvent):
        event.acceptProposedAction()  # 接受拖放事件

    def dropEvent(self, event):
        # 获取拖拽的文件路径
        file_urls = event.mimeData().urls()
        for file_url in file_urls:
            file_path = file_url.toLocalFile()  # 将URL转换为本地文件路径
            if file_path:
                # 设置焦点到拖放的表格
                self.setFocus()
                # 创建线程对象
                open_file_action = OpenFile(self, file_path)
                # 绑定总行列信号槽
                open_file_action.data_count.connect(self.set_rc)
                # 绑定数据信号槽
                open_file_action.table_value.connect(self.set_data)
                # 绑定表头标题信号槽
                open_file_action.table_title.connect(self.set_table_title)
                open_file_action.start()

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

    @pyqtSlot(int, int)
    def set_rc(self, row, col):
        self.data_count.emit(row, col)

    @pyqtSlot(int, int, str)
    def set_data(self, row: int, col: int, value: str):
        self.table_value.emit(row, col, value)

    @pyqtSlot(list)
    def set_table_title(self, title_list):
        self.table_title.emit(title_list)
