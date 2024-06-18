from .node import TrieNode
from .node_data import NodeData

class Trie(TrieNode):
    def __init__(self):
        super().__init__()

    def insert(self, word: str, data: 'NodeData'=None):
        node = self
        for letter in word:
            if letter not in node.children:
                node.children[letter] = TrieNode(letter)
            node = node.children[letter]
        node.is_end_of_word = True
        if data:
            node.data.append(data)

    def search(self, word: str) -> list[NodeData]:
        node = self
        for letter in word:
            if letter not in node.children:
                return None
            node = node.children[letter]
        if node.is_end_of_word:
            return node.data
        return None

    def starts_with(self, prefix) -> list[str]:
        node = self
        for letter in prefix:
            if letter not in node.children:
                return []
            node = node.children[letter]
        
        words = []
        queue = [(node, prefix)]
        while queue:
            (current_node, current_prefix) = queue.pop(0)
            if current_node.is_end_of_word:
                words.append(prefix + current_node.letter)
            queue.extend([(child, current_prefix + current_node.letter) for child in current_node.children.values()])
        return words

    def __repr__(self):
        return f"Trie()"
    
    def __contains__(self, word: str) -> bool:
        return self.search(word) is not None