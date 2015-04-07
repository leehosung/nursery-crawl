import unittest

from util import addr2coord, name2coord


class UtilTestCase(unittest.TestCase):

    def test_addr2coord(self):
        result = addr2coord("서울특별시 중구 예장동 5")
        self.assertEqual(37.55953654696171, result['lat'])
        self.assertEqual(126.98887218728699, result['lng'])

    @unittest.skip("not implemented")
    def test_name2coord(self):
        result = name2coord("마리아몬테소리어린이집", "070-7581-1030", "서울특별시 성북구 정릉동 239")
        self.assertEqual(37.55953654696171, result['lat'])
        self.assertEqual(126.98887218728699, result['lng'])


if __name__ == '__main__':
    unittest.main()
