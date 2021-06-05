import re
import sys

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import pyqtSignal

from db.database import Database
from exceptions.exceptions import ColumnNotFoundError, CellDataConversionError, ConversionError
from db.table import Table
from gui.add_table_window import AddTableWindow
from gui.confirm_removal_window import ConfirmRemovalMessageBox


class ClickableLineEdit(QtWidgets.QLineEdit):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        # noinspection PyUnresolvedReferences
        self.clicked.emit()


class DatabaseWindow(QtWidgets.QMainWindow):
    def __init__(self, db=Database()):
        super().__init__()
        self.db = db
        self.current_table: Table = Table({})
        self.current_table_name: str = ''

        self.add_table_window = None
        self.setup_UI()

        self.records_to_delete: list[int] = []

    def setup_UI(self):
        self.resize(1139, 775)
        # MainWindow.resize(800, 500)
        self.centralwidget = QtWidgets.QWidget(self)

        self.add_table_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_table_button.setGeometry(QtCore.QRect(30, 360, 71, 23))
        self.add_table_button.setText('Add table')
        self.add_table_button.clicked.connect(self.add_table)

        self.delete_table_button = QtWidgets.QPushButton(self.centralwidget)
        self.delete_table_button.setGeometry(QtCore.QRect(30, 390, 91, 23))
        self.delete_table_button.setText('Delete table')
        self.delete_table_button.clicked.connect(self.delete_table)

        self.query_line_edit = ClickableLineEdit(self.centralwidget)
        self.query_line_edit.setGeometry(QtCore.QRect(220, 30, 751, 31))
        line_edit_font = self.query_line_edit.font()
        line_edit_font.setPixelSize(12)
        self.query_line_edit.setFont(line_edit_font)
        # noinspection PyUnresolvedReferences
        self.query_line_edit.clicked.connect(self.clear_line_edit)

        self.reset_button = QtWidgets.QPushButton(self.centralwidget)
        self.reset_button.setGeometry(QtCore.QRect(980, 30, 51, 31))
        self.reset_button.setText('Reset')
        self.reset_button.clicked.connect(self.reset_data)

        self.filter_button = QtWidgets.QPushButton(self.centralwidget)
        self.filter_button.setGeometry(QtCore.QRect(1040, 30, 61, 31))
        self.filter_button.setText('Filter')
        self.filter_button.clicked.connect(self.filter_data)
        self.filter_button.setDisabled(True)

        self.records_label = QtWidgets.QLabel(self.centralwidget)
        self.records_label.setGeometry(QtCore.QRect(220, 70, 41, 21))
        self.records_label.setText('Records')

        self.add_record_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_record_button.setGeometry(QtCore.QRect(270, 70, 21, 21))
        self.add_record_button.setText('+')
        self.add_record_button.setDisabled(True)
        self.add_record_button.clicked.connect(self.add_record)

        self.delete_record_button = QtWidgets.QPushButton(self.centralwidget)
        self.delete_record_button.setGeometry(QtCore.QRect(300, 70, 21, 20))
        self.delete_record_button.setText('-')
        self.delete_record_button.setDisabled(True)
        self.delete_record_button.clicked.connect(self.delete_record)

        self.confirm_changes_button = QtWidgets.QPushButton(self.centralwidget)
        self.confirm_changes_button.setGeometry(QtCore.QRect(340, 70, 51, 21))
        self.confirm_changes_button.setText('Confirm')
        self.confirm_changes_button.setDisabled(True)
        self.confirm_changes_button.clicked.connect(self.confirm_changes)

        self.table_names = QtWidgets.QTableWidget(self.centralwidget)
        self.table_names.setGeometry(QtCore.QRect(30, 30, 171, 321))
        self.table_names.setColumnCount(1)
        self.table_names.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_names.cellDoubleClicked.connect(self.load_table)
        self.table_names.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table_names.setHorizontalHeaderLabels(['Table name'])

        self.data_table = QtWidgets.QTableWidget(self.centralwidget)
        self.data_table.setGeometry(QtCore.QRect(220, 100, 881, 641))
        self.data_table.setColumnCount(0)
        self.data_table.setRowCount(0)

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
        self.load_table_names()

    def save_db(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save database', '', 'Database Files (*.db)')[0]

        if not filename:
            return

        self.db.save(filename)

    def parse_query(self, query):
        pattern = r'\[[\"|\'](\w+)[\"|\']\]'
        p = re.compile(pattern)

        def name_to_index(match: re.Match):
            column_name = match.group(1)
            try:
                column_index = self.current_table.column_names.index(column_name)
            except ValueError:
                raise ColumnNotFoundError(column_name, self.current_table_name)
            return f'[1][{column_index}]'

        return p.sub(name_to_index, query)

    def reset_data(self):
        self.refresh_table_data(self.current_table.data)

    def filter_data(self):
        try:
            parsed_query = self.parse_query(self.query_line_edit.text())

        except ColumnNotFoundError as column_not_found:
            self.query_line_edit.setStyleSheet('QLineEdit {background: rgb(255, 0, 0, 127);}')
            self.query_line_edit.setToolTip(f'No such column: {column_not_found.column_name}')

        else:  # lambda row: row['integer'] in [1, 3, 50, 70]
            rows = dict(filter(eval(parsed_query), self.current_table.data.items()))
            self.refresh_table_data(rows)

    def clear_line_edit(self):
        self.query_line_edit.setStyleSheet('QLineEdit {background: white;}')
        self.query_line_edit.setToolTip('')

    def add_table(self):
        if not self.add_table_window:
            self.add_table_window = AddTableWindow(self)
            self.add_table_window.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            self.add_table_window.show()

    def delete_table(self):
        selected_tables_indexes = self.table_names.selectedIndexes()
        tables_to_delete = []
        for table_index in selected_tables_indexes:
            table_name = self.table_names.item(table_index.row(), 0).text()

            confirmation_window = ConfirmRemovalMessageBox(
                self, f'Are you sure you want to delete table "{table_name}"?')
            if confirmation_window.ask():
                self.db.drop_table(table_name)
                tables_to_delete.append(table_name)

        if tables_to_delete:
            self.load_table_names()

            if self.current_table_name in tables_to_delete:
                self.data_table.setRowCount(0)
                self.data_table.setColumnCount(0)
                self.filter_button.setDisabled(True)

    def add_record(self):
        row_count = self.data_table.rowCount()
        self.data_table.setRowCount(row_count + 1)
        for j in range(self.data_table.columnCount()):
            self.data_table.setItem(row_count, j, QtWidgets.QTableWidgetItem())

        self.data_table.setVerticalHeaderItem(row_count, QtWidgets.QTableWidgetItem('+'))

    def delete_record(self):
        selected_records_indexes = self.data_table.selectedItems()
        for record_index in selected_records_indexes:
            v_header_text = self.data_table.verticalHeaderItem(record_index.row()).text()
            self.data_table.removeRow(record_index.row())

            if v_header_text != '+':
                record_id = int(v_header_text)
                self.records_to_delete.append(record_id)

    def add_records(self):
        for row in range(self.data_table.rowCount()):
            record = []
            if self.data_table.verticalHeaderItem(row).text() == '+':
                for col in range(self.data_table.columnCount()):
                    value_str = self.data_table.item(row, col).text()
                    data_type = self.current_table.column_types[col]

                    try:
                        value = data_type.convert(value_str)
                        record.append(value)
                    except ConversionError:
                        raise CellDataConversionError(col, row, value_str, data_type)

                self.current_table.insert(record)

    def delete_records(self):
        for record_id in self.records_to_delete:
            self.current_table.delete(record_id)

    def confirm_changes(self):
        try:
            self.add_records()

        except CellDataConversionError as convertion_error:
            self.highlight_data_cell(convertion_error.col, convertion_error.row,
                                     f'Failed to convert value to {convertion_error.data_type}')

        else:
            if self.records_to_delete:
                confirmation_window = ConfirmRemovalMessageBox(
                    self, f'Are you sure you want to delete {len(self.records_to_delete)} records?')

                if confirmation_window.ask():
                    self.delete_records()
                self.records_to_delete.clear()

            self.refresh_table_data(self.current_table.data)

    def load_table_names(self):
        table_names = self.db.get_table_names()
        self.table_names.setRowCount(len(table_names))
        for i, row in enumerate(table_names):
            item = QtWidgets.QTableWidgetItem(row)
            self.table_names.setItem(i, 0, item)

    def refresh_table_data(self, data):
        self.data_table.setRowCount(len(data))
        for i, (record_id, record) in enumerate(data.items()):
            for j, value in enumerate(record):
                item = QtWidgets.QTableWidgetItem(str(value))
                self.data_table.setItem(i, j, item)
                self.data_table.setVerticalHeaderItem(i, QtWidgets.QTableWidgetItem(str(record_id)))

    def load_table(self, row):
        table_name = self.table_names.item(row, 0).text()
        self.current_table_name = table_name
        self.current_table = self.db.get_table(table_name)

        column_names = self.current_table.column_names
        column_types = self.current_table.column_types

        self.data_table.clear()

        self.data_table.setColumnCount(len(column_names))
        self.data_table.setHorizontalHeaderLabels(column_names)

        for col, column_type in enumerate(column_types):
            self.data_table.horizontalHeaderItem(col).setToolTip(str(column_type))

        self.refresh_table_data(self.current_table.data)

        self.filter_button.setDisabled(False)
        self.add_record_button.setDisabled(False)
        self.delete_record_button.setDisabled(False)
        self.confirm_changes_button.setDisabled(False)

    def highlight_data_cell(self, col, row, tool_tip):
        cell = self.data_table.item(row, col)
        cell.setBackground(QtGui.QColor(255, 0, 0, 127))
        cell.setToolTip(tool_tip)
        self.data_table.clearSelection()

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
    app = QtWidgets.QApplication(sys.argv)
    w = DatabaseWindow()
    w.db.load('kek.db')
    w.load_table_names()
    w.load_table(0)
    w.show()
    app.exec()


if __name__ == '__main__':
    def except_hook(cls, exception, traceback):
        sys.__excepthook__(cls, exception, traceback)
    sys.excepthook = except_hook

    main()
