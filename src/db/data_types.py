from abc import ABC, abstractmethod

from db.exceptions import InvalidTypeError


class Type(ABC):
    @staticmethod
    @abstractmethod
    def validate(value):
        pass

    @abstractmethod
    def __str__(self):
        pass


class Integer(Type):
    @staticmethod
    def validate(value):
        if not isinstance(value, int):
            raise InvalidTypeError(value, 'integer')

    def __str__(self):
        return 'Integer'


class Float(Type):
    @staticmethod
    def validate(value):
        if not isinstance(value, float) and not isinstance(value, int):
            raise InvalidTypeError(value, 'float')

    def __str__(self):
        return 'Float'


class Text(Type):
    @staticmethod
    def validate(value):
        if not isinstance(value, str):
            raise InvalidTypeError(value, 'text')

    def __str__(self):
        return 'Text'


# __all__ = ['Type', 'Integer', 'Float', 'Text', 'InvalidTypeError']