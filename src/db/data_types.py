from abc import ABC, abstractmethod

from exceptions.exceptions import InvalidTypeError


class DataType(ABC):
    @staticmethod
    @abstractmethod
    def validate(value):
        pass

    @staticmethod
    @abstractmethod
    def convert(value):
        pass

    @abstractmethod
    def __str__(self):
        pass


class _Integer(DataType):
    @staticmethod
    def validate(value):
        if not isinstance(value, int):
            raise InvalidTypeError(value, 'integer')

    @staticmethod
    def convert(value):
        return int(value)

    def __str__(self):
        return 'Integer'


class _Float(DataType):
    @staticmethod
    def validate(value):
        if not isinstance(value, float) and not isinstance(value, int):
            raise InvalidTypeError(value, 'float')

    @staticmethod
    def convert(value):
        return float(value)

    def __str__(self):
        return 'Float'


class _Text(DataType):
    @staticmethod
    def validate(value):
        if not isinstance(value, str):
            raise InvalidTypeError(value, 'text')

    @staticmethod
    def convert(value):
        return str(value)

    def __str__(self):
        return 'Text'


Integer = _Integer()
Float = _Float()
Text = _Text()

# __all__ = ['Type', 'Integer', 'Float', 'Text', 'InvalidTypeError']