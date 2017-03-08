import unittest
from gotorrent.peer import *
from gotorrent.tracker import *
from pyactor.context import set_context, create_host, serve_forever


class PushTest(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

    def test_push(self):
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
        p1.set_seed("nando pene corto")
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



        serve_forever()


if __name__ == '__main__':
    unittest.main()
