from random import choice

class Peer(object):
    _tell = ['announce_me', 'attach_tracker', 'init_start', 'init_push', 'init_pull', 'set_seed', 'push', 'make_push', 'make_pull', 'attach_printer']
    _ask = ['get_id', 'pull']
    _ref = ['attach_tracker', 'set_seed', 'attach_printer']

    def __init__(self):
        self.data = {}

    def set_seed(self, string):
        for idx, char in enumerate(string):
            self.data[idx] = char

    def init_start(self):
        self.interval = self.host.interval(3, self.proxy, 'announce_me')

    def init_push(self):
        self.init_start()
        self.interval_push = self.host.interval(1, self.proxy, 'make_push')

    def init_pull(self):
        self.init_start()
        self.interval_pull = self.host.interval(1, self.proxy, 'make_pull')

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
        for peer in self.tracker.get_peers("file"):
            try:
                data = choice(self.data.items())
                peer.push(data[0], data[1])
            except:
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
                self.printer.to_print(str(self.id) + str(self.data.items()))
                # self.printer.to_print(str(self.id) + str(all) + str(used) + str(diff) + str(pos))
            except:
                pass
