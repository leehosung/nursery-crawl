import unittest

from util import addr2coord, transfer_coord, info2coord
from exceptions import APILimitError


class UtilTestCase(unittest.TestCase):

    def test_addr2coord(self):
        try:
            result = addr2coord("서울특별시 중구 예장동 5")
        except APILimitError:
            return
        self.assertEqual(37.55953654696171, result['lat'])
        self.assertEqual(126.98887218728699, result['lng'])

    def test_transfer_coord(self):
        (x, y) = transfer_coord(312563, 557832)
        self.assertEqual(127.0073380512766, x)
        self.assertEqual(37.618638925256256, y)

    def test_info2coord(self):
        try:
            result = info2coord("마리아몬테소리어린이집", "070-7581-1030", "서울특별시 성북구 정릉동 239")
        except APILimitError:
            return
        self.assertEqual(37.618638925256256, result['lat'])
        self.assertEqual(127.0073380512766, result['lng'])


if __name__ == '__main__':
    unittest.main()
