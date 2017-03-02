class Peer(object):
    _tell = ['announce_me', 'attach_tracker', 'init_start', 'stop_interval']
    _ask = ['get_id']
    _ref = ['attach_tracker']

    def init_start(self):
        self.interval = self.host.interval(3, self.proxy, 'announce_me')
        self.host.later(5, self.proxy, 'stop_interval')

    def get_id(self):
        return self.id

    def stop_interval(self):
        self.interval.set()

    def announce_me(self):
        self.tracker.announce("file", self)

    def attach_tracker(self, tracker):
        self.tracker = tracker
