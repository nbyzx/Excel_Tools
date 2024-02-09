from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QProgressBar


class ProgressBar(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 设置进度条最小值和最大值
        self.setRange(0, 100)
        # 设置初始值为0
        self.setValue(0)
        self.setTextVisible(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedHeight(15)
