import re

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal

from db import data_types
from exceptions.exceptions import DuplicateColumnNameError, EmptyColumnNameError, IllegalColumnNameError, EmptyTableNameError, \
    IllegalTableNameError
from db.table import Table


NAMING_PATTERN = '^[A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ0-9_]*$'


class TypeComboBox(QtWidgets.QComboBox):
    def __init__(self, data_types):
        super().__init__()

        self.data_types_dict = {str(data_type): data_type for data_type in data_types}
        for data_type in data_types:
            self.addItem(str(data_type))


class ClickableLineEdit(QtWidgets.QLineEdit):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        # noinspection PyUnresolvedReferences
        self.clicked.emit()


class AddTableWindow(QtWidgets.QWidget):
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

        self.line_edit_table_name = ClickableLineEdit(self)
        self.line_edit_table_name.setGeometry(QtCore.QRect(20, 40, 191, 20))
        # noinspection PyUnresolvedReferences
        self.line_edit_table_name.clicked.connect(self.clear_name_line_edit_color)
        self.line_edit_table_name.property("qmouse")

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
        self.columns_table.verticalHeader().setDefaultSectionSize(30)
        self.columns_table.verticalHeader().setVisible(True)
        self.columns_table.setColumnWidth(1, 96)

        self.columns_table.clicked.connect(self.clear_cell_color)

        self.setWindowTitle('Add table')
        QtCore.QMetaObject.connectSlotsByName(self)

    def add_column(self):
        row = self.columns_table.rowCount()
        self.columns_table.setRowCount(row + 1)

        column_name = QtWidgets.QTableWidgetItem()
        column_types = TypeComboBox([
            data_types.Integer,
            data_types.Float,
            data_types.Text])

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
        if not table_name:
            raise EmptyTableNameError()

        if not re.match(NAMING_PATTERN, table_name):
            raise IllegalTableNameError()

        data = {}

        for row_index in range(self.columns_table.rowCount()):
            column_name = self.columns_table.item(row_index, 0).text().strip()
            column_type = self.columns_table.cellWidget(row_index, 1).currentText()

            if not column_name:
                raise EmptyColumnNameError(row_index)

            if not re.match(NAMING_PATTERN, column_name):
                raise IllegalColumnNameError(row_index)

            if column_name not in data.keys():
                data[column_name] = column_type
            else:
                raise DuplicateColumnNameError(row_index)

        return table_name, data

    def clear_cell_color(self, cell_index: QtCore.QModelIndex):
        cell = self.columns_table.item(cell_index.row(), cell_index.column())
        cell.setBackground(QtGui.QColor(0, 0, 0, 0))
        cell.setToolTip('')

    def clear_name_line_edit_color(self):
        self.line_edit_table_name.setStyleSheet('QLineEdit {background: white;}')
        self.line_edit_table_name.setToolTip('')

    def confirm(self):
        try:
            table_name, data = self.get_table_data()
        except EmptyTableNameError:
            self.highlight_table_name_line_edit('Table name should not be empty')

        except IllegalTableNameError:
            self.highlight_table_name_line_edit('Table should only contain characters, numbers or _')

        except EmptyColumnNameError as empty_name_error:
            row_index = empty_name_error.row_index
            self.highlight_column_name_cell(row_index, 'Column names should not be empty')

        except IllegalColumnNameError as illegal_name_error:
            row_index = illegal_name_error.row_index
            self.highlight_column_name_cell(row_index, 'Column name should only contain characters, numbers or _')

        except DuplicateColumnNameError as duplicate_error:
            row_index = duplicate_error.row_index
            self.highlight_column_name_cell(row_index, 'Column names should be unique')

        else:
            table = Table(data)
            self.db.add_table(table, table_name)
            self.main_window.load_table_names()
            self.close()

    def highlight_column_name_cell(self, row_index, tool_tip):
        cell = self.columns_table.item(row_index, 0)
        cell.setBackground(QtGui.QColor(255, 0, 0, 127))
        cell.setToolTip(tool_tip)
        self.columns_table.clearSelection()

    def highlight_table_name_line_edit(self, tool_tip):
        self.line_edit_table_name.setStyleSheet('QLineEdit {background: rgb(255, 0, 0, 127);}')
        self.line_edit_table_name.setToolTip(tool_tip)

    def cancel(self):
        self.close()

    def closeEvent(self, a0):
        self.main_window.add_table_window = None
        self.close()
