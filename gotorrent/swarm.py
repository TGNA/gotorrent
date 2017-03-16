from datetime import datetime
from random import sample


class Swarm(object):
    def __init__(self, peer):
        self.peers = {}
        self.update(peer)

    def remove_unannounced(self, diff_time=10):
        current = datetime.now()
        aux_dict = {}
        for peer, last_update in self.peers.items():
            diff = current - last_update
            if diff.total_seconds() <= diff_time:
                aux_dict[peer] = last_update
        self.peers = aux_dict
        # print ', '.join(map(str, self.peers.keys()))

    def update(self, peer):
        self.peers[peer] = datetime.now()

    def get_peers_id(self):
        ids = map(lambda x : x.get_id(),self.peers.keys())
        return sample(ids,min(3, len(self.peers)))

    def get_peers(self):
        return sample(self.peers.keys(), min(3, len(self.peers)))
