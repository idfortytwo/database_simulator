import sys

from PyQt5 import QtCore, QtWidgets

from db.database import Database
from gui.add_table_window import AddTableWindow


class ConfirmRemoval(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()


class DatabaseWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()

        self.add_table_window = None
        self.setup_UI()

    def setup_UI(self):
        self.resize(1139, 775)
        # MainWindow.resize(800, 500)
        self.centralwidget = QtWidgets.QWidget(self)

        self.add_table_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_table_button.setGeometry(QtCore.QRect(30, 360, 71, 23))
        self.add_table_button.setText('Add table')
        self.add_table_button.clicked.connect(self.add_table)

        # TODO: remove table function
        # TODO: ask for confirmation
        self.remove_table_button = QtWidgets.QPushButton(self.centralwidget)
        self.remove_table_button.setGeometry(QtCore.QRect(30, 390, 91, 23))
        self.remove_table_button.setText('Remove table')

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(220, 30, 801, 41))
        self.search_button = QtWidgets.QPushButton(self.centralwidget)
        self.search_button.setGeometry(QtCore.QRect(1030, 30, 71, 41))
        self.search_button.setText("Search")

        self.table_names_table = QtWidgets.QTableWidget(self.centralwidget)
        self.table_names_table.setGeometry(QtCore.QRect(30, 30, 171, 321))
        self.table_names_table.setColumnCount(1)
        self.table_names_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_names_table.cellDoubleClicked.connect(self.refill_table_data)
        self.table_names_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.table_data_table = QtWidgets.QTableWidget(self.centralwidget)
        self.table_data_table.setGeometry(QtCore.QRect(220, 80, 881, 661))
        self.table_data_table.setColumnCount(0)
        self.table_data_table.setRowCount(0)

        self.load_db_button = QtWidgets.QPushButton(self.centralwidget)
        self.load_db_button.setGeometry(QtCore.QRect(30, 670, 91, 31))
        self.load_db_button.setText('Load database')
        self.load_db_button.clicked.connect(self.load_db)

        self.save_db_button = QtWidgets.QPushButton(self.centralwidget)
        self.save_db_button.setGeometry(QtCore.QRect(30, 710, 91, 31))
        self.save_db_button.setText('Save database')
        self.save_db_button.clicked.connect(self.save_db)

        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.statusbar)

        self.setWindowTitle('Database Simulator')
        QtCore.QMetaObject.connectSlotsByName(self)

    def load_db(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Load database', '', 'Database Files (*.db)')[0]

        if not filename:
            return

        self.db.load(filename)
        self.fill_tables_table()

    def save_db(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save database', '', 'Database Files (*.db)')[0]

        if not filename:
            return

        self.db.save(filename)

    def add_table(self):
        if not self.add_table_window:
            self.add_table_window = AddTableWindow(self)
            self.add_table_window.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            self.add_table_window.show()

    def fill_tables_table(self):
        table_names = self.db.get_table_names()
        self.table_names_table.setRowCount(len(table_names))
        for i, row in enumerate(table_names):
            item = QtWidgets.QTableWidgetItem(row)
            self.table_names_table.setItem(i, 0, item)

    def refill_table_data(self, row):
        table_name = self.table_names_table.item(row, 0).text()
        table = self.db.get_table(table_name)

        column_names = table.column_names
        column_types = table.column_types
        rows = table.data

        self.table_data_table.clear()

        self.table_data_table.setColumnCount(len(column_names))
        self.table_data_table.setHorizontalHeaderLabels(column_names)
        self.table_data_table.setRowCount(len(rows))

        for col, column_type in enumerate(column_types):
            self.table_data_table.horizontalHeaderItem(col).setToolTip(str(column_type))

        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                item = QtWidgets.QTableWidgetItem(str(value))
                self.table_data_table.setItem(i, j, item)

    def closeEvent(self, a0):
        if self.add_table_window:
            self.add_table_window.close()
        super().close()


def run_GUI():
    app = QtWidgets.QApplication(sys.argv)
    w = DatabaseWindow()
    w.show()
    app.exec()


def main():
    run_GUI()


if __name__ == '__main__':
    def except_hook(cls, exception, traceback):
        sys.__excepthook__(cls, exception, traceback)

    sys.excepthook = except_hook
    main()
