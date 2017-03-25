import plotly.plotly as py
import plotly.graph_objs as go


class Printer(object):
    _tell = ['to_print', 'add_data_to_graph', 'to_graph']

    def __init__(self):
        self.data = {}

    def to_print(self, string):
        print string

    def add_data_to_graph(self, peer_id, cycle, size):
        try:
            self.data[peer_id].x.append(cycle)
            self.data[peer_id].y.append(size)
        except KeyError:
            self.data[peer_id] = go.Scatter(
                x=[cycle],
                y=[size],
                name=peer_id
            )

    def to_graph(self, title, filename):
        layout = go.Layout(
            title=title,
            width=1000,
            height=640,
            xaxis=dict(title='gossip cycle'),
            yaxis=dict(title='string size'),
        )

        fig = go.Figure(data=self.data.values(), layout=layout)
        py.image.save_as(fig, filename=filename + '.png')
        print "generated graphic " + filename + '.png'
