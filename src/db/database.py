import pickle

from exceptions.exceptions import NoSuchTableError
from db.table import Table


class Database:
    def __init__(self):
        self.filename = None
        self.tables: dict[str, Table] = {}

    def add_table(self, table: Table, table_name: str) -> None:
        """Adds a table of given name to database"""
        self.tables[table_name] = table

    def get_table(self, table_name: str) -> Table:
        """Returns a table of given name"""
        try:
            return self.tables[table_name]
        except KeyError:
            raise NoSuchTableError(table_name)

    def get_table_names(self) -> list[str]:
        """Returns list of names of tables in database"""
        return list(self.tables.keys())

    def drop_table(self, table_name: str) -> None:
        """Removes a table of given name from database"""
        try:
            self.tables.pop(table_name)
        except KeyError:
            raise NoSuchTableError(table_name)

    def to_dict(self) -> dict[str: list]:
        """Returns tables data as dict"""
        return {
            'tables': {**self.tables}
        }

    def save(self, filename: str = None) -> None:
        """Serializes database to a file"""
        with open(filename or self.filename, 'wb') as f:
            pickle.dump(self.to_dict(), f)

    def load(self, filename: str) -> None:
        """Deserializes database from a file"""
        with open(filename, 'rb') as f:
            unpickled = pickle.load(f)
            self.tables = unpickled['tables']
            self.filename = filename

    def show(self) -> None:
        """Prints database data"""
        for table_name, table_data in self.tables.items():
            print(f'{table_name}:')
            for record in table_data.data.values():
                print(record)
            print('')