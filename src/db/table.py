from typing import Union

from db.data_types import DataType
from exceptions.exceptions import RecordIndexError


class Table:
    def __init__(self, columns: dict, records: list[list] = None):
        self._column_names: list[str] = list(columns.keys())
        self._column_types: list[DataType] = list(columns.values())
        self._data: dict[int: Union[int, float, str]] = {}
        self._record_id_sequence = 0

        if records:
            self.batch_insert(records)

        self.i = 0

    def __iter__(self):
        return self

    def __next__(self) -> list:
        if self.i < len(self._data):
            record = self._data[self.i]
            self.i += 1
            return record

        self.i = 0
        raise StopIteration

    def get_columns(self) -> dict[str: DataType]:
        """Returns dictionary of column names and data types"""
        return dict(zip(self._column_names, self._column_types))

    @property
    def column_names(self):
        return self._column_names

    @property
    def column_types(self):
        return self._column_types

    @property
    def data(self):
        return self._data

    def insert(self, record: list[Union[int, float, str]]) -> None:
        """Inserts new record into table"""
        for value, expected_type in zip(record, self._column_types):
            expected_type.validate(value)

        self._data[self._record_id_sequence] = record
        self._record_id_sequence += 1

    def batch_insert(self, records: list[list[Union[int, float, str]]]) -> None:
        """Inserts list of records into table"""
        for record in records:
            for value, expected_type in zip(record, self._column_types):
                expected_type.validate(value)

        for record in records:
            self._data[self._record_id_sequence] = record
            self._record_id_sequence += 1

    def delete(self, record_id: int) -> None:
        """Deletes a record of given id"""
        try:
            del self._data[record_id]
        except IndexError:
            raise RecordIndexError(record_id)

    def __repr__(self) -> str:
        return str(self._data)