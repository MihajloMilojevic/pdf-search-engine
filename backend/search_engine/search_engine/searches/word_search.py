from .convert import convert_to_result
from .base_search import BaseSearch

class WordSearch(BaseSearch):
    def __init__(self, word: str):
        self.word = word.lower()

    def search(self, engine):
        return convert_to_result(self.word, engine.trie.search(self.word))
    
    def __str__(self):
        return f"WordSearch({self.word})"
    
    def __repr__(self):
        return str(self)
        