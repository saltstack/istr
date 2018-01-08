# -*- coding: utf-8 -*-
'''
    tests.conftest
    ~~~~~~~~~~~~~~
'''

# Import python libs
import os
import sys

CODE_ROOT = os.path.join(
    os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
    'src'
)
if CODE_ROOT in sys.path:
    sys.path.remove(CODE_ROOT)
sys.path.insert(0, CODE_ROOT)
