from random import choice
from pyactor.context import interval, later
from pyactor.exceptions import TimeoutError
import os


string_length = 0


class Peer(object):
    _tell = ['announce_me', 'attach_tracker', 'init_start', 'init_push',
             'init_pull', 'init_hybrid', 'set_seed', 'push', 'make_push',
             'make_pull', 'make_hybrid', 'attach_printer', 'stop_interval',
             'make_graph']
    _ask = ['get_id', 'pull', 'get_data']
    _ref = ['attach_tracker', 'attach_printer']

    def __init__(self):
        self.data = {}

    def set_seed(self):
        f = open("source.txt", "r")
        for idx, char in enumerate(f.read()):
            self.data[idx] = char
        f.close()
        global string_length
        string_length = idx+1

    def init_start(self):
        self.interval = interval(self.host, 3, self.proxy, 'announce_me')
        later(5, self.proxy, 'stop_interval')

    def stop_interval(self):
        self.interval.set()

    def init_push(self):
        self.cycle = 0
        self.interval = interval(self.host, 3, self.proxy, 'announce_me')
        self.interval_push = interval(self.host, 1, self.proxy, 'make_push')
        later(20, self.proxy, 'make_graph', 'Push', 'push')

    def init_pull(self):
        self.cycle = 0
        self.interval = interval(self.host, 3, self.proxy, 'announce_me')
        self.interval_pull = interval(self.host, 1, self.proxy, 'make_pull')
        later(20, self.proxy, 'make_graph', 'Pull', 'pull')

    def init_hybrid(self):
        self.cycle = 0
        self.interval = interval(self.host, 3, self.proxy, 'announce_me')
        self.interval_hybrid = interval(self.host, 1, self.proxy,
                                        'make_hybrid')
        later(20, self.proxy, 'make_graph', 'Hybrid', 'hybrid')

    def make_graph(self, title, filename):
        self.printer.to_graph(title, filename)

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
        self.printer.to_print(str(self.id) + str(self.data.items()))

    def make_push(self):
        self.cycle = self.cycle + 1
        for peer in self.tracker.get_peers("file"):
            try:
                data = choice(self.data.items())
                peer.push(data[0], data[1])
            except IndexError:
                pass
            self.printer.to_print(str(self.id) + str(self.data.items()))
            if self.id != "seed":
                self.printer.add_data_to_graph(self.id, self.cycle,
                                               len(self.data.keys()))

    def pull(self, chunk_id):
        return self.data[chunk_id]

    def make_pull(self):
        all = set(range(string_length))
        self.cycle = self.cycle + 1

        for peer in self.tracker.get_peers("file"):
            if self.id == peer.actor.id:
                continue
            used = set(self.data.keys())
            diff = list(all - used)
            if not diff:
                continue
            pos = choice(diff)
            try:
                self.data[pos] = peer.pull(pos)
            except (TimeoutError, KeyError):
                pass
            self.printer.to_print(str(self.id) +
                                  str(self.data.items()))
            self.printer.add_data_to_graph(self.id, self.cycle,
                                           len(self.data.keys()))

    def make_hybrid(self):
        all = set(range(string_length))
        self.cycle = self.cycle + 1

        for peer in self.tracker.get_peers("file"):
            try:
                # push
                data = choice(self.data.items())
                peer.push(data[0], data[1])
            except IndexError:
                pass
            # pulls
            if self.id == peer.actor.id:
                continue
            used = set(self.data.keys())
            diff = list(all - used)
            if not diff:
                continue
            pos = choice(diff)
            try:
                self.data[pos] = peer.pull(pos)
            except (TimeoutError, KeyError):
                pass
            self.printer.to_print(str(self.id) + str(self.data.items()))
            self.printer.add_data_to_graph(self.id,
                                           self.cycle, len(self.data.keys()))
