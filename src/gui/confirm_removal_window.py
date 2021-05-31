from PyQt5 import QtWidgets


class ConfirmRemovalMessageBox(QtWidgets.QMessageBox):
    def __init__(self, parent, text):
        super().__init__(parent)
        self.parent = parent
        self.text = text

    def ask(self):
        response = self.warning(self.parent, 'Confirm removal', self.text, self.Yes | self.No)
        return response == self.Yes