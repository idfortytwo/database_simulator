from abc import ABC, abstractmethod

from exceptions.exceptions import InvalidTypeError, ConversionError


class DataType(ABC):
    @staticmethod
    @abstractmethod
    def validate(value):
        pass

    @abstractmethod
    def convert(self, value):
        pass

    @abstractmethod
    def __str__(self):
        pass


class _Integer(DataType):
    @staticmethod
    def validate(value):
        if not isinstance(value, int):
            raise InvalidTypeError(value, 'integer')

    def convert(self, value):
        try:
            return int(value)
        except ValueError:
            raise ConversionError(value, self)

    def __str__(self):
        return 'Integer'


class _Float(DataType):
    @staticmethod
    def validate(value):
        if not isinstance(value, float) and not isinstance(value, int):
            raise InvalidTypeError(value, 'float')

    def convert(self, value):
        try:
            return float(value)
        except ValueError:
            raise ConversionError(value, self)

    def __str__(self):
        return 'Float'


class _Text(DataType):
    @staticmethod
    def validate(value):
        if not isinstance(value, str):
            raise InvalidTypeError(value, 'text')

    def convert(self, value):
        try:
            return str(value)
        except ValueError:
            raise ConversionError(value, self)

    def __str__(self):
        return 'Text'


Integer = _Integer()
Float = _Float()
Text = _Text()

# __all__ = ['Type', 'Integer', 'Float', 'Text', 'InvalidTypeError']