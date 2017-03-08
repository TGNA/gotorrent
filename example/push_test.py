from gotorrent.peer import *
from gotorrent.tracker import *
from pyactor.context import set_context, create_host, serve_forever
from gotorrent.printer import *

set_context()
host = create_host()

printer = host.spawn('printer', Printer)
# Spawn tracker and peers
tracker = host.spawn('tracker', Tracker)
p1 = host.spawn('peer1', Peer)
p1.set_seed("qwerty")
p2 = host.spawn('peer2', Peer)
p3 = host.spawn('peer3', Peer)

p1.attach_printer(printer)
p2.attach_printer(printer)
p3.attach_printer(printer)

# Attach tracker to peers
p1.attach_tracker(tracker)
p2.attach_tracker(tracker)
p3.attach_tracker(tracker)

# Start intervals
tracker.init_start()

p1.init_start()
p2.init_start()
p3.init_start()

serve_forever()
