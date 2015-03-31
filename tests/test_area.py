import unittest
import sys
sys.path.insert(0, '..')
import os
from area import *


class AreaTestCase(unittest.TestCase):

    def test_crawl_arcodes(self):
        for area in Area.crawl_areas():
            print(area)


if __name__ == '__main__':
    unittest.main()
