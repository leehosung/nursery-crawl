import unittest
import sys
sys.path.insert(0, '..')
import os
from childcare_service_api import *


class ChildcareServiceApiTestCase(unittest.TestCase):

    def test_get_child_facility_item(self):
        api = ChildcareServiceApi()
        api.get_child_facility_item(11110000042)


if __name__ == '__main__':
    unittest.main()
