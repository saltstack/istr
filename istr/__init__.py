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
__version__ = '0.9.0'
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
                self.__normalized = unicodedata.normalize('NFKD',
                                                          text.casefold())
        return self.__normalized

    def __repr__(self):
        return 'istr({})'.format(super().__repr__())

    def __eq__(self, other):
        if not isinstance(other, istr):
            other = istr(other)
        return self.normalized == other.normalized

    def __lt__(self, other):
        if not isinstance(other, istr):
            other = istr(other)
        return self.normalized < other.normalized

    def __le__(self, other):
        if not isinstance(other, istr):
            other = istr(other)
        return self.normalized <= other.normalized

    def __gt__(self, other):
        if not isinstance(other, istr):
            other = istr(other)
        return self.normalized > other.normalized

    def __ne__(self, other):
        if not isinstance(other, istr):
            other = istr(other)
        return self.normalized != other.normalized

    def __ge__(self, other):
        if not isinstance(other, istr):
            other = istr(other)
        return self.normalized >= other.normalized

    def __hash__(self):
        return hash(self.normalized)

    def __contains__(self, other):
        if not isinstance(other, istr):
            other = istr(other)
        return other.normalized in self.normalized

    def count(self, other, *args):  # pylint: disable=arguments-differ
        if not isinstance(other, istr):
            other = istr(other)
        return str.count(self.normalized, other.normalized, *args)

    def endswith(self, other, *args):
        if not isinstance(other, istr):
            other = istr(other)
        return str.endswith(self.normalized, other.normalized, *args)

    def find(self, other, *args):  # pylint: disable=arguments-differ
        if not isinstance(other, istr):
            other = istr(other)
        return str.find(self.normalized, other.normalized, *args)

    def index(self, other, *args):  # pylint: disable=arguments-differ
        if not isinstance(other, istr):
            other = istr(other)
        return str.index(self.normalized, other.normalized, *args)

    def rfind(self, other, *args):
        if not isinstance(other, istr):
            other = istr(other)
        return str.rfind(self.normalized, other.normalized, *args)

    def rindex(self, other, *args):
        if not isinstance(other, istr):
            other = istr(other)
        return str.rindex(self.normalized, other.normalized, *args)

    def startswith(self, other, *args):
        if not isinstance(other, istr):
            other = istr(other)
        return str.startswith(self.normalized, other.normalized, *args)

    def casefold(self):
        return self.normalized.casefold()
