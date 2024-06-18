
class TrieNode:
    def __init__(self, letter=None):
        self.letter = letter
        self.children = {}
        self.is_end_of_word = False
        self.data = []

    def __repr__(self):
        return f"TrieNode({self.letter})"