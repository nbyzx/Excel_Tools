import threading

from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QAction, QDragEnterEvent, QColor
from PyQt6.QtWidgets import QTableWidget, QMenu, QApplication, QTableWidgetItem

from Utils.openfile import OpenFile


class Table(QTableWidget):
    thread_lock = True

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setAcceptDrops(True)
        self.setDragEnabled(True)  # 允许拖动
        self.setColumnCount(1)
        self.setRowCount(1)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.thread_lock:
            self.parent.select_table = QApplication.focusWidget()
            self.parent.interface.set_table_color()
        super().mousePressEvent(event)

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
                self.parent.select_table = self.parent.centralWidget().focusWidget()
                self.parent.interface.set_table_color()
                # 创建线程对象
                open_file_action = OpenFile(self, file_path)
                # 绑定总行列信号槽
                open_file_action.data_count.connect(self.parent.interface.set_rc)
                # 绑定数据信号槽
                open_file_action.table_value.connect(self.parent.interface.set_data)
                # 绑定表头标题信号槽
                open_file_action.table_title.connect(self.parent.interface.set_table_title)
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
