import unittest
from gotorrent.peer import *
from gotorrent.tracker import *
from pyactor.context import set_context, create_host, sleep, shutdown


class PeerTest(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

    def test_peer(self):
        try:
            set_context()
        except:
            pass

        try:
            host = create_host()
        except:
            pass

        self.assertEqual(host.__class__.__name__, 'Proxy')
        self.assertEqual(host.actor.klass.__name__, 'Host')

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

        p1.init_start()
        p2.init_start()
        p3.init_start()
        sleep(5)
        self.assertEqual(set(['peer1', 'peer2', 'peer3']), set(tracker.get_peers("file")))
        sleep(15)
        self.assertEqual([], tracker.get_peers("file"))
        shutdown()


if __name__ == '__main__':
    unittest.main()
