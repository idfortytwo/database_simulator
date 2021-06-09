from typing import Union

from db.data_types import DataType
from exceptions.exceptions import RecordIndexError


class Table:
    def __init__(self, columns: dict, records: list[list] = None):
        self.column_names: list[str] = list(columns.keys())
        self.column_types: list[DataType] = list(columns.values())
        self.data: dict[int: Union[int, float, str]] = {}
        self.record_id_sequence = 0

        if records:
            self.batch_insert(records)

        self.i = 0

    def __iter__(self):
        return self

    def __next__(self) -> list:
        if self.i < len(self.data):
            record = self.data[self.i]
            self.i += 1
            return record

        self.i = 0
        raise StopIteration

    def get_columns(self) -> dict[str: DataType]:
        return dict(zip(self.column_names, self.column_types))

    def insert(self, record: list) -> None:
        for value, expected_type in zip(record, self.column_types):
            expected_type.validate(value)

        self.data[self.record_id_sequence] = record
        self.record_id_sequence += 1

    def batch_insert(self, records: list[list]) -> None:
        for record in records:
            for value, expected_type in zip(record, self.column_types):
                expected_type.validate(value)

        for record in records:
            self.data[self.record_id_sequence] = record
            self.record_id_sequence += 1

    def delete(self, record_id: int) -> None:
        try:
            del self.data[record_id]
        except IndexError:
            raise RecordIndexError(record_id)

    def __repr__(self) -> str:
        return str(self.data)