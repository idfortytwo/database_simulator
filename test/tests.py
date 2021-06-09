import sys
import unittest

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication

from db.data_types import Integer, Text, Float
from gui.main_window import DatabaseWindow
from src.db.database import Database

app = QApplication(sys.argv)


class GuiTest(unittest.TestCase):
    TEST_DB = Database()

    def setUp(self):
        self.gui = DatabaseWindow(GuiTest.TEST_DB)
        self.gui._load_table_names()

    def test_02(self):
        left_click = QtCore.Qt.LeftButton

        QTest.mouseClick(self.gui._add_table_button, left_click)
        for letter in 'testi':
            QTest.keyClick(self.gui._add_table_window.line_edit_table_name, letter)

        self.gui._add_table_window.columns_table.item(0, 0).setText('ID')
        self.gui._add_table_window.columns_table.cellWidget(0, 1).setCurrentIndex(0)

        QTest.mouseClick(self.gui._add_table_window.add_column_button, left_click)
        self.gui._add_table_window.columns_table.item(1, 0).setText('imię')
        self.gui._add_table_window.columns_table.cellWidget(1, 1).setCurrentIndex(2)

        QTest.mouseClick(self.gui._add_table_window.add_column_button, left_click)
        self.gui._add_table_window.columns_table.item(2, 0).setText('nazwisko')
        self.gui._add_table_window.columns_table.cellWidget(2, 1).setCurrentIndex(2)

        QTest.mouseClick(self.gui._add_table_window.add_column_button, left_click)
        self.gui._add_table_window.columns_table.item(3, 0).setText('wzrost')
        self.gui._add_table_window.columns_table.cellWidget(3, 1).setCurrentIndex(1)

        yes_button = QtWidgets.QDialogButtonBox.Ok
        QTest.mouseClick(self.gui._add_table_window.button_box.button(yes_button), left_click)

        self.assertEqual({
            'ID': Integer,
            'imię': Text,
            'nazwisko': Text,
            'wzrost': Float
        },
            self.gui._db.get_table('testi').get_columns())

    def add_row(self, data):
        row = self.gui._data_table.rowCount()
        QTest.mouseClick(self.gui._add_record_button, QtCore.Qt.LeftButton)
        for col, value in enumerate(data):
            self.gui._data_table.item(row, col).setText(value)

    def test_03(self):
        self.gui._load_table(0)

        self.add_row(['1', 'Roch', 'Przyłbipięt', '1.50'])
        QTest.mouseClick(self.gui._confirm_changes_button, QtCore.Qt.LeftButton)

        self.assertEqual({0: [1, 'Roch', 'Przyłbipięt', 1.5]},
                         self.gui._db.get_table('testi').data)

    def test_04(self):
        self.gui._load_table(0)

        self.add_row(['2', 'Ziemniaczysław', 'Bulwiasty', '1.91'])
        QTest.mouseClick(self.gui._confirm_changes_button, QtCore.Qt.LeftButton)

        self.assertEqual({
            0: [1, 'Roch', 'Przyłbipięt', 1.5],
            1: [2, 'Ziemniaczysław', 'Bulwiasty', 1.91]
        },
            self.gui._db.get_table('testi').data)

    def test_05(self):
        self.gui._load_table(0)

        self.add_row(['cztery', 'bla', 'bla', '-90'])
        QTest.mouseClick(self.gui._confirm_changes_button, QtCore.Qt.LeftButton)

        self.assertEqual('Failed to convert value to Integer',
                         self.gui._data_table.item(2, 0).toolTip())

    def test_06(self):
        self.gui._load_table(0)

        gui_data = {
            int(self.gui._data_table.verticalHeaderItem(row).text()): [
                self.gui._data_table.item(row, col).text()
                for col
                in range(self.gui._data_table.columnCount())
            ]
            for row
            in range(self.gui._data_table.rowCount())
        }

        db_data = {
            k: [str(value) for value in v]
            for k, v
            in self.gui._current_table.data.items()
        }

        self.assertEqual(gui_data, db_data)

    def test_07(self):
        self.gui._load_table(0)
        self.add_row(['3', 'aaa', 'AAA', '1.75'])
        self.add_row(['4', 'bbb', 'BBB', '1.80'])
        self.add_row(['5', 'ccc', 'CCC', '1.85'])
        QTest.mouseClick(self.gui._confirm_changes_button, QtCore.Qt.LeftButton)

        self.gui._data_table.setRangeSelected(QtWidgets.QTableWidgetSelectionRange(0, 0, 0, 0), True)
        self.gui._data_table.setRangeSelected(QtWidgets.QTableWidgetSelectionRange(2, 0, 2, 0), True)
        QTest.mouseClick(self.gui._delete_record_button, QtCore.Qt.LeftButton)

        self.gui._add_records()
        self.gui.records_to_delete.clear()
        self.gui._refresh_table_data(self.gui._current_table.data)

        self.gui._data_table.setRangeSelected(QtWidgets.QTableWidgetSelectionRange(0, 0, 0, 0), True)
        self.gui._data_table.setRangeSelected(QtWidgets.QTableWidgetSelectionRange(2, 0, 2, 0), True)
        QTest.mouseClick(self.gui._delete_record_button, QtCore.Qt.LeftButton)

        self.gui._add_records()
        self.gui._delete_records()
        self.gui.records_to_delete.clear()
        self.gui._refresh_table_data(self.gui._current_table.data)

        self.assertEqual({
            1: [2, 'Ziemniaczysław', 'Bulwiasty', 1.91],
            3: [4, 'bbb', 'BBB', 1.8],
            4: [5, 'ccc', 'CCC', 1.85]
        },
            self.gui._db.get_table('testi').data)

    def test_08(self):
        left_click = QtCore.Qt.LeftButton

        QTest.mouseClick(self.gui._add_table_button, left_click)
        for letter in 'test2':
            QTest.keyClick(self.gui._add_table_window.line_edit_table_name, letter)

        self.gui._add_table_window.columns_table.item(0, 0).setText('reserved')
        self.gui._add_table_window.columns_table.cellWidget(0, 1).setCurrentIndex(2)

        QTest.mouseClick(self.gui._add_table_window.add_column_button, left_click)
        self.gui._add_table_window.columns_table.item(1, 0).setText('kolor')
        self.gui._add_table_window.columns_table.cellWidget(1, 1).setCurrentIndex(0)

        yes_button = QtWidgets.QDialogButtonBox.Ok
        QTest.mouseClick(self.gui._add_table_window.button_box.button(yes_button), left_click)

        self.assertEqual({
            'reserved': Text,
            'kolor': Integer
        },
            self.gui._db.get_table('test2').get_columns())

    def test_09(self):
        self.gui._load_table(1)

        self.add_row(['', '1337'])
        QTest.mouseClick(self.gui._confirm_changes_button, QtCore.Qt.LeftButton)

        self.assertEqual({0: ['', 1337]}, self.gui._db.get_table('test2').data)

    def test_10(self):
        self.gui._load_table(1)

        self.add_row(['bla', '1939b'])
        QTest.mouseClick(self.gui._confirm_changes_button, QtCore.Qt.LeftButton)

        self.assertEqual('Failed to convert value to Integer',
                         self.gui._data_table.item(1, 1).toolTip())

    def test_11(self):
        self.gui._db.drop_table('test2')
        self.assertEqual(list(self.gui._db.tables.keys()), ['testi'])

    def test_12(self):
        QTest.mouseClick(self.gui._add_table_button, QtCore.Qt.LeftButton)
        yes_button = QtWidgets.QDialogButtonBox.Ok
        QTest.mouseClick(self.gui._add_table_window.button_box.button(yes_button), QtCore.Qt.LeftButton)

        self.assertEqual('Table name should not be empty',
                         self.gui._add_table_window.line_edit_table_name.toolTip())

        QTest.mouseClick(self.gui._add_table_window.button_box.button(QtWidgets.QDialogButtonBox.Cancel),
                         QtCore.Qt.LeftButton)

    def test_13(self):
        QTest.mouseClick(self.gui._add_table_button, QtCore.Qt.LeftButton)

        QTest.keyClick(self.gui._add_table_window.line_edit_table_name, ' ')

        yes_button = QtWidgets.QDialogButtonBox.Ok
        QTest.mouseClick(self.gui._add_table_window.button_box.button(yes_button), QtCore.Qt.LeftButton)

        self.assertEqual('Table should only contain characters, numbers or _',
                         self.gui._add_table_window.line_edit_table_name.toolTip())

        QTest.mouseClick(self.gui._add_table_window.button_box.button(QtWidgets.QDialogButtonBox.Cancel),
                         QtCore.Qt.LeftButton)

    def test_14(self):
        QTest.mouseClick(self.gui._add_table_button, QtCore.Qt.LeftButton)

        for letter in 'table_name':
            QTest.keyClick(self.gui._add_table_window.line_edit_table_name, letter)

        yes_button = QtWidgets.QDialogButtonBox.Ok
        QTest.mouseClick(self.gui._add_table_window.button_box.button(yes_button), QtCore.Qt.LeftButton)

        self.assertEqual('Column names should not be empty',
                         self.gui._add_table_window.columns_table.item(0, 0).toolTip())

        QTest.mouseClick(self.gui._add_table_window.button_box.button(QtWidgets.QDialogButtonBox.Cancel),
                         QtCore.Qt.LeftButton)

    def test_15(self):
        QTest.mouseClick(self.gui._add_table_button, QtCore.Qt.LeftButton)

        for letter in 'table_name':
            QTest.keyClick(self.gui._add_table_window.line_edit_table_name, letter)
        self.gui._add_table_window.columns_table.item(0, 0).setText('    ')

        yes_button = QtWidgets.QDialogButtonBox.Ok
        QTest.mouseClick(self.gui._add_table_window.button_box.button(yes_button), QtCore.Qt.LeftButton)

        self.assertEqual('Column names should not be empty',
                         self.gui._add_table_window.columns_table.item(0, 0).toolTip())

        QTest.mouseClick(self.gui._add_table_window.button_box.button(QtWidgets.QDialogButtonBox.Cancel),
                         QtCore.Qt.LeftButton)

    def test_16(self):
        self.gui._load_table(0)
        self.add_row(['6', 'ddd', 'DDD', '1.72'])
        self.add_row(['7', 'eee', 'EEE', '1.78'])
        self.add_row(['8', 'fff', 'FFF', '1.86'])
        self.add_row(['9', 'ggg', 'GGG', '1.67'])
        self.add_row(['10', 'hhh', 'HHH', '1.79'])
        QTest.mouseClick(self.gui._confirm_changes_button, QtCore.Qt.LeftButton)

        self.gui._query_line_edit.setText("lambda row: row['ID'] % 2 == 0 and row['wzrost'] >= 1.8")
        QTest.mouseClick(self.gui._filter_button, QtCore.Qt.LeftButton)

        gui_data = {
            int(self.gui._data_table.verticalHeaderItem(row).text()): [
                self.gui._data_table.item(row, col).text()
                for col
                in range(self.gui._data_table.columnCount())
            ]
            for row
            in range(self.gui._data_table.rowCount())
        }

        self.assertEqual({
            1: ['2', 'Ziemniaczysław', 'Bulwiasty', '1.91'],
            3: ['4', 'bbb', 'BBB', '1.8'],
            7: ['8', 'fff', 'FFF', '1.86']
        },
            gui_data)


if __name__ == '__main__':
    unittest.main()
