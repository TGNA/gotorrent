from pyactor.context import interval_host, later


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
