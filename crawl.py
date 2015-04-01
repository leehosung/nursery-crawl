import argparse
import json
import logging.config
from settings import *


class NotFound(Exception):
    pass


def setup_logging(default_path='logging.json', default_level=logging.INFO, env_key='LOG_CFG'):
    """Setup logging configuration"""
    value = os.getenv(env_key, None)
    path = defaut_path if not value else value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)



class Crawler(object):

    def __init__(self):
        setup_logging()

    def crawl_arcodes(self, db_filename=DB_FILENAME):
        for arname in ARNAMES:
           rs = self._crawl_arcode(arname)
           for r in rs:
                print(rs)

    def _crawl_arcode(self, arname):
        uri = "http://api.childcare.go.kr/mediate/rest/cpmsapi020/cpmsapi020/request?key=%s&arname=%s" % (API020_KEY, arname)
        rs = xmltodict.parse(requests.get(uri).text)['response']['item']
        self.logger.debug("%d area are crawled with %s" % (len(rs), arname))
        return rs

    def crawl_nurseries(self, db_filename=DB_FILENAME):
        db = TinyDB(db_filename)
        area_table = db.table("area")
        nursery_table = db.table("nursery")
        for area in area_table.all():
            ns = crawl_nurseries_in_area(area)
            for n in ns:
                nursery_table.insert(n.__dict__)

    def crawl_nurseries_in_area(self, area, max_tolerance=20):
        index = 0
        tolerance = 0
        nurseries = []
        while True:
            stcode = "%s%06d" % (area["arcode"], index)
            n = Nursery(stcode)
            try:
                n.get_summary()
            except NotFound:
                tolerance += 1
                if tolerance > max_tolerance:
                    break
            except Exception:
                print("Can't get summary : %s" % stcode)
                raise
            else:
                tolerance = 0
                nurseries.append(n)
            index += 1
        self.logger.debug("%d nurseries are crawled in %s/%s" % (len(nurseries), area["sidoname"], area["sigunname"]))
        return nurseries

def parse():
    parser = argparse.ArgumentParser(description="Crawl nurseries")
    parser.add_argument('--arcode', action='store_const', const=True, default=False, help='crawl area codes')
    return parser.parse_args()


if __name__ == '__main__':
    crawler = Crawler()
    args = parse()
    if args.arcode:
        crawler.crawl_arcodes()

