import datetime

class ListTime(object):
    def __init__(self, peer):
        self.peers = {}
        self.update(peer)

    def remove_unannounced(self, diffTime = 10):
        current = datetime.datetime.now()
        aux_dict = {}
        for peer, last_update in self.peers.items():
            diff = current - last_update
            if (diff.total_seconds() <= diffTime):
                aux_dict[peer] = last_update
        self.peers = aux_dict
        print ', '.join(map(str, self.peers.keys()))

    def update(self, peer):
        self.peers[peer] = datetime.datetime.now()

    def get_peers(self):
        return self.peers.keys()