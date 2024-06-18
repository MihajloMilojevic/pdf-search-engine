from math import ceil
import types
from typing import List, Tuple

from ..utils import strip_text
from ..trie import Trie
from ..graph import PagesGraph, GraphNode
from .generate import generate_trie, generate_graph
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
        self.document = pymupdf.open(file_path)
        self.trie: Trie = generate_trie(self.document)
        self.graph: PagesGraph = generate_graph(self.document, page_offset)


    def search(self, input_text: str):
        if '"' in input_text:
            # Fraze search
            raise NotImplementedError("Phrase search is not implemented yet")
        if 'AND' in input_text or 'OR' in input_text or 'NOT' in input_text:
            # Boolean search
            raise NotImplementedError("Boolean search is not implemented yet")
        return self.__search_words(input_text)
    
    def __search_words(self, input_text: str):
        words = strip_text(input_text).split()
        results = {} 
        ### results = {
        ###    page: {
        ###        word: (occurrences, [positions])
        ###    }
        ### }
        for word in words:
            trie_results = self.trie.search(word)
            for trie_result in trie_results:
                page = trie_result.page
                if page not in results:
                    results[page] = {}
                if word not in results[page]:
                    results[page][word] = [0, []]
                results[page][word][0] += trie_result.occurrences
                results[page][word][1].extend(trie_result.positions)
        for page in results:
            for word in results[page]:
                results[page][word] = tuple(results[page][word])
        return results
        
        


    def __rank(self, results: dict[int, dict[str, tuple[int, list[int]]]], searched_words) -> dict[int, float]:
        scores = {}
        # calucating score of each page
        for page, words in results.items():
            # each ingoing link is worth LINK_WEIGHT
            score = len(self.graph[page].in_edges) * self.LINK_WEIGHT
            # for each page that links to the current page check number of occurrences of each searched words
            for edge in self.graph[page].in_edges:
                if edge not in results:
                    continue
                for word in searched_words:
                    if word in results[edge]:
                        score += self.LINK_OCCURRENCE_WEIGHT * results[edge][word][0]
            # for each word in the page check number of occurrences
            for word in words:
                score += self.WORD_OCCURRENCE_WEIGHT * words[word][0]
            # the more words are found the better - square the coefficient to more emphasize the difference
            score *= (len(words) / len(searched_words))**2
            scores[page] = score

        pages = []
        for page, words in results.items():
            wordlist = []
            for word, data in words.items():
                wordlist.append({
                    "word": word,
                    "occurrences": data[0],
                    "positions": data[1]
                })
            wordlist.sort(key=lambda x: x["occurrences"], reverse=True)
            wordlist = list(map(lambda x: (x["word"], x["positions"]), wordlist))
            pages.append((page, wordlist))
        pages.sort(key=lambda x: scores[x[0]], reverse=True)
        return pages



