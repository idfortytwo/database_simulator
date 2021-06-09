from PyQt5 import QtWidgets


class ConfirmRemovalMessageBox(QtWidgets.QMessageBox):
    # noinspection PyUnresolvedReferences
    def __init__(self, parent: 'DatabaseWindow', text: str):
        super().__init__(parent)
        self._parent = parent
        self._text = text

    def ask(self) -> bool:
        response = self.warning(self._parent, 'Confirm removal', self._text, self.Yes | self.No)
        return response == self.Yes