import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QAbstractItemView, QMainWindow, QWidget, QPushButton, QLineEdit, QTableWidget, QStatusBar, \
    QTableWidgetItem, QVBoxLayout, QLabel, QApplication

from db.database import Database


class AddTableWindow(QWidget):
    def __init__(self):
        super().__init__()


class ConfirmRemoval(QWidget):
    def __init__(self):
        super().__init__()


class DatabaseWindow:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = QMainWindow()
        self.db = Database()

    def setupUi(self):
        self.main_window.setObjectName("MainWindow")
        self.main_window.resize(1139, 775)
        # MainWindow.resize(800, 500)
        self.centralwidget = QWidget(self.main_window)
        self.centralwidget.setObjectName("centralwidget")

        self.add_table_button = QPushButton(self.centralwidget)
        self.add_table_button.setGeometry(QtCore.QRect(30, 360, 71, 23))
        self.add_table_button.setText('Add table')

        self.remove_table_button = QPushButton(self.centralwidget)
        self.remove_table_button.setGeometry(QtCore.QRect(30, 390, 91, 23))
        self.remove_table_button.setText('Remove table')

        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(220, 30, 801, 41))
        self.lineEdit.setObjectName("lineEdit")
        self.search_button = QPushButton(self.centralwidget)
        self.search_button.setGeometry(QtCore.QRect(1030, 30, 71, 41))
        self.search_button.setObjectName("pushButton_3")
        self.search_button.setText("Search")

        self.table_names_table = QTableWidget(self.centralwidget)
        self.table_names_table.setGeometry(QtCore.QRect(30, 30, 171, 321))
        self.table_names_table.setObjectName("tableWidget")
        self.table_names_table.setColumnCount(1)
        self.table_names_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_names_table.cellDoubleClicked.connect(self.refill_table_data)

        self.table_data_table = QTableWidget(self.centralwidget)
        self.table_data_table.setGeometry(QtCore.QRect(220, 80, 881, 661))
        self.table_data_table.setObjectName("tableWidget_2")
        self.table_data_table.setColumnCount(0)
        self.table_data_table.setRowCount(0)

        self.load_db_button = QtWidgets.QPushButton(self.centralwidget)
        self.load_db_button.setGeometry(QtCore.QRect(30, 670, 91, 31))
        self.load_db_button.setObjectName("pushButton_4")
        self.load_db_button.setText('Load database')
        self.load_db_button.clicked.connect(self.load_db)

        self.save_db_button = QtWidgets.QPushButton(self.centralwidget)
        self.save_db_button.setGeometry(QtCore.QRect(30, 710, 91, 31))
        self.save_db_button.setObjectName("pushButton_5")
        self.save_db_button.setText('Save database')
        self.save_db_button.clicked.connect(self.save_db)

        self.main_window.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(self.main_window)
        self.statusbar.setObjectName("statusbar")
        self.main_window.setStatusBar(self.statusbar)

        self.main_window.setWindowTitle('Database Simulator')
        QtCore.QMetaObject.connectSlotsByName(self.main_window)

    def load_db(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(
            self.main_window, 'Load database', '', 'Database Files (*.db)')[0]

        if not filename:
            return

        self.db.load(filename)
        self.fill_tables_table()

    def save_db(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(
            self.main_window, 'Save database', '', 'Database Files (*.db)')[0]

        if not filename:
            return

        self.db.save(filename)

    def fill_tables_table(self):
        table_names = self.db.get_table_names()
        self.table_names_table.setRowCount(len(table_names))
        for i, row in enumerate(table_names):
            item = QTableWidgetItem(row)
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

    def show(self):
        self.setupUi()
        self.fill_tables_table()

        self.main_window.show()
        self.app.exec()


def main():
    ui = DatabaseWindow()
    ui.show()

    # database_selection_window = SelectDatabaseWindow()
    # database_selection_window.show()


if __name__ == '__main__':
    main()
