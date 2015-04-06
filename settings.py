import os
import configparser

ARNAMES = [
    "서울특별시", "부산광역시", "대구광역시",
    "인천광역시", "광주광역시", "대전광역시",
    "울산광역시", "경기도", "강원도",
    "충청북도", "충청남도", "전라북도", "전라남도",
    "경상북도", "경상남도", "제주도"
]

DAUM_KEY = os.environ.get("DAUM_KEY")
API020_KEY = os.environ.get("API020_KEY")
CHILDCARE_SERVICE_KEY = os.environ.get("CHILDCARE_SERVICE_KEY")

if os.path.isfile("local_settings.py"):
    from local_settings import *
