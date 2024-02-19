from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QDragEnterEvent
from PyQt6.QtWidgets import QTableWidget, QMenu, QApplication, QMessageBox, QDialog, QTableWidgetItem

from Ui.editheaderdialog import EditHeaderDialog
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
        # 双击表头事件
        self.horizontalHeader().sectionDoubleClicked.connect(self.table_edit_header)

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

        table_operate = menu.addMenu('表格操作')
        table_del = table_operate.addMenu('删除')
        table_add = table_operate.addMenu('插入')
        table_add_row = table_add.addMenu('插入行')
        table_add_col = table_add.addMenu('插入列')
        table_add_row_top = QAction('上方', self)
        table_add_row_top.triggered.connect(lambda: self.table_add(0))
        table_add_row_bottom = QAction('下方', self)
        table_add_row_bottom.triggered.connect(lambda: self.table_add(1))
        table_add_col_left = QAction('左侧', self)
        table_add_col_left.triggered.connect(lambda: self.table_add(2))
        table_add_col_right = QAction('右侧', self)
        table_add_col_right.triggered.connect(lambda: self.table_add(3))
        table_add_row.addAction(table_add_row_top)
        table_add_row.addAction(table_add_row_bottom)
        table_add_col.addAction(table_add_col_left)
        table_add_col.addAction(table_add_col_right)
        del_row = QAction('删除行', self)
        del_row.triggered.connect(lambda: self.table_del(True))
        del_col = QAction('删除列', self)
        del_col.triggered.connect(lambda: self.table_del(False))
        table_del.addAction(del_row)
        table_del.addAction(del_col)
        table_operate.addMenu(table_del)

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

    def table_edit_header(self, index):
        table = self.parent.select_table
        dialog = EditHeaderDialog(self)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            new_header_text = dialog.getText()

            # 执行表头修改操作
            item = QTableWidgetItem(new_header_text)
            table.setHorizontalHeaderItem(index, item)

    def table_add(self, types: int):
        table = self.parent.select_table
        rows = set(item.row() for item in table.selectedItems())
        cols = set(item.column() for item in table.selectedItems())

        if types == 0:
            row_index = next(iter(rows), None)
            if row_index is not None and row_index != 0:
                row_index -= 1
            table.insertRow(row_index)
        elif types == 1:
            table.insertRow(max(rows) + 1 if rows else 0)
        elif types == 2:
            table.insertColumn(next(iter(cols), None))
        elif types == 3:
            table.insertColumn(max(cols) + 1 if cols else 0)

    def table_del(self, types: bool):
        table = self.parent.select_table
        rows = set(item.row() for item in table.selectedItems())
        cols = set(item.column() for item in table.selectedItems())

        # 根据类型删除行或列
        if types:
            for row_index in sorted(rows, reverse=True):
                table.removeRow(row_index)
        else:
            for col_index in sorted(cols, reverse=True):
                table.removeColumn(col_index)

    def onContextMenuAction(self, row, column, action):
        item = self.item(row, column)
        if item is not None:
            print(f"选择的行：{row}，选择的列：{column}")
            print(f"选择的内容: {item.text()}")
            print(f"选择的菜单: {action}")
