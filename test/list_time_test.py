import unittest
from gotorrent.list_time import ListTime


class ListTimeTest(unittest.TestCase):
    def test_get_peers(self):
        list = ListTime(1)
        list.update(2)
        list.update(3)
        result = list.get_peers()
        self.assertEqual([1, 2, 3], result)


if __name__ == '__main__':
    unittest.main()
