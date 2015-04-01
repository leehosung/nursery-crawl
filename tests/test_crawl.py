import unittest
from crawl import Crawler


class CrawlerTestCase(unittest.TestCase):

    def test_crawl_arcodes(self):
        crawler = Crawler()
        crawler.crawl_arcodes()


if __name__ == '__main__':
    unittest.main()
