'''
Tracker
Made by: Oscar Blanco and Victor Colome
'''

from list_time import ListTime


class Tracker(object):
    _tell = ['announce', 'init_start', 'check_peers']
    _ask = ['get_peers']
    _ref = ['announce']

    def __init__(self):
        self.peers = {}

    def init_start(self):
        self.interval_check = self.host.interval(1, self.proxy, 'check_peers')

    def check_peers(self):
        for key, peers in self.peers.items():
            peers.remove_unannounced()

    def announce(self, torrent_hash, peer_ref):
        try:
            self.peers[torrent_hash].update(peer_ref)
        except KeyError:
            self.peers[torrent_hash] = ListTime(peer_ref)

    def get_peers(self, torrent_hash):
        try:
            return self.peers[torrent_hash].get_peers()
        except KeyError:
            return []
