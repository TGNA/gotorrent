import unittest
from gotorrent.peer import *
from gotorrent.tracker import *
from pyactor.context import set_context, create_host, sleep, shutdown


class PeerTest(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        try:
            set_context()
        except:
            pass
        self.host = create_host()
        # Spawn tracker and peers
        self.tracker = self.host.spawn('tracker', Tracker)
        self.p1 = self.host.spawn('peer1', Peer)
        self.p2 = self.host.spawn('peer2', Peer)
        self.p3 = self.host.spawn('peer3', Peer)
        # Attach tracker to peers
        self.p1.attach_tracker(self.tracker)
        self.p2.attach_tracker(self.tracker)
        self.p3.attach_tracker(self.tracker)

    def test_peer(self):
        self.tracker.init_start()
        self.p1.init_start()
        self.p2.init_start()
        self.p3.init_start()
        sleep(0.5)
        self.assertEqual(set(['peer1', 'peer2', 'peer3']), set(self.tracker.get_peers("file")))
        sleep(13)
        self.assertEqual([], self.tracker.get_peers("file"))
        shutdown()


if __name__ == '__main__':
    unittest.main()
