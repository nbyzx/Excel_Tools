from PyQt6.QtWidgets import QApplication
from Ui.mywindow import MyWindow

if __name__ == '__main__':
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()
