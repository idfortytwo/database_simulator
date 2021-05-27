import sys

from PyQt5 import QtCore, QtWidgets, QtGui

from db.data_types import Integer, Float, Text
from db.database import Database
from db.exceptions import DuplicateColumnNameError
from db.table import Table


class TypeComboBox(QtWidgets.QComboBox):
    def __init__(self, data_types):
        super().__init__()

        self.data_types_dict = {str(data_type): data_type for data_type in data_types}
        for data_type in data_types:
            self.addItem(str(data_type))

    # def currentText(self):
    #     return self.data_types_dict[self.currentText()]


class AddTableWindow(QtWidgets.QWidget):
    db: Database

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_UI()
        self.add_column()
        self.db = self.main_window.db

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
        self.columns_table.verticalHeader().setDefaultSectionSize(40)
        self.columns_table.verticalHeader().setVisible(True)
        self.columns_table.setColumnWidth(1, 96)

        self.columns_table.clicked.connect(self.clear_color)

        self.setWindowTitle('Add table')
        QtCore.QMetaObject.connectSlotsByName(self)

    def add_column(self):
        row = self.columns_table.rowCount()
        self.columns_table.setRowCount(row + 1)

        column_name = QtWidgets.QTableWidgetItem()
        column_types = TypeComboBox([Integer, Float, Text])

        self.columns_table.setItem(row, 0, column_name)
        self.columns_table.setCellWidget(row, 1, column_types)

    def remove_column(self):
        selected_rows = [index.row() for index in self.columns_table.selectedIndexes()]

        if selected_rows:
            for selected_row in selected_rows:
                self.columns_table.removeRow(selected_row)
        else:
            self.columns_table.removeRow(self.columns_table.rowCount()-1)

    def get_table_data(self):
        table_name = self.line_edit_table_name.text()
        data = {}

        for row_index in range(self.columns_table.rowCount()):
            column_name = self.columns_table.item(row_index, 0).text()
            column_type = self.columns_table.cellWidget(row_index, 1).currentText()

            if column_name not in data.keys():
                data[column_name] = column_type
            else:
                raise DuplicateColumnNameError(row_index)

        return table_name, data

    def clear_color(self, cell_index: QtCore.QModelIndex):
        cell = self.columns_table.item(cell_index.row(), cell_index.column())
        cell.setBackground(QtGui.QColor(0, 0, 0, 0))
        cell.setToolTip('')

    def confirm(self):
        try:
            table_name, data = self.get_table_data()

        except DuplicateColumnNameError as duplicate_error:
            row_index = duplicate_error.row_index
            duplicate_cell = self.columns_table.item(row_index, 0)
            duplicate_cell.setBackground(QtGui.QColor(255, 0, 0, 127))
            duplicate_cell.setToolTip('Column names should be unique')
            self.columns_table.clearSelection()

        else:
            table = Table(data)
            self.db.add_table(table, table_name)

            self.main_window.fill_tables_table()

            self.close()

    def cancel(self):
        self.close()

    def closeEvent(self, a0):
        self.main_window.add_table_window = None
        self.close()


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
    def except_hook(cls, exception, traceback):
        sys.__excepthook__(cls, exception, traceback)

    sys.excepthook = except_hook
    main()
