# mywindow.py
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("窗口类示例")

        self.label = QLabel(self)
        self.label.setText("点击按钮以显示消息")
        self.label.move(50, 50)

        self.button = QPushButton(self)
        self.button.setText("点击我")
        self.button.move(50, 100)
        self.button.clicked.connect(self.button_click)

    def button_click(self):
        self.label.setText("Hello, World!")


if __name__ == '__main__':
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()
