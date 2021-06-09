from PyQt5 import QtWidgets


class ConfirmRemovalMessageBox(QtWidgets.QMessageBox):
    # noinspection PyUnresolvedReferences
    def __init__(self, parent: 'DatabaseWindow', text: str):
        super().__init__(parent)
        self.parent = parent
        self.text = text

    def ask(self) -> bool:
        response = self.warning(self.parent, 'Confirm removal', self.text, self.Yes | self.No)
        return response == self.Yes