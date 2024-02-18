from PyQt6.QtCore import Qt, QStandardPaths
from PyQt6.QtGui import QAction, QIcon, QPixmap, QPainter
from PyQt6.QtWidgets import QToolBar, QFileDialog, QTableWidget, QTableWidgetItem, QMessageBox, QMenu, QToolButton


class ToolBar(QToolBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setMinimumSize(24, 24)
        self.open_file_button = QAction(QIcon('./img/toolbar/open_file.png'), '打开文件', self)
        self.as_save_button = QAction(QIcon('./img/toolbar/as_save.png'), "另存为", self)
        self.sort_button = QAction(QIcon('./img/toolbar/sort.png'), "排序", self)
        self.to_png_button = QToolButton()
        self.to_png_button.setToolTip('导出PNG')  # 设置提示文字
        self.to_png_button.setIcon(QIcon('./img/toolbar/to_png.png'))
        self.to_png_button.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)  # 设置下拉菜单模式为MenuButtonPopup
        self.to_png_menu = QMenu()  # 创建下拉菜单
        self.to_png_button_no_header = QAction("不带表头", self)
        self.to_png_button_no_vheader = QAction("不带行表头", self)
        self.to_png_menu.addAction(self.to_png_button_no_header)
        self.to_png_menu.addAction(self.to_png_button_no_vheader)
        self.left_justifying_button = QAction(QIcon('./img/toolbar/left_justifying.png'), "左对齐", self)
        self.horizontally_button = QAction(QIcon('./img/toolbar/horizontally.png'), "水平居中", self)
        self.right_justifying_button = QAction(QIcon('./img/toolbar/right_justifying.png'), "右对齐", self)
        self.init_ui()

    def init_ui(self):
        self.open_file_button.triggered.connect(self.parent.menu_bar.open_file)
        self.addAction(self.open_file_button)
        self.as_save_button.triggered.connect(self.parent.menu_bar.save_as_file)
        self.addAction(self.as_save_button)
        self.to_png_button.setMenu(self.to_png_menu)  # 设置下拉菜单
        self.to_png_button.clicked.connect(lambda: self.to_png(0))
        self.to_png_button_no_header.triggered.connect(lambda: self.to_png(1))
        self.to_png_button_no_vheader.triggered.connect(lambda: self.to_png(2))
        self.addWidget(self.to_png_button)
        self.addSeparator()  # 添加分隔栏
        self.sort_button.setCheckable(True)  # 设置为可选中
        self.sort_button.triggered.connect(self.sort)
        self.addAction(self.sort_button)
        self.left_justifying_button.triggered.connect(
            lambda: self.text_align(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter))
        self.horizontally_button.triggered.connect(lambda: self.text_align(Qt.AlignmentFlag.AlignCenter))
        self.right_justifying_button.triggered.connect(
            lambda: self.text_align(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter))
        self.addAction(self.left_justifying_button)
        self.addAction(self.horizontally_button)
        self.addAction(self.right_justifying_button)

    def text_align(self, types: Qt.AlignmentFlag):
        table = self.parent.select_table
        # 获取选中的行和列
        selected_items = table.selectedItems()
        for selected_item in selected_items:
            selected_item.setTextAlignment(types)

    def sort(self):
        table = self.parent.select_table
        sort = not table.isSortingEnabled()
        # 设置表头可点击排序
        table.horizontalHeader().setSectionsClickable(sort)
        # 设置排序指示器
        table.setSortingEnabled(sort)

    def to_png(self, header):
        table = self.parent.select_table
        # 获取选中的行和列
        selected_items = table.selectedItems()
        selected_rows = set()
        selected_cols = set()
        table_width = table.verticalHeader().width()
        table_height = table.horizontalHeader().height()
        for item in selected_items:
            selected_rows.add(item.row())
            selected_cols.add(item.column())
        # 创建一个新的QTableWidget，用于保存选中的行和列
        new_table_widget = QTableWidget(len(selected_rows), len(selected_cols))
        if header == 1:
            new_table_widget.horizontalHeader().setVisible(False)
            new_table_widget.verticalHeader().setVisible(False)
            table_width = 0
            table_height = 0
        elif header == 2:
            new_table_widget.verticalHeader().setVisible(False)
            table_width = 0
        for col in selected_cols:
            table_width += table.columnWidth(col)
            title = table.horizontalHeaderItem(col).text()
            new_table_widget.setHorizontalHeaderItem(col - min(selected_cols), QTableWidgetItem(title))
            new_table_widget.setColumnWidth(col - min(selected_cols), table.columnWidth(col))
        for row in selected_rows:
            table_height += table.rowHeight(row)
            new_table_widget.setRowHeight(row - min(selected_rows), table.rowHeight(row))
        new_table_widget.setMinimumSize(table_width, table_height)
        new_table_widget.viewport().setMinimumSize(table_width, table_height)
        # 复制选中的行和列数据到新的QTableWidget
        for item in selected_items:
            row = item.row() - min(selected_rows)
            col = item.column() - min(selected_cols)
            new_item = QTableWidgetItem(item.text())
            new_table_widget.setItem(row, col, new_item)

        # 创建QPixmap对象，并设置大小为QTableWidget的尺寸
        pixmap = QPixmap(table_width, table_height)
        pixmap.fill(Qt.GlobalColor.black)  # 设置背景色

        # 创建QPainter对象，并将QPixmap作为绘制设备
        painter = QPainter(pixmap)

        # 设置绘制区域，只绘制新的QTableWidget
        painter.setClipRect(new_table_widget.viewport().rect())

        # 将QTableWidget绘制到QPixmap上
        new_table_widget.render(painter)

        # 结束绘制
        painter.end()

        # 获取系统桌面路径
        desktop_path = QStandardPaths.standardLocations(QStandardPaths.StandardLocation.DesktopLocation)[0]
        save_path = QFileDialog.getSaveFileName(self, "另存为", desktop_path, "PNG文件 (*.png)")[0]
        if save_path:
            # 保存QPixmap为图片文件
            pixmap.save(save_path)  # 图片保存路径及文件名
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setWindowTitle("保存完成")
            msg_box.setText("图片已保存！")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
