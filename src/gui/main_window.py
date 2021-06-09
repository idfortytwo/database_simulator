import re
import sys
from typing import Union

from PyQt5 import QtCore, QtWidgets, QtGui

from db.database import Database
from exceptions.exceptions import ColumnNotFoundError, CellDataConversionError, ConversionError
from db.table import Table
from gui.add_table_window import AddTableWindow
from gui.confirm_removal_window import ConfirmRemovalMessageBox
from gui.widgets import ClickableLineEdit


class DatabaseWindow(QtWidgets.QMainWindow):
    def __init__(self, db=Database()):
        super().__init__()
        self._db = db
        self._current_table: Table = Table({})
        self._current_table_name: str = ''

        self._add_table_window: Union[AddTableWindow, None] = None
        self._setup_UI()

        self.records_to_delete: list[int] = []

    def _setup_UI(self) -> None:
        self.setFixedSize(1139, 775)
        self._centralwidget = QtWidgets.QWidget(self)

        self._add_table_button = QtWidgets.QPushButton(self._centralwidget)
        self._add_table_button.setGeometry(QtCore.QRect(30, 360, 71, 23))
        self._add_table_button.setText('Add table')
        self._add_table_button.clicked.connect(self._add_table)

        self._delete_table_button = QtWidgets.QPushButton(self._centralwidget)
        self._delete_table_button.setGeometry(QtCore.QRect(30, 390, 91, 23))
        self._delete_table_button.setText('Delete table')
        self._delete_table_button.clicked.connect(self._delete_table)

        self._query_line_edit = ClickableLineEdit(self._centralwidget)
        self._query_line_edit.setGeometry(QtCore.QRect(220, 30, 751, 31))
        line_edit_font = self._query_line_edit.font()
        line_edit_font.setPixelSize(12)
        self._query_line_edit.setFont(line_edit_font)
        # noinspection PyUnresolvedReferences
        self._query_line_edit.clicked.connect(self._clear_line_edit)

        self._reset_button = QtWidgets.QPushButton(self._centralwidget)
        self._reset_button.setGeometry(QtCore.QRect(980, 30, 51, 31))
        self._reset_button.setText('Reset')
        self._reset_button.clicked.connect(self._reset_data)

        self._filter_button = QtWidgets.QPushButton(self._centralwidget)
        self._filter_button.setGeometry(QtCore.QRect(1040, 30, 61, 31))
        self._filter_button.setText('Filter')
        self._filter_button.clicked.connect(self._filter_data)
        self._filter_button.setDisabled(True)

        self._records_label = QtWidgets.QLabel(self._centralwidget)
        self._records_label.setGeometry(QtCore.QRect(220, 70, 41, 21))
        self._records_label.setText('Records')

        self._add_record_button = QtWidgets.QPushButton(self._centralwidget)
        self._add_record_button.setGeometry(QtCore.QRect(270, 70, 21, 21))
        self._add_record_button.setText('+')
        self._add_record_button.setDisabled(True)
        self._add_record_button.clicked.connect(self._add_record)

        self._delete_record_button = QtWidgets.QPushButton(self._centralwidget)
        self._delete_record_button.setGeometry(QtCore.QRect(300, 70, 21, 20))
        self._delete_record_button.setText('-')
        self._delete_record_button.setDisabled(True)
        self._delete_record_button.clicked.connect(self._delete_record)

        self._confirm_changes_button = QtWidgets.QPushButton(self._centralwidget)
        self._confirm_changes_button.setGeometry(QtCore.QRect(340, 70, 51, 21))
        self._confirm_changes_button.setText('Confirm')
        self._confirm_changes_button.setDisabled(True)
        self._confirm_changes_button.clicked.connect(self._confirm_changes)

        self._table_names = QtWidgets.QTableWidget(self._centralwidget)
        self._table_names.setGeometry(QtCore.QRect(30, 30, 171, 321))
        self._table_names.setColumnCount(1)
        self._table_names.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self._table_names.cellDoubleClicked.connect(self._load_table)
        self._table_names.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self._table_names.setHorizontalHeaderLabels(['Table name'])

        self._data_table = QtWidgets.QTableWidget(self._centralwidget)
        self._data_table.setGeometry(QtCore.QRect(220, 100, 881, 641))
        self._data_table.setColumnCount(0)
        self._data_table.setRowCount(0)
        self._data_table.horizontalHeader().setMinimumSectionSize(100)

        self._load_db_button = QtWidgets.QPushButton(self._centralwidget)
        self._load_db_button.setGeometry(QtCore.QRect(30, 670, 91, 31))
        self._load_db_button.setText('Load database')
        self._load_db_button.clicked.connect(self._load_db)

        self._save_db_button = QtWidgets.QPushButton(self._centralwidget)
        self._save_db_button.setGeometry(QtCore.QRect(30, 710, 91, 31))
        self._save_db_button.setText('Save database')
        self._save_db_button.clicked.connect(self._save_db)

        self.setCentralWidget(self._centralwidget)
        self._statusbar = QtWidgets.QStatusBar(self)
        self.setStatusBar(self._statusbar)

        self.setWindowTitle('Database Simulator')
        QtCore.QMetaObject.connectSlotsByName(self)

    @property
    def db(self):
        return self._db

    def _load_db(self) -> None:
        filename = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Load database', '', 'Database Files (*.db)')[0]

        if not filename:
            return

        self._db.load(filename)
        self._load_table_names()

    def _save_db(self) -> None:
        filename = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save database', '', 'Database Files (*.db)')[0]

        if not filename:
            return

        self._db.save(filename)

    def _parse_query(self, query: str) -> str:
        pattern = r'\[[\"|\'](\w+)[\"|\']\]'
        p = re.compile(pattern)

        def name_to_index(match: re.Match):
            column_name = match.group(1)
            try:
                column_index = self._current_table.column_names.index(column_name)
            except ValueError:
                raise ColumnNotFoundError(column_name, self._current_table_name)
            return f'[1][{column_index}]'

        return p.sub(name_to_index, query)

    def _reset_data(self) -> None:
        self._refresh_table_data(self._current_table.data)

    def _filter_data(self) -> None:
        try:
            parsed_query = self._parse_query(self._query_line_edit.text())

        except ColumnNotFoundError as column_not_found:
            self._query_line_edit.setStyleSheet('QLineEdit {background: rgb(255, 0, 0, 127);}')
            self._query_line_edit.setToolTip(f'No such column: {column_not_found.column_name}')

        else:
            rows = dict(filter(eval(parsed_query), self._current_table.data.items()))
            self._refresh_table_data(rows)

    def _clear_line_edit(self) -> None:
        self._query_line_edit.setStyleSheet('QLineEdit {background: white;}')
        self._query_line_edit.setToolTip('')

    def _add_table(self) -> None:
        if not self._add_table_window:
            self._add_table_window = AddTableWindow(self)
            self._add_table_window.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            self._add_table_window.show()

    def _delete_table(self) -> None:
        selected_tables_indexes = self._table_names.selectedIndexes()
        tables_to_delete = []
        for table_index in selected_tables_indexes:
            table_name = self._table_names.item(table_index.row(), 0).text()

            confirmation_window = ConfirmRemovalMessageBox(
                self, f'Are you sure you want to delete table "{table_name}"?')
            if confirmation_window.ask():
                self._db.drop_table(table_name)
                tables_to_delete.append(table_name)

        if tables_to_delete:
            self._load_table_names()

            if self._current_table_name in tables_to_delete:
                self._data_table.setRowCount(0)
                self._data_table.setColumnCount(0)
                self._filter_button.setDisabled(True)
                self._add_record_button.setDisabled(True)
                self._delete_record_button.setDisabled(True)
                self._confirm_changes_button.setDisabled(True)

    def _add_record(self) -> None:
        row_count = self._data_table.rowCount()
        self._data_table.setRowCount(row_count + 1)
        for j in range(self._data_table.columnCount()):
            self._data_table.setItem(row_count, j, QtWidgets.QTableWidgetItem())

        self._data_table.setVerticalHeaderItem(row_count, QtWidgets.QTableWidgetItem('+'))

    def _delete_record(self) -> None:
        selected_records_indexes = self._data_table.selectedItems()
        for record_index in selected_records_indexes:
            v_header_text = self._data_table.verticalHeaderItem(record_index.row()).text()
            self._data_table.removeRow(record_index.row())

            if v_header_text != '+':
                record_id = int(v_header_text)
                self.records_to_delete.append(record_id)

    def _add_records(self) -> None:
        for row in range(self._data_table.rowCount()):
            record = []
            if self._data_table.verticalHeaderItem(row).text() == '+':
                for col in range(self._data_table.columnCount()):
                    value_str = self._data_table.item(row, col).text()
                    data_type = self._current_table.column_types[col]

                    try:
                        value = data_type.convert(value_str)
                        record.append(value)
                    except ConversionError:
                        raise CellDataConversionError(col, row, value_str, data_type)

                self._current_table.insert(record)

    def _delete_records(self) -> None:
        for record_id in self.records_to_delete:
            self._current_table.delete(record_id)

    def _confirm_changes(self) -> None:
        try:
            self._add_records()

        except CellDataConversionError as convertion_error:
            self._highlight_data_cell(convertion_error.col, convertion_error.row,
                                      f'Failed to convert value to {convertion_error.data_type}')

        else:
            if self.records_to_delete:
                confirmation_window = ConfirmRemovalMessageBox(
                    self, f'Are you sure you want to delete {len(self.records_to_delete)} records?')

                if confirmation_window.ask():
                    self._delete_records()
                self.records_to_delete.clear()

            self._refresh_table_data(self._current_table.data)

    def _load_table_names(self) -> None:
        table_names = self._db.get_table_names()
        self._table_names.setRowCount(len(table_names))
        for i, row in enumerate(table_names):
            item = QtWidgets.QTableWidgetItem(row)
            self._table_names.setItem(i, 0, item)

    def _refresh_table_data(self, data: dict[int: Union[int, float, str]]) -> None:
        self._data_table.setRowCount(len(data))
        for i, (record_id, record) in enumerate(data.items()):
            for j, value in enumerate(record):
                item = QtWidgets.QTableWidgetItem(str(value))
                self._data_table.setItem(i, j, item)
                self._data_table.setVerticalHeaderItem(i, QtWidgets.QTableWidgetItem(str(record_id)))

    def _load_table(self, table_name_row: int) -> None:
        table_name = self._table_names.item(table_name_row, 0).text()
        self._current_table_name = table_name
        self._current_table = self._db.get_table(table_name)

        column_names = self._current_table.column_names
        column_types = self._current_table.column_types

        self._data_table.clear()

        self._data_table.setColumnCount(len(column_names))
        self._data_table.setHorizontalHeaderLabels(column_names)

        for col, column_type in enumerate(column_types):
            self._data_table.horizontalHeaderItem(col).setToolTip(str(column_type))

        self._refresh_table_data(self._current_table.data)

        self._filter_button.setDisabled(False)
        self._add_record_button.setDisabled(False)
        self._delete_record_button.setDisabled(False)
        self._confirm_changes_button.setDisabled(False)
        self._data_table.resizeColumnsToContents()

    def _highlight_data_cell(self, col: int, row: int, tool_tip: str):
        cell = self._data_table.item(row, col)
        cell.setBackground(QtGui.QColor(255, 0, 0, 127))
        cell.setToolTip(tool_tip)
        self._data_table.clearSelection()

    def closeEvent(self, a0) -> None:
        if self._add_table_window:
            self._add_table_window.close()
        super().close()


def run_GUI() -> None:
    app = QtWidgets.QApplication(sys.argv)
    w = DatabaseWindow()
    w.show()
    app.exec()
