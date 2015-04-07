import argparse
import decimal
import json
import logging
import logging.config
import os
import sys

import boto
from boto.s3.key import Key

from area import Area
from facility import Nursery
from exceptions import APILimitError
from settings import S3_BUCKET_NAME, NURSERY_FILE_PATH

logger = logging.getLogger("nursery-crawl")


def setup_logging(
    default_path='logging.json',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """Setup logging configuration"""
    value = os.getenv(env_key, None)
    path = default_path if not value else value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            f = float(o)
            if f%1 != 0:
                return f
            else:
                return int(f)
        return super(DecimalEncoder, self).default(o)


class Crawler(object):

    def __init__(self):
        setup_logging()

    def crawl_arcodes(self, limit=sys.maxsize, dynamo_conn=None):
        count = 0
        for area in Area.crawl_areas():
            if count >= limit:
                break
            area.save(dynamo_conn)
            count += 1
        logger.info("%d areas are crawled" % count)
        return count

    def crawl_nurseries(self, limit=sys.maxsize, dynamo_conn=None):
        count = 0
        for nursery in Nursery.crawl_facilities():
            if count >= limit:
                break
            nursery.save(dynamo_conn)
            count += 1
        logger.info("%d nurseries are crawled" % count)
        return count

    def crawl_nursery_details(self, limit=sys.maxsize, dynamo_conn=None):
        count = 0
        rs = Nursery.get_all_facilities(dynamo_conn)
        rs = sorted(rs, key=lambda nursery: nursery.get("detail_updated", ""))
        for r in rs:
            if count >= limit:
                break
            try:
                nursery = Nursery(r["facility_id"])
                nursery.crawl_facility_info()
                nursery.save(dynamo_conn)
            except APILimitError as e:
                logger.error(e)
                break
            count += 1
        logger.info("%d nursery details are crawled" % count)
        return count

    def update_s3(self, dynamo_conn=None, s3_conn=None):
        rs = Nursery.get_all_facilities(dynamo_conn)
        rs = [x.__dict__["_data"] for x in rs]
        json_str = json.dumps(rs, cls=DecimalEncoder)
        count = len(rs)
        if s3_conn is None:
            s3_conn = boto.connect_s3()
        b = s3_conn.get_bucket(S3_BUCKET_NAME)
        k = Key(b)
        k.key = NURSERY_FILE_PATH
        k.set_contents_from_string(json_str)
        logger.info("%d nurseries are uploaded to S3" % count)
        return count

def parse():
    parser = argparse.ArgumentParser(description="Crawl nurseries")
    parser.add_argument(
        '--arcode', action='store_const', const=True,
        default=False, help='crawl area codes'
    )
    parser.add_argument(
        '--nursery', action='store_const', const=True,
        default=False, help='crawl nurseries'
    )
    parser.add_argument(
        '--nursery_detail', action='store_const', const=True,
        default=False, help='crawl nursery details'
    )
    parser.add_argument(
        '--limit', default=sys.maxsize, type=int, help='crawl limit count'
    )
    parser.add_argument(
        '--s3', action='store_const', const=True,
        default=False, help='update nursey info in S3'
    )
    return parser.parse_args()


if __name__ == '__main__':
    crawler = Crawler()
    args = parse()
    if args.arcode:
        crawler.crawl_arcodes(limit=args.limit)
    if args.nursery:
        crawler.crawl_nurseries(limit=args.limit)
    if args.nursery_detail:
        crawler.crawl_nursery_details(limit=args.limit)
    if args.s3:
        crawler.update_s3()
