import unittest
from gotorrent.swarm import Swarm


class SwarmTest(unittest.TestCase):
    def test_get_peers(self):
        list = Swarm(1)
        list.update(2)
        list.update(3)
        result = list.get_peers()
        self.assertEqual([1, 2, 3], result)

    def test_remove_unannounced(self):
        list = Swarm(1)
        list.update(2)
        list.update(3)
        list.remove_unannounced(diff_time=0)
        result = list.get_peers()
        self.assertEqual([], result)


if __name__ == '__main__':
    unittest.main()
