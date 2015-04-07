import unittest
import os
import json
import logging

from boto.dynamodb2.layer1 import DynamoDBConnection
from boto.dynamodb2.table import Table
from boto.dynamodb2.fields import HashKey
from boto.dynamodb2.types import NUMBER
from boto.s3.connection import S3Connection, OrdinaryCallingFormat

from settings import S3_BUCKET_NAME

logger = logging.getLogger(__name__)


class MixinTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(MixinTestCase, self).__init__(*args, **kwargs)
        self.tables = dict()

    def connect_local_dynamodb(self):
        self.conn = DynamoDBConnection(
            host='localhost',
            port=8010,
            aws_access_key_id='anything',
            aws_secret_access_key='anything',
            is_secure=False)

    def connect_local_s3(self):
        self.s3_conn = S3Connection('anything', 'anything', is_secure=False, port=4567, host='localhost', calling_format=OrdinaryCallingFormat())

    def create_bucket(self):
        self.s3_conn.create_bucket(S3_BUCKET_NAME)

    def delete_bucket(self):
        bucket = self.s3_conn.get_bucket(S3_BUCKET_NAME)
        for key in bucket.list():
            key.delete()
        self.s3_conn.delete_bucket(S3_BUCKET_NAME)

    def create_table(self, table_name, hashkey_name):
        logger.debug("creating table : table_name=%s, hashkey_name=%s", table_name, hashkey_name)
        if table_name in self.conn.list_tables()["TableNames"]:
            Table(table_name, connection=self.conn).delete()
        table = Table.create(table_name, schema=[HashKey(hashkey_name, data_type=NUMBER)], connection=self.conn)
        self.tables[table_name] = table

    def delete_tables(self):
        for table_name in self.conn.list_tables()["TableNames"]:
            Table(table_name, connection=self.conn).delete()

    def load_fixtures(self, table_name):
        fixture_name = 'tests/fixtures/%s.json' % table_name
        if os.path.isfile(fixture_name):
            with open(fixture_name) as f:
                rs = json.loads(f.read())
        for r in rs:
            self.tables[table_name].put_item(data=r)
