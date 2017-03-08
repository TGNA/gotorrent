from random import choice

class Peer(object):
    _tell = ['announce_me', 'attach_tracker', 'init_start', 'stop_interval', 'set_seed', 'push']
    _ask = ['get_id']
    _ref = ['attach_tracker']

    def __init__(self):
        self.data = {}

    def set_seed(self, string):
        for idx, char in enumerate(string):
            self.data[idx] = char

    def init_start(self):
        self.interval = self.host.interval(3, self.proxy, 'announce_me')
        self.interval_push = self.host.interval(1, self.proxy, 'make_push')
        self.host.later(5, self.proxy, 'stop_interval')

    def get_id(self):
        return self.id

    def stop_interval(self):
        self.interval.set()

    def announce_me(self):
        self.tracker.announce("file", self)

    def attach_tracker(self, tracker):
        self.tracker = tracker

    def push(self, chunk_id, chunk_data):
        self.data[chunk_id] = chunk_data
        print self.id, self.data.items()

    def make_push(self):
        peer = choice(self.tracker.get_peers())
        data = choice(self.data.items())

        peer.push(data[0], data[1])

