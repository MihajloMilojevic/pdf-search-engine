from .graph_node import GraphNode

class PagesGraph:
    def __init__(self, num_pages):
        self.nodes: dict[GraphNode] = {}
        for page in range(num_pages):
            self.add_node(page)
        for i in range(num_pages):
            for j in [-1, 1]:
                if i + j >= 0 and i + j < num_pages:
                    self.add_edge(i, i + j)

    def add_node(self, page):
        node = GraphNode(page)
        self.nodes[page] = node
        return node

    def add_edge(self, origin: int, destination: int):
        self.nodes[origin].add_edge(destination, out=True)
        self.nodes[destination].add_edge(origin, out=False)

    def remove_edge(self, origin: int, destination: int):
        self.nodes[origin].remove_edge(destination, out=True)
        self.nodes[destination].remove_edge(origin, out=False)

    def __str__(self):
        return str(self.nodes)
    
    def __getitem__(self, key):
        return self.nodes[key]