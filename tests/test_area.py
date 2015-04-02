import unittest

from boto.dynamodb2.layer1 import DynamoDBConnection
from boto.dynamodb2.table import Table
from boto.dynamodb2.fields import HashKey
from boto.dynamodb2.types import NUMBER

from area import Area

class AreaTestCase(unittest.TestCase):

    def setUp(self):
        self.conn = DynamoDBConnection(
            host='localhost',
            port=8010,
            aws_access_key_id='unittest',
            aws_secret_access_key='unittest',
            is_secure=False
        )
        if 'areas' in self.conn.list_tables()["TableNames"]:
            Table('areas', connection=self.conn).delete()
        self.table = Table.create('areas', schema=[HashKey('arcode', data_type=NUMBER)], connection=self.conn)

    def tearDown(self):
        self.table.delete()

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
        received_area = self.table.get_item(arcode=11305)
        self.assertEqual(area.sigunname, received_area['sigunname'])


if __name__ == '__main__':
    unittest.main()
