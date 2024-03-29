#!/usr/bin/env python 
import sys
sys.stdout = None
import unittest
from test_util import *
from test_table import *
from test_import import *
from test_differ import *
from test_engines import *
from test_fixtures import *
from test_plaintypes import *
from test_ColumnFixture import *
from test_RowFixture import *
from test_ActionFixture import *
from fitnesse.test_protocol import *
from fitnesse.test_client import *

if __name__ == '__main__':
    unittest.main()
