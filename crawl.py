import requests
import xmltodict
import logging
import os
import json
import logging.handlers
from settings import *

from tinydb import TinyDB, where

from bs4 import BeautifulSoup


logger = logging.getLogger('nursery')
logger.setLevel(min(CONSOLE_LOG_LEVEL, FILE_LOG_LEVEL))
formatter = logging.Formatter(LOG_FORMAT)

ch = logging.StreamHandler()
ch.setLevel(CONSOLE_LOG_LEVEL)
ch.setFormatter(formatter)
logger.addHandler(ch)

fh = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=10*1024*1024, backupCount=5)
fh.setLevel(FILE_LOG_LEVEL)
fh.setFormatter(formatter)
logger.addHandler(fh)


class NotFound(Exception):
    pass


def crawl_arcodes(db_filename=DB_FILENAME):
    db = TinyDB(db_filename)
    table = db.table("area")
    for arname in ARNAMES:
       rs = crawl_arcode(arname)
       for r in rs:
           table.insert(r)


def crawl_arcode(arname):
    uri = "http://api.childcare.go.kr/mediate/rest/cpmsapi020/cpmsapi020/request?key=%s&arname=%s" % (API020_KEY, arname)
    rs = xmltodict.parse(requests.get(uri).text)['response']['item']
    logger.debug("%d area are crawled with %s" % (len(rs), arname))
    return rs


def crawl_nurseries(db_filename=DB_FILENAME):
    db = TinyDB(db_filename)
    area_table = db.table("area")
    nursery_table = db.table("nursery")
    for area in area_table.all():
        ns = crawl_nurseries_in_area(area)
        for n in ns:
            nursery_table.insert(n.__dict__)

def crawl_nurseries_in_area(area, max_tolerance=20):
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
    logger.debug("%d nurseries are crawled in %s/%s" % (len(nurseries), area["sidoname"], area["sigunname"]))
    return nurseries

class Nursery(object):

    def __init__(self, stcode):
        self.stcode = stcode

    def get_summary(self):
        uri = "http://info.childcare.go.kr/info/pnis/search/preview/SummaryInfoSlPu.jsp?flag=YJ&STCODE_POP=%s" % self.stcode
        response = requests.get(uri)
        soup = BeautifulSoup(response.text)
        self.name = soup.find("p", {"class": "mainTitle"}).text
        if self.name == "":
            raise NotFound
        taL = soup.find("td", {"class": "taL"}).text.strip()
        ts = taL.split("\n")
        self.zip_code = ts[0].strip().replace('(', '').replace(')', '')
        self.address = ts[1].strip().replace(u'\xa0', u' ')
        self.type = soup.find('table', {'class': 'table_01'}).find('a', text="어린이집 유형").parent.parent.findNext('td').text

        coord = self.addr2coord(self.address)
        if coord == None:
            logger.error("[%s]%s can't get coordiation" % (self.stcode, self.name))
        else:
            self.lat = coord['lat']
            self.lng = coord['lng']
        logger.debug("[%s]%s is crawled" % (self.stcode, self.name))

    def addr2coord(self, address):
        daum_local_api = "https://apis.daum.net/local/geo/addr2coord?apikey=%s&q=%s&output=json"
        response = requests.get(daum_local_api % (DAUM_KEY, address))
        result = json.loads(response.text)
        if int(result["channel"]["totalCount"]) > 0:
            return result["channel"]["item"][0]
        else:
            return None


if __name__ == '__main__':
    os.remove(DB_FILENAME)
    crawl_arcodes()
    crawl_nurseries()
