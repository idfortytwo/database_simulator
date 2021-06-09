class Error(Exception):
    """Project exceptions base class"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class NoSuchTableError(Error):
    def __init__(self, table_name: str):
        self.message = f'no such table: {table_name}'


class RecordIndexError(Error):
    def __init__(self, index: int):
        self.message = f'no record at index {index}'


class InvalidTypeError(Error):
    # noinspection PyUnresolvedReferences
    def __init__(self, value: int, data_type: 'DataType'):
        self.message = f'{value} is not {data_type}'


class DuplicateColumnNameError(Error):
    def __init__(self, row_index: int):
        self.row_index = row_index
        self.message = f'duplicate column name at row {row_index}'


class EmptyColumnNameError(Error):
    def __init__(self, row_index: int):
        self.row_index = row_index
        self.message = f'empty column name at row {row_index}'


class IllegalColumnNameError(Error):
    def __init__(self, row_index: int):
        self.row_index = row_index
        self.message = f'illegal characters in column name at row {row_index}'


class EmptyTableNameError(Error):
    def __init__(self):
        self.message = f'empty table name'


class IllegalTableNameError(Error):
    def __init__(self):
        self.message = f'illegal characters in table name'


class ColumnNotFoundError(Error):
    def __init__(self, column_name: int, table_name: str):
        self.column_name = column_name
        self.table_name = table_name
        self.message = f'no such column in table {table_name}: {column_name}'


class ConversionError(Error):
    # noinspection PyUnresolvedReferences
    def __init__(self, value: any, data_type: 'DataType'):
        self.value = value
        self.data_type = data_type
        self.message = f'failed to convert "{value}" to {data_type}'


class CellDataConversionError(ConversionError):
    # noinspection PyUnresolvedReferences
    def __init__(self, col: int, row: int, value: any, data_type: 'DataType'):
        super().__init__(value, data_type)
        self.col = col
        self.row = row
        self.message = f'failed to convert "{value}" to {data_type} at cell {col}:{row}'