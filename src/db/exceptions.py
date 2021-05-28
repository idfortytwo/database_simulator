class Error(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class NoSuchTableError(Error):
    def __init__(self, table_name):
        self.message = f'no such table: {table_name}'


class RecordIndexError(Error):
    def __init__(self, index):
        self.message = f'no record at index {index}'


class InvalidTypeError(Error):
    def __init__(self, value, data_type):
        self.message = f'{value} is not {data_type}'


class DuplicateColumnNameError(Error):
    def __init__(self, row_index):
        self.row_index = row_index
        self.message = f'duplicate column name at row {row_index}'


class EmptyColumnNameError(Error):
    def __init__(self, row_index):
        self.row_index = row_index
        self.message = f'empty column name at row {row_index}'
