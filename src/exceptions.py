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
