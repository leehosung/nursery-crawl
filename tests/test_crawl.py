import unittest
import sys
sys.path.insert(0, '..')
import os
from crawl import *
from tinydb import TinyDB, where


class CrawlTestCase(unittest.TestCase):

    def test_crawl_arcodes(self):
        db_filename = "test.json"
        os.remove(db_filename)

        crawl_arcodes(db_filename)
        db = TinyDB(db_filename)
        table = db.table("arcodes")
        self.assertTrue(len(table.search(where('arcode') == '11110')) > 0)

    def test_crawl_nurseries_in_area(self):
        crawl_nurseries_in_area("11110")


class NurseryTestCase(unittest.TestCase):

    def test_get_summary(self):
        n = Nursery(11110000156)
        n.get_summary()
        self.assertEqual(n.name, "GS건설 꿈과 희망의 어린이집")
        self.assertEqual(n.address, "서울특별시 종로구 종로 33 그랑서울 2층")
        self.assertEqual(n.zip_code, "110-130")
        self.assertEqual(n.type, "직장")

    def test_fail_get_coordination(self):
        n = Nursery(11110000054)
        n.get_summary()


if __name__ == '__main__':
    unittest.main()
