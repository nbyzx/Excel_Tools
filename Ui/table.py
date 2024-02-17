from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QDragEnterEvent
from PyQt6.QtWidgets import QTableWidget, QMenu, QApplication

from Utils.openfile import OpenFile


class Table(QTableWidget):
    thread_lock = True

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setAcceptDrops(True)
        # self.setDragEnabled(True)  # 允许拖动
        self.setColumnCount(1)
        self.setRowCount(1)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def mousePressEvent(self, event):
        if self.thread_lock:
            self.parent.select_table = QApplication.focusWidget()
            sort = self.parent.select_table.isSortingEnabled()
            self.parent.toolbar.sort_button.setChecked(sort)
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

    def show_context_menu(self, pos):
        row = self.currentRow()
        column = self.currentColumn()

        # 创建右键菜单
        menu = QMenu(self)

        # 添加数据提取菜单
        data_extraction_menu = menu.addMenu("数据提取")

        # 添加动作
        get_age = QAction("取选中列年龄", self)
        get_age.triggered.connect(self.parent.interface.get_age)
        data_extraction_menu.addAction(get_age)

        get_gender = QAction("取选中列性别", self)
        get_gender.triggered.connect(self.parent.interface.get_gender)
        data_extraction_menu.addAction(get_gender)

        get_phone_number = QAction("取选中列手机号", self)
        get_phone_number.triggered.connect(lambda: self.parent.interface.get_number('手机号'))
        data_extraction_menu.addAction(get_phone_number)

        get_identity_number = QAction("取选中列身份证号", self)
        get_identity_number.triggered.connect(lambda: self.parent.interface.get_number('身份证号'))
        data_extraction_menu.addAction(get_identity_number)

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
