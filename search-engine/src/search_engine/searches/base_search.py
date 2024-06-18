from abc import ABC
from ..engine import SearchEngine
from .results import SearchResult


class BaseSearch(ABC):
    def search(self, engine: 'SearchEngine') -> 'SearchResult':
        pass