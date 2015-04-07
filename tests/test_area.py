import unittest

from area import Area
from test_common import MixinTestCase


class AreaTestCase(MixinTestCase):

    def setUp(self):
        self.connect_local_dynamodb()
        self.create_table('area', 'arcode')

    def tearDown(self):
        self.delete_tables()

    def test_crawl_arcode(self):
        rs = Area.crawl_area('제주도')
        self.assertEqual(2, len(rs))

    def test_crawl_arcodes(self):
        count = 0
        for area in Area.crawl_areas():
            if area == Area('서울특별시', '강북구', 11305):
                break
            if count == 10:
                self.fail()
            else:
                count += 1
        else:
            self.fail()

    def test_save(self):
        area = Area('서울특별시', '강북구', 11305)
        area.save(connection=self.conn)
        received_area = self.tables['area'].get_item(arcode=11305)
        self.assertEqual(area.sigunname, received_area['sigunname'])


if __name__ == '__main__':
    unittest.main()
