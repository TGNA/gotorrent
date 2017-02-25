'''
Tracker
Made by: Oscar Blanco and Victor Colome
'''

from pyactor.context import set_context, interval_host, create_host, sleep, serve_forever, later
from list_time import ListTime


class Tracker(object):
    _tell = ['announce', 'init_start']
    _ask = ['get_peers']
    _ref = ['announce']

    def __init__(self):
        self.peers = {}

    def init_start(self):
        self.interval_check = interval_host(self.host, 10, self.check_peers)

    def check_peers(self):
        for key, peers in self.peers.items():
            print "==="
            print key
            peers.remove_unannounced()
            print "==="

    def announce(self, torrent_hash, peer_ref):
        print "announce from", peer_ref
        try:
            self.peers[torrent_hash].update(peer_ref)
        except KeyError:
            self.peers[torrent_hash] = ListTime(peer_ref)

    def get_peers(self, torrent_hash):
        try:
            return self.peers[torrent_hash].get_peers()
        except KeyError:
            return []


class Peer(object):
    _tell = ['announce_me', 'attach_tracker', 'init_start']
    _ask = []
    _ref = ['attach_tracker']

    def init_start(self):
        self.interval = interval_host(self.host, 3, self.announce_me)
        later(15, self.stop_interval)

    def stop_interval(self):
        self.interval.set()

    def announce_me(self):
        self.tracker.announce("file", self.id)

    def attach_tracker(self, tracker):
        self.tracker = tracker


if __name__ == "__main__":
    set_context()
    host = create_host()
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
    sleep(2)
    p1.init_start()
    sleep(2)
    p2.init_start()
    sleep(15)
    p3.init_start()

    serve_forever()
