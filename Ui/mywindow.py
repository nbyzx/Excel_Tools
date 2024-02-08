from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from Ui.menu import MenuBar
from Ui.table import Table


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Excel工具")

        screen_rect = QApplication.primaryScreen().availableGeometry()

        window_width = screen_rect.width() // 2
        window_height = screen_rect.height() // 2

        window_x = (screen_rect.width() - window_width) // 2
        window_y = (screen_rect.height() - window_height) // 2

        self.setGeometry(window_x, window_y, window_width, window_height)

        self.table = Table(self)

        layout = QVBoxLayout()
        layout.addWidget(self.table)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        menu_bar = MenuBar(self)
        self.setMenuBar(menu_bar)
