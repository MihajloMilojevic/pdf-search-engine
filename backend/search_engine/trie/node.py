from .node_data import NodeData

class TrieNode:
    def __init__(self, letter=None):
        self.letter = letter
        self.children: dict[str, TrieNode] = {}
        self.is_end_of_word = False
        self.data: list[NodeData] = []

    def __repr__(self):
        return f"TrieNode({self.letter})"