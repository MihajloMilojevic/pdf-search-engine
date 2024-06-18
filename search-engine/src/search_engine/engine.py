from math import ceil

from .parser import Parser
from ..utils import strip_text
from ..trie import Trie
from ..graph import PagesGraph, GraphNode
from .generate import generate_trie, generate_graph
from .searches import BaseSearch, SearchResult
import pymupdf


class SearchEngine:
    # Weights for ranking
    # occurences of the word in the page is more relevant than the number of links and occurences in the links
    LINK_WEIGHT = 5
    LINK_OCCURRENCE_WEIGHT = 3
    WORD_OCCURRENCE_WEIGHT = 10


    def __init__(self, file_path: str, page_offset: int = 0):
        self.file_path: str = file_path
        self.page_offset: int = page_offset
        document = pymupdf.open(file_path)
        self.trie: Trie = generate_trie(document)
        self.graph: PagesGraph = generate_graph(document, page_offset)


    def search(self, input_text: str):
        parser = Parser(input_text)
        expression: BaseSearch = parser.parse()

        results = expression.search(self)
        return self.__rank(results)
        
        


    def __rank(self, results: SearchResult) -> dict[int, float]:
        scores = {}
        searched_words = results.words()
        # calucating score of each page
        for page in results:
            # each ingoing link is worth LINK_WEIGHT
            score = len(self.graph[page].in_edges) * self.LINK_WEIGHT
            # for each page that links to the current page check number of occurrences of each searched words
            for edge in self.graph[page].in_edges:
                if edge not in results:
                    continue
                for word in searched_words:
                    if word in results[edge]:
                        score += self.LINK_OCCURRENCE_WEIGHT * results[edge][word].occurrences
            # for each word in the page check number of occurrences
            words = results[page]
            for word in words:
                score += self.WORD_OCCURRENCE_WEIGHT * words[word].occurrences
            # the more words are found the better - square the coefficient to more emphasize the difference
            score *= (len(words) / len(searched_words))**2
            scores[page] = score

        pages = []
        for page in results:
            wordlist = list(results[page].items())
            
            wordlist.sort(key=lambda x: x.occurrences, reverse=True)
            wordlist = list(map(lambda x: (x.word, x.positions), wordlist))
            pages.append((page, wordlist))
        pages.sort(key=lambda x: scores[x[0]], reverse=True)
        return pages



