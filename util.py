import json
import logging

import requests
import xmltodict

from settings import DAUM_KEY, NAVER_KEY
from exceptions import APIError, APILimitError

logger = logging.getLogger(__name__)


def addr2coord(address):
    logger.debug("addr2coord : addreess=%s", address)
    # TODO - try naver API
    daum_local_api = "https://apis.daum.net/local/geo/addr2coord?apikey=%s&q=%s&output=json"
    response = requests.get(daum_local_api % (DAUM_KEY, address))
    result = json.loads(response.text)
    if response.status_code != 200:
        if result['errorType'] == 'RequestThrottled':
            raise APILimitError(result['message'])
        raise APIError(result['message'])

    if int(result["channel"]["totalCount"]) > 0:
        return result["channel"]["item"][0]
    else:
        return None

def transfer_coord(x, y, from_coord="KTM", to_coord="WGS84"):
    logger.debug("transfer_coord : x=%s, y=%s", x, y)
    daum_local_api = "http://apis.daum.net/maps/transcoord?apikey=%s&x=%s&y=%s&fromCoord=%s&toCoord=%s&output=json"
    response = requests.get(daum_local_api % (DAUM_KEY, x, y, from_coord, to_coord))
    result = json.loads(response.text)
    return (result["x"], result["y"])

def info2coord(name, phone, address):
    logger.debug("info2coord : name=%s, phone=%s, address=%s", name, phone, address)
    daum_local_api = "https://apis.daum.net/local/v1/search/keyword.json?apikey=%s&query=%s"
    response = requests.get(daum_local_api % (DAUM_KEY, name))
    result = json.loads(response.text)
    for r in result["channel"]["item"]:
        if r["phone"] == phone or r["address"] == address:
            r["lat"] = r["latitude"]
            r["lng"] = r["longitude"]
            return r

    naver_local_api = "http://openapi.naver.com/search?key=%s&target=local&query=%s"
    headers = {'referer': 'http://nursery.novice.io'}
    response = requests.get(naver_local_api % (NAVER_KEY, name), headers=headers)
    for r in xmltodict.parse(response.text)["rss"]["channel"]["item"]:
        if r["telephone"] == phone or r["address"] == address:
            (x, y) = transfer_coord(r["mapx"], r["mapy"])
            r["lat"] = y
            r["lng"] = x
            return r

    return None
