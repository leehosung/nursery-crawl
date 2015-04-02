import unittest
from area import Area


class AreaTestCase(unittest.TestCase):

    def test_crawl_arcodes(self):
        areas = [x for x in Area.crawl_areas()]
        self.assertIn(Area('경상남도', '진주시', 48170), areas)


if __name__ == '__main__':
    unittest.main()
