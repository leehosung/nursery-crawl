import argparse
import json
import logging.config
import os

from area import Area


class NotFound(Exception):
    pass


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

    def crawl_arcodes(self, limit=None, connection=None):
        count = 0
        for area in Area.crawl_areas():
            if limit is not None and count >= limit:
                break
            area.save(connection)
            count += 1
        return count


def parse():
    parser = argparse.ArgumentParser(description="Crawl nurseries")
    parser.add_argument(
        '--arcode', action='store_const', const=True,
        default=False, help='crawl area codes'
    )
    return parser.parse_args()


if __name__ == '__main__':
    crawler = Crawler()
    args = parse()
    if args.arcode:
        crawler.crawl_arcodes()
