from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox


class EditHeaderDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("编辑表头")
        self.layout = QVBoxLayout(self)

        self.label = QLabel("请输入新的表头名称:")
        self.layout.addWidget(self.label)

        self.edit = QLineEdit()
        self.layout.addWidget(self.edit)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

    def getText(self):
        return self.edit.text()
