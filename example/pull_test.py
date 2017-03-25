from gotorrent.peer import *
from gotorrent.tracker import *
from pyactor.context import set_context, create_host, serve_forever
from gotorrent.printer import *


set_context()
host = create_host()

printer = host.spawn('printer', Printer)

# Spawn tracker and peers
tracker = host.spawn('tracker', Tracker)

s = host.spawn('seed', Peer)
s.set_seed()

p1 = host.spawn('peer1', Peer)
p2 = host.spawn('peer2', Peer)
p3 = host.spawn('peer3', Peer)
p4 = host.spawn('peer4', Peer)
p5 = host.spawn('peer5', Peer)

# Attach printer to peers
s.attach_printer(printer)
p1.attach_printer(printer)
p2.attach_printer(printer)
p3.attach_printer(printer)
p4.attach_printer(printer)
p5.attach_printer(printer)

# Attach tracker to peers
s.attach_tracker(tracker)
p1.attach_tracker(tracker)
p2.attach_tracker(tracker)
p3.attach_tracker(tracker)
p4.attach_tracker(tracker)
p5.attach_tracker(tracker)

# Start intervals
tracker.init_start()

s.init_pull()
p1.init_pull()
p2.init_pull()
p3.init_pull()
p4.init_pull()
p5.init_pull()

serve_forever()