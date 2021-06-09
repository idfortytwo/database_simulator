from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal

from db.data_types import DataType


class TypeComboBox(QtWidgets.QComboBox):
    def __init__(self, data_types: list[DataType]):
        super().__init__()

        self.data_types_dict = {str(data_type): data_type for data_type in data_types}
        for data_type in data_types:
            self.addItem(str(data_type))


class ClickableLineEdit(QtWidgets.QLineEdit):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        # noinspection PyUnresolvedReferences
        self.clicked.emit()
