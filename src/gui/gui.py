import sys

from PyQt5 import QtCore, QtWidgets
from db.database import Database


class AddTableWindow(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_UI()

    def setup_UI(self):
        self.resize(421, 385)

        self.button_box = QtWidgets.QDialogButtonBox(self)
        self.button_box.setGeometry(QtCore.QRect(230, 330, 161, 51))
        self.button_box.setMinimumSize(QtCore.QSize(0, 0))
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.button_box.accepted.connect(self.confirm)
        self.button_box.rejected.connect(self.cancel)

        self.label_table_name = QtWidgets.QLabel(self)
        self.label_table_name.setGeometry(QtCore.QRect(20, 20, 61, 16))
        self.label_table_name.setText('Table name')

        self.line_edit_table_name = QtWidgets.QLineEdit(self)
        self.line_edit_table_name.setGeometry(QtCore.QRect(20, 40, 191, 20))

        self.label_columns = QtWidgets.QLabel(self)
        self.label_columns.setGeometry(QtCore.QRect(20, 80, 61, 16))
        self.label_columns.setText('Columns')

        self.add_column_button = QtWidgets.QPushButton(self)
        self.add_column_button.setGeometry(QtCore.QRect(70, 80, 16, 16))
        self.add_column_button.setText('+')
        self.add_column_button.clicked.connect(self.add_column)

        self.remove_column_button = QtWidgets.QPushButton(self)
        self.remove_column_button.setGeometry(QtCore.QRect(90, 80, 16, 16))
        self.remove_column_button.setText('-')
        self.remove_column_button.clicked.connect(self.remove_column)

        self.columns_table = QtWidgets.QTableWidget(self)
        self.columns_table.setGeometry(QtCore.QRect(20, 100, 381, 221))
        self.columns_table.setColumnCount(2)

        self.columns_table.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem('Column name'))
        self.columns_table.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem('Data type'))

        self.columns_table.horizontalHeader().setVisible(True)
        self.columns_table.horizontalHeader().setDefaultSectionSize(220)
        self.columns_table.horizontalHeader().setHighlightSections(True)
        self.columns_table.horizontalHeader().setSortIndicatorShown(False)
        self.columns_table.horizontalHeader().setStretchLastSection(True)
        self.columns_table.verticalHeader().setDefaultSectionSize(50)
        self.columns_table.verticalHeader().setStretchLastSection(True)
        self.columns_table.setColumnWidth(1, 96)

        self.setWindowTitle('Add table')
        QtCore.QMetaObject.connectSlotsByName(self)

    def add_column(self):
        print('add column')

    def remove_column(self):
        print('remove column')

    def confirm(self):
        print('confirm')

    def cancel(self):
        print('cancel')

    def closeEvent(self, a0):
        self.main_window.add_table_window = None
        super().close()


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

        headers = table.column_names
        rows = table.data

        self.table_data_table.clear()

        self.table_data_table.setColumnCount(len(headers))
        self.table_data_table.setHorizontalHeaderLabels(headers)
        self.table_data_table.setRowCount(len(rows))

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
    main()
