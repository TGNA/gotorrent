import unittest
from gotorrent.peer import *
from gotorrent.tracker import *
from gotorrent.printer import *
from pyactor.context import set_context, create_host, sleep, shutdown


class PeerTest(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        try:
            set_context()
        except:
            pass
        try:
            self.host = create_host()
        except:
            pass

    def test_peer(self):
        # Spawn tracker and peers
        tracker = self.host.spawn('tracker', Tracker)
        p1 = self.host.spawn('peer1', Peer)
        p2 = self.host.spawn('peer2', Peer)
        p3 = self.host.spawn('peer3', Peer)
        # Attach printer to peers
        printer = self.host.spawn('printer', Printer)
        p1.attach_printer(printer)
        p2.attach_printer(printer)
        p3.attach_printer(printer)
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
        self.assertEqual(set(['peer1', 'peer2', 'peer3']), set(tracker.get_peers("file", True)))
        sleep(18)
        self.assertEqual([], tracker.get_peers("file"))

    def test_pull(self):
        p1 = self.host.spawn('peer1', Peer)
        p1.set_seed("qwerty")

        self.assertEqual(p1.pull(0), 'q')

    def test_push(self):
        p1 = self.host.spawn('peer1', Peer)
        p1.push(0, 'q')

        self.assertEqual(p1.pull(0), 'q')

    def test_get_data_set_seed(self):
        p1 = self.host.spawn('peer1', Peer)
        p1.set_seed("qwerty")
        self.assertEqual(p1.get_data(), 'qwerty')

    def test_make_pull(self):
        tracker = self.host.spawn('tracker', Tracker)
        p1 = self.host.spawn('peer1', Peer)
        p1.set_seed("qwerty")
        p2 = self.host.spawn('peer2', Peer)
        p3 = self.host.spawn('peer3', Peer)

        p1.attach_tracker(tracker)
        p2.attach_tracker(tracker)
        p3.attach_tracker(tracker)

        # Attach printer to peers
        printer = self.host.spawn('printer', Printer)
        p1.attach_printer(printer)
        p2.attach_printer(printer)
        p3.attach_printer(printer)

        # Start intervals
        tracker.init_start()

        p1.init_pull()
        p2.init_pull()
        p3.init_pull()

        sleep(30)

        self.assertEqual(p1.get_data(), 'qwerty')
        self.assertEqual(p2.get_data(), 'qwerty')
        self.assertEqual(p3.get_data(), 'qwerty')

    def test_make_push(self):
        tracker = self.host.spawn('tracker', Tracker)
        p1 = self.host.spawn('peer1', Peer)
        p1.set_seed("qwerty")
        p2 = self.host.spawn('peer2', Peer)
        p3 = self.host.spawn('peer3', Peer)

        p1.attach_tracker(tracker)
        p2.attach_tracker(tracker)
        p3.attach_tracker(tracker)

        # Attach printer to peers
        printer = self.host.spawn('printer', Printer)
        p1.attach_printer(printer)
        p2.attach_printer(printer)
        p3.attach_printer(printer)

        # Start intervals
        tracker.init_start()

        p1.init_push()
        p2.init_push()
        p3.init_push()

        sleep(30)

        self.assertEqual(p1.get_data(), 'qwerty')
        self.assertEqual(p2.get_data(), 'qwerty')
        self.assertEqual(p3.get_data(), 'qwerty')

    def test_make_hybrid(self):
        tracker = self.host.spawn('tracker', Tracker)
        p1 = self.host.spawn('peer1', Peer)
        p1.set_seed("qwerty")
        p2 = self.host.spawn('peer2', Peer)
        p3 = self.host.spawn('peer3', Peer)

        p1.attach_tracker(tracker)
        p2.attach_tracker(tracker)
        p3.attach_tracker(tracker)

        # Attach printer to peers
        printer = self.host.spawn('printer', Printer)
        p1.attach_printer(printer)
        p2.attach_printer(printer)
        p3.attach_printer(printer)

        # Start intervals
        tracker.init_start()

        p1.init_hybrid()
        p2.init_hybrid()
        p3.init_hybrid()

        sleep(20)

        self.assertEqual(p1.get_data(), 'qwerty')
        self.assertEqual(p2.get_data(), 'qwerty')
        self.assertEqual(p3.get_data(), 'qwerty')

    def tearDown(self):
        shutdown()

if __name__ == '__main__':
    unittest.main()
