import argparse
import json
import logging
import logging.config
import os
import sys

from area import Area
from facility import Nursery
from exceptions import APILimitError

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


class Crawler(object):

    def __init__(self):
        setup_logging()

    def crawl_arcodes(self, limit=sys.maxsize, connection=None):
        count = 0
        for area in Area.crawl_areas():
            if count >= limit:
                break
            area.save(connection)
            count += 1
        logger.info("%d areas are crawled" % count)
        return count

    def crawl_nurseries(self, limit=sys.maxsize, connection=None):
        count = 0
        for nursery in Nursery.crawl_facilities():
            if count >= limit:
                break
            nursery.save(connection)
            count += 1
        logger.info("%d nurseries are crawled" % count)
        return count

    def crawl_nursery_details(self, limit=sys.maxsize, connection=None):
        count = 0
        rs = Nursery.get_all_facilities()
        rs = sorted(rs, key=lambda nursery: nursery.get("detail_updated", ""))
        for r in rs:
            if count >= limit:
                break
            try:
                nursery = Nursery(r["facility_id"])
                nursery.crawl_facility_info()
                nursery.save(connection)
            except APILimitError as e:
                logger.error(e)
                break
            count += 1
        logger.info("%d nursery details are crawled" % count)
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
