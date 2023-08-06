import sys
from string import Template
from .type import language


class Formatter:

    def __init__(self, string: str, __values: dict):
        if len(__values.keys()) <= 0:
            raise ValueError("Values cannot be empty")
        self.data = Template(string).safe_substitute(**__values)


class TranslatedString:

    def __init__(
            self,
            string: str | Formatter,
            _language: language,
            _file: str,
            _key: str,
    ):
        self.string: str = string if isinstance(string, str) else string.data
        self.language = _language
        self.file = _file
        self.key = _key

    def __str__(self):
        return self.string

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return len(self.string)

    def __getitem__(self, item):
        return self.string[item]

    def __iter__(self):
        return iter(self.string)

    def __contains__(self, item):
        return item in self.string

    def __add__(self, other):
        return self.string + other

    def __radd__(self, other):
        return other + self.string

    def __mul__(self, other):
        return self.string * other

    def __rmul__(self, other):
        return other * self.string

    def __eq__(self, other):
        return self.string == other

    def __ne__(self, other):
        return self.string != other

    def __lt__(self, other):
        return self.string < other

    def __le__(self, other):
        return self.string <= other

    def __gt__(self, other):
        return self.string > other

    def __ge__(self, other):
        return self.string >= other

    def __hash__(self):
        return hash(self.string)

    def __bool__(self):
        return bool(self.string)

    def __format__(self, format_spec):
        return self.string.format(format_spec)

    def __dir__(self):
        return dir(self.string)

    def __sizeof__(self):
        return sys.getsizeof(self.string)
