from ..engine import SearchEngine
from .convert import convert_to_result
from .base_search import BaseSearch

class WordSearch(BaseSearch):
    def __init__(self, word: str):
        self.word = word

    def search(self, engine: SearchEngine):
        return convert_to_result(self.word, engine.trie.search(self.word))
        