from random import choice
from pyactor.context import interval, later


class Peer(object):
    _tell = ['announce_me', 'attach_tracker', 'init_start', 'init_push',
             'init_pull', 'init_hybrid', 'set_seed', 'push', 'make_push',
             'make_pull', 'make_hybrid', 'attach_printer', 'stop_interval']
    _ask = ['get_id', 'pull', 'get_data']
    _ref = ['attach_tracker', 'set_seed', 'attach_printer']

    def __init__(self):
        self.data = {}

    def set_seed(self, string):
        for idx, char in enumerate(string):
            self.data[idx] = char

    def init_start(self):
        self.interval = interval(self.host, 3, self.proxy, 'announce_me')
        later(5, self.proxy, 'stop_interval')

    def stop_interval(self):
        self.interval.set()

    def init_push(self):
        self.interval = interval(self.host, 3, self.proxy, 'announce_me')
        self.interval_push = interval(self.host, 1, self.proxy, 'make_push')

    def init_pull(self):
        self.interval = interval(self.host, 3, self.proxy, 'announce_me')
        self.interval_pull = interval(self.host, 1, self.proxy, 'make_pull')

    def init_hybrid(self):
        self.interval = interval(self.host, 3, self.proxy, 'announce_me')
        self.interval_hybrid = interval(self.host, 1, self.proxy,
                                        'make_hybrid')

    def get_id(self):
        return self.id

    def get_data(self):
        return ''.join(self.data.values())

    def announce_me(self):
        self.tracker.announce("file", self.proxy)

    def attach_tracker(self, tracker):
        self.tracker = tracker

    def attach_printer(self, printer):
        self.printer = printer

    def push(self, chunk_id, chunk_data):
        self.data[chunk_id] = chunk_data
        # self.printer.to_print(str(self.id) + str(self.data.items()))

    def make_push(self):
        for peer in self.tracker.get_peers("file"):
            try:
                data = choice(self.data.items())
                peer.push(data[0], data[1])
            except IndexError:
                pass

    def pull(self, chunk_id):
        return self.data[chunk_id]

    def make_pull(self):
        all = set(range(6))
        for peer in self.tracker.get_peers("file"):
            try:
                used = set(self.data.keys())
                diff = list(all - used)
                pos = choice(diff)
                self.data[pos] = peer.pull(pos)
                # self.printer.to_print(str(self.id) + str(self.data.items()))
            except IndexError:
                pass

    def make_hybrid(self):
        all = set(range(6))
        for peer in self.tracker.get_peers("file"):
            try:
                # push
                data = choice(self.data.items())
                peer.push(data[0], data[1])
            except IndexError:
                pass
            try:
                # pulls
                used = set(self.data.keys())
                diff = list(all - used)
                pos = choice(diff)
                self.data[pos] = peer.pull(pos)
            except IndexError:
                pass
