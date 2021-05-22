from db.data_types import Type
from db.exceptions import RecordIndexError


class Table:
    def __init__(self, columns: dict, records: list[list] = None):
        self.column_names: list[str] = list(columns.keys())
        self.column_types: list[Type] = list(columns.values())
        self.data = []

        if records:
            self.batch_insert(records)

        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.i < len(self.data):
            record = self.data[self.i]
            self.i += 1
            return record

        self.i = 0
        raise StopIteration

    def insert(self, record: list):
        for value, expected_type in zip(record, self.column_types):
            expected_type.validate(value)

        self.data.append(record)

    def batch_insert(self, records: list[list]):
        for record in records:
            for value, expected_type in zip(record, self.column_types):
                expected_type.validate(value)

        self.data.extend(records)

    def delete(self, index):
        try:
            del self.data[index]
        except IndexError:
            raise RecordIndexError(index)

    def save(self, filename):
        with open(filename, 'w') as f:
            for column_name in self.column_names:
                f.write(f'{column_name} ')
            f.write('\n')

            for column_type in self.column_types:
                f.write(f'{column_type} ')
            f.write('\n')

            for record in self.data:
                for value in record:
                    f.write(f'{repr(value)} ')
                f.write('\n')

    def __repr__(self):
        return str(self.data)