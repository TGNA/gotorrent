import unittest
from gotorrent.peer import *
from gotorrent.tracker import *
from pyactor.context import set_context, create_host, sleep, shutdown


class TrackerTest(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

    def test_tracker(self):
        try:
            set_context()
        except:
            pass

        try:

            host = create_host()
        except:
            pass

        # Spawn tracker and peers
        tracker = host.spawn('tracker', Tracker)
        p1 = host.spawn('peer1', Peer)
        p2 = host.spawn('peer2', Peer)
        p3 = host.spawn('peer3', Peer)
        # Attach tracker to peers
        p1.attach_tracker(tracker)
        p2.attach_tracker(tracker)
        p3.attach_tracker(tracker)

        # Start intervals
        tracker.init_start()

        p1.announce_me()
        sleep(0.5)
        self.assertEqual(['peer1'], tracker.get_peers("file"))

        p2.announce_me()
        sleep(0.5)
        self.assertEqual(set(['peer1', 'peer2']), set(tracker.get_peers("file")))

        p3.announce_me()
        sleep(0.5)
        self.assertEqual(set(['peer1', 'peer2', 'peer3']), set(tracker.get_peers("file")))

        self.assertEqual([], tracker.get_peers("file1"))

        shutdown()


if __name__ == '__main__':
    unittest.main()
