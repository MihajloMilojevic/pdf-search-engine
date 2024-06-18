from abc import ABC
from .results import SearchResult


class BaseSearch(ABC):
    def search(self, engine) -> 'SearchResult':
        pass