# -*- coding: utf-8 -*-
'''
    istr.py
    ~~~~~~~

    Case insensitive string implementation.

    Based on https://code.activestate.com/recipes/194371/ and
    https://stackoverflow.com/a/29247821/1258307
'''

# Metadata
__author__ = 'Pedro Algarvio'
__email__ = 'pedro@algarvio.me'
__version__ = '1.0.2'
__version_info__ = tuple(
    int(part) for part in __version__.split('.') if part.isdigit()
)

# Import python libs
import unicodedata


class istr(str):  # pylint: disable=invalid-name
    '''
    Case insensitive strings class.
    Performs like str except comparisons are case insensitive.
    '''

    @property
    def normalized(self):
        if not hasattr(self, '__normalized'):
            text = super().__str__()
            try:
                # Can it be decoded using ascii
                text.encode('ascii')
                self.__normalized = text.casefold()
            except UnicodeEncodeError:
                # Text contains characters not in the ascii range
                self.__normalized = unicodedata.normalize('NFKC',
                                                          text.casefold())
        return self.__normalized

    def __repr__(self):
        return 'istr({})'.format(super().__repr__())

    def __eq__(self, other):
        try:
            return self.normalized == self._normalize(other)
        except TypeError:
            return NotImplemented

    def __lt__(self, other):
        try:
            return self.normalized < self._normalize(other)
        except TypeError:
            return NotImplemented

    def __le__(self, other):
        try:
            return self.normalized <= self._normalize(other)
        except TypeError:
            return NotImplemented

    def __gt__(self, other):
        try:
            return self.normalized > self._normalize(other)
        except TypeError:
            return NotImplemented

    def __ne__(self, other):
        try:
            return self.normalized != self._normalize(other)
        except TypeError:
            return NotImplemented

    def __ge__(self, other):
        try:
            return self.normalized >= self._normalize(other)
        except TypeError:
            return NotImplemented

    def __hash__(self):
        return hash(self.normalized)

    def __contains__(self, other):
        return self._normalize(other) in self.normalized

    def count(self, other, *args):  # pylint: disable=arguments-differ
        return str.count(self.normalized, self._normalize(other), *args)

    def endswith(self, other, *args):
        return str.endswith(self.normalized, self._normalize(other), *args)

    def find(self, other, *args):  # pylint: disable=arguments-differ
        return str.find(self.normalized, self._normalize(other), *args)

    def index(self, other, *args):  # pylint: disable=arguments-differ
        return str.index(self.normalized, self._normalize(other), *args)

    def rfind(self, other, *args):
        return str.rfind(self.normalized, self._normalize(other), *args)

    def rindex(self, other, *args):
        return str.rindex(self.normalized, self._normalize(other), *args)

    def startswith(self, other, *args):
        return str.startswith(self.normalized, self._normalize(other), *args)

    def casefold(self):
        return self.normalized.casefold()

    def _normalize(self, obj):
        if isinstance(obj, istr):
            return obj.normalized
        if isinstance(obj, str):
            return self.__class__(obj).normalized
        raise TypeError(f"Argument must be str, not {type(obj)}")
