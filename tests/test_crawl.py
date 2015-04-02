import unittest

from crawl import Crawler
from test_common import MixinTestCase


class CrawlerTestCase(MixinTestCase):

    def setUp(self):
        self.connect_local_dynamodb()
        self.create_table('areas', 'arcode')

    def tearDown(self):
        self.delete_table()

    def test_crawl_arcodes(self):
        crawler = Crawler()
        count = crawler.crawl_arcodes(limit=10, connection=self.conn)
        self.assertEqual(count, 10)


if __name__ == '__main__':
    unittest.main()
