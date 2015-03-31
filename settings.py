import logging

ARNAMES = [
    "서울특별시", "부산광역시", "대구광역시",
    "인천광역시", "광주광역시", "대전광역시",
    "울산광역시", "경기도", "강원도",
    "충청북도", "충청남도", "전라북도", "전라남도",
    "경상북도", "경상남도", "제주도"
]

API020_KEY = "e52250c1fe194b0fbed49dced4d20376"
DAUM_KEY = "785e8fe5def74896cc2d2c4ace066d4d"
CHILDCARE_SERVICE_KEY = "4COh4sQ6iwph0lr3lsHdJjuSYuXFXtN6phc1+m2ALWgDfC9rGAFyLkwU/R3pDYm/jMPuzqmS6a6NJDx1oPHU0w=="

DB_FILENAME = "nursery.json"

CONSOLE_LOG_LEVEL = logging.DEBUG
FILE_LOG_LEVEL = logging.DEBUG

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILENAME = 'nursery.log'
