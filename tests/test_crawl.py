import unittest

from crawl import Crawler
from test_common import MixinTestCase


class CrawlerTestCase(MixinTestCase):

    def setUp(self):
        self.crawler = Crawler()
        self.connect_local_dynamodb()
        self.create_table('area', 'arcode')
        self.create_table('nursery', 'facility_id')

    def tearDown(self):
        self.delete_tables()

    def test_crawl_arcodes(self):
        count = self.crawler.crawl_arcodes(limit=5, connection=self.conn)
        self.assertEqual(count, 5)

    def test_crawl_nurseries(self):
        count = self.crawler.crawl_nurseries(limit=5, connection=self.conn)
        self.assertEqual(count, 5)

    def test_crawl_nursery_details(self):
        count = self.crawler.crawl_nursery_details(limit=5, connection=self.conn)
        self.assertEqual(count, 5)


if __name__ == '__main__':
    unittest.main()
