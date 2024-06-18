
class GraphNode:
    def __init__(self, page):
        self.page = page
        self.in_edges = set()
        self.out_edges = set()

    def add_edge(self, edge, out=True):
        if out:
            self.out_edges.add(edge)
        else:
            self.in_edges.add(edge)

    def remove_edge(self, edge, out=True):
        if out:
            self.out_edges.remove(edge)
        else:
            self.in_edges.remove(edge)

    def __repr__(self):
        return str(self.page)

    def __str__(self):
        return str(self.page)