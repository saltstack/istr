# -*- coding: utf-8 -*-
'''
    tests.conftest
    ~~~~~~~~~~~~~~
'''

# Import python libs
import os
import sys

CODE_ROOT = os.path.dirname(os.path.dirname(__file__))
if CODE_ROOT in sys.path:
    sys.path.remove(CODE_ROOT)
sys.path.insert(0, CODE_ROOT)
