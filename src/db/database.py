import pickle

from db.exceptions import NoSuchTableError
from db.table import Table


class Database:
    def __init__(self):
        self.filename = None
        self.tables = {}

    def add_table(self, table: Table, table_name: str):
        self.tables[table_name] = table

    def get_table(self, table_name: str) -> Table:
        try:
            return self.tables[table_name]
        except KeyError:
            raise NoSuchTableError(table_name)

    def get_table_names(self):
        return list(self.tables.keys())

    def drop_table(self, table_name: str):
        try:
            self.tables.pop(table_name)
        except KeyError:
            raise NoSuchTableError(table_name)

    def to_dict(self) -> dict:
        return {
            'tables': {**self.tables}
        }

    def save(self, filename=None):
        with open(filename or self.filename, 'wb') as f:
            pickle.dump(self.to_dict(), f)

    def load(self, filename):
        with open(filename, 'rb') as f:
            unpickled = pickle.load(f)
            self.tables = unpickled['tables']
            self.filename = filename

    def show(self):
        for table_name, table_data in self.tables.items():
            print(f'{table_name}:')
            for record in table_data:
                print(record)
            print('')