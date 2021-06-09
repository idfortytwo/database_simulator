from abc import ABC, abstractmethod

from exceptions.exceptions import InvalidTypeError, ConversionError


class DataType(ABC):
    """Database data type abstract base class"""
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
        """Raises exception if value is not a valid integer"""
        if not isinstance(value, int):
            raise InvalidTypeError(value, 'integer')

    def convert(self, value: any) -> int:
        """Converts a value to integer"""
        try:
            return int(value)
        except ValueError:
            raise ConversionError(value, self)

    def __str__(self):
        return 'Integer'


class _Float(DataType):
    @staticmethod
    def validate(value: any):
        """Raises exception if value is not a valid float"""
        if not isinstance(value, float) and not isinstance(value, int):
            raise InvalidTypeError(value, 'float')

    def convert(self, value: any) -> float:
        """Converts a value to float"""
        try:
            return float(value)
        except ValueError:
            raise ConversionError(value, self)

    def __str__(self):
        return 'Float'


class _Text(DataType):
    @staticmethod
    def validate(value):
        """Raises exception if value is not a valid text"""
        if not isinstance(value, str):
            raise InvalidTypeError(value, 'text')

    def convert(self, value: any) -> str:
        """Converts a value to text"""
        try:
            return str(value)
        except ValueError:
            raise ConversionError(value, self)

    def __str__(self):
        return 'Text'


Integer = _Integer()
Float = _Float()
Text = _Text()