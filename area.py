from settings import ARNAMES, API020_KEY
import xmltodict
import requests
import logging


class Area(object):

    def __init__(self, sidoname, sigunname, arcode):
        self.sidoname = sidoname
        self.sigunname = sigunname
        self.arcode = int(arcode)

    def __str__(self):
        return "[%d]%s %s" % (self.arcode, self.sidoname, self.sigunname)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def save(self):
        pass

    @staticmethod
    def crawl_areas():
        for arname in ARNAMES:
           rs = Area.crawl_area(arname)
           for r in rs:
               yield Area(**r)

    @staticmethod
    def crawl_area(arname):
        uri = "http://api.childcare.go.kr/mediate/rest/cpmsapi020/cpmsapi020/request?key=%s&arname=%s" % (API020_KEY, arname)
        rs = xmltodict.parse(requests.get(uri).text)['response']['item']
        logging.debug("%d area are crawled with %s" % (len(rs), arname))
        return rs
