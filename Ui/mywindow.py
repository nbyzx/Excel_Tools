from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QGuiApplication

from Ui.menu import MenuBar


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Excel工具")

        screen = QGuiApplication.primaryScreen()
        screen_rect = screen.availableGeometry()

        window_width = screen_rect.width() // 2
        window_height = screen_rect.height() // 2

        window_x = (screen_rect.width() - window_width) // 2
        window_y = (screen_rect.height() - window_height) // 2

        self.setGeometry(window_x, window_y, window_width, window_height)

        menu_bar = MenuBar(self)
        self.setMenuBar(menu_bar)
