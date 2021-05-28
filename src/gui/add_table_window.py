from PyQt5 import QtCore, QtGui, QtWidgets

from db import data_types
from db.exceptions import DuplicateColumnNameError
from db.table import Table


class TypeComboBox(QtWidgets.QComboBox):
    def __init__(self, data_types):
        super().__init__()

        self.data_types_dict = {str(data_type): data_type for data_type in data_types}
        for data_type in data_types:
            self.addItem(str(data_type))


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
        self.columns_table.verticalHeader().setDefaultSectionSize(30)
        self.columns_table.verticalHeader().setVisible(True)
        self.columns_table.setColumnWidth(1, 96)

        self.columns_table.clicked.connect(self.clear_color)

        self.setWindowTitle('Add table')
        QtCore.QMetaObject.connectSlotsByName(self)

    # TODO: check if table name is empty
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

    # TODO: ask for confirmation
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
            self.highlight_duplicated_row(row_index)

        else:
            table = Table(data)
            self.db.add_table(table, table_name)
            self.main_window.fill_tables_table()
            self.close()

    def highlight_duplicated_row(self, row_index):
        duplicate_cell = self.columns_table.item(row_index, 0)
        duplicate_cell.setBackground(QtGui.QColor(255, 0, 0, 127))
        duplicate_cell.setToolTip('Column names should be unique')
        self.columns_table.clearSelection()

    def cancel(self):
        self.close()

    def closeEvent(self, a0):
        self.main_window.add_table_window = None
        self.close()
