import unittest

from boto.dynamodb2.layer1 import DynamoDBConnection
from boto.dynamodb2.table import Table
from boto.dynamodb2.fields import HashKey
from boto.dynamodb2.types import NUMBER


class MixinTestCase(unittest.TestCase):

    def connect_local_dynamodb(self):
        self.conn = DynamoDBConnection(
            host='localhost',
            port=8010,
            aws_access_key_id='anything',
            aws_secret_access_key='anything',
            is_secure=False)

    def create_table(self, table_name, hashkey_name):
        if table_name in self.conn.list_tables()["TableNames"]:
            Table(table_name, connection=self.conn).delete()
        self.table = Table.create(table_name, schema=[HashKey(hashkey_name, data_type=NUMBER)], connection=self.conn)

    def delete_table(self):
        self.table.delete()
