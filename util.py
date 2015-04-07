import json

import requests
import xmltodict

from settings import DAUM_KEY, NAVER_KEY
from exceptions import APIError, APILimitError


def addr2coord(address):
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

def name2coord(name, phone, address):
    daum_local_api = "https://apis.daum.net/local/v1/search/keyword.json?apikey=%s&query=%s"
    response = requests.get(daum_local_api % (DAUM_KEY, name))
    result = json.loads(response.text)
    for r in result["channel"]["item"]:
        if r["phone"] == phone or r["address"] == address:
            return r

    #naver_local_api = "http://openapi.naver.com/search?key=%s&target=local&query=%s"
    #headers = {'referer': 'http://nursery.novice.io'}
    #response = requests.get(naver_local_api % (NAVER_KEY, name), headers=headers)
    #for r in xmltodict.parse(response.text)["rss"]["channel"]["item"]:
    #    if r["telephone"] == phone or r["address"] == address:
    #        return r
    # http://apis.daum.net/maps/transcoord?apikey=key&x=경도&y=위도&fromCoord=KTM&toCoord=WGS84&output=xml

    return None
