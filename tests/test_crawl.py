import unittest

from crawl import Crawler
from test_common import MixinTestCase


class CrawlerTestCase(MixinTestCase):

    def setUp(self):
        self.crawler = Crawler()
        self.connect_local_dynamodb()
        self.create_table('area', 'arcode')
        self.create_table('nursery', 'facility_id')
        self.connect_local_s3()
        self.create_bucket()

    def tearDown(self):
        self.delete_tables()
        self.delete_bucket()

    def test_crawl_arcodes(self):
        count = self.crawler.crawl_arcodes(limit=3, dynamo_conn=self.conn)
        self.assertEqual(count, 3)

    def test_crawl_nurseries(self):
        count = self.crawler.crawl_nurseries(limit=3, dynamo_conn=self.conn)
        self.assertEqual(count, 3)

    def test_crawl_nursery_details(self):
        self.load_fixtures("nursery")
        count = self.crawler.crawl_nursery_details(limit=3, dynamo_conn=self.conn)
        self.assertEqual(count, 3)

    def test_update_s3(self):
        self.load_fixtures("nursery")
        count = self.crawler.update_s3(dynamo_conn=self.conn, s3_conn=self.s3_conn)
        self.assertEqual(count, 10)


if __name__ == '__main__':
    unittest.main()
