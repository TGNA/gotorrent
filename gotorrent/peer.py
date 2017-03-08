from random import choice

class Peer(object):
    _tell = ['announce_me', 'attach_tracker', 'init_start', 'set_seed', 'push', 'make_push', 'attach_printer']
    _ask = ['get_id']
    _ref = ['attach_tracker', 'set_seed', 'attach_printer']

    def __init__(self):
        self.data = {}

    def set_seed(self, string):
        for idx, char in enumerate(string):
            self.data[idx] = char

    def init_start(self):
        self.interval = self.host.interval(3, self.proxy, 'announce_me')
        self.interval_push = self.host.interval(1, self.proxy, 'make_push')

    def get_id(self):
        return self.id

    def announce_me(self):
        self.tracker.announce("file", self)

    def attach_tracker(self, tracker):
        self.tracker = tracker

    def attach_printer(self, printer):
        self.printer = printer

    def push(self, chunk_id, chunk_data):
        self.data[chunk_id] = chunk_data
        self.printer.to_print(str(self.id) + str(self.data.items()))

    def make_push(self):
        try:
            peer = choice(self.tracker.get_peers("file"))
            data = choice(self.data.items())

            peer.push(data[0], data[1])
        except:
            pass
