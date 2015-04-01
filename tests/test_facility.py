import unittest
from datetime import datetime
import os
from facility import *


class FacilityTestCase(unittest.TestCase):

    def test_crawl_facilities(self):
        facilities = [x for x in Facility.crawl_facilities(limit=10)]
        for f in facilities:
            if f.facility_name == "새싹어린이집":
                break
        else:
            self.fail()

    def test_crawl_facility_info(self):
        f = Facility(11215000106)
        f.crawl_facility_info()
        self.assertEqual("새싹어린이집", f.facility_name)
        self.assertEqual("민간개인", f.cr_type)
        self.assertEqual("일반", f.cr_spec)
        self.assertTrue(hasattr(f, "fixed_number"))
        self.assertTrue(hasattr(f, "present_number"))
        self.assertEqual("박현정", f.president_name)
        self.assertEqual(datetime(2001, 5, 21), f.open_date)
        self.assertEqual(True, f.vehicle)
        self.assertEqual("02-457-7702", f.telephone)
        self.assertEqual("서울 광진구 자양2동 682-4 1층", f.address)
        self.assertEqual(False, f.gov_support)
        self.assertEqual(True, f.accident_insurance)
        self.assertEqual(True, f.fire_insurance)
        self.assertEqual(True, f.compensation_insurance)

        self.assertEqual({
            "0": 383300,
            "1": 337700,
            "2": 278000,
            "3": 243000,
            "4": 238000,
            "5over": 238000
        }, f.prices)

        self.assertEqual({
            "0": 1,
            "1": 0,
            "2": 2,
            "3": 0,
            "4": 0,
            "5over": 0
        }, f.waitings)

        self.assertEqual(0, f.reserv_confirm)
        self.assertEqual(0, f.reserv_wait)
        self.assertEqual(0, f.reserv_remain)
        self.assertEqual(0, f.reserv_regular)

        self.assertEqual(5, len(f.photos))


if __name__ == '__main__':
    unittest.main()
