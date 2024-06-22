from math import ceil

from .parser import Parser
from ..utils import strip_text
from ..trie import Trie
from ..graph import PagesGraph, GraphNode
from .generate import generate_trie, generate_graph
from .searches import BaseSearch, SearchResult
import pymupdf
import spellchecker
import re

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
        document.close()


    def search(self, input_text: str, page: int = 1, results_per_page: int = 10):
        if not input_text:
            return [], 0, 1, results_per_page
        parser = Parser(input_text)
        expression: BaseSearch = parser.parse()

        results = expression.search(self)
        results = self.__rank(results)
        total_results = len(results)
        total_pages = ceil(len(results) / results_per_page)
        page = min(max(1, page), total_pages)
        start = (page - 1) * results_per_page
        results = results[start:start + results_per_page]
        for i in range(len(results)):
            results[i] = (results[i][0], self.__get_context(results[i][0], results[i][1]))
        return results, total_results, total_pages, page, results_per_page
    
    def __get_context(self, page: int, results: list[tuple[str, set[int]]]) -> str:
        CHARACTERS_BEFORE = 30
        CHARACTERS_AFTER = 100
        if len(results) == 0:
            return "", set()
        document = pymupdf.open(self.file_path)
        text = re.sub(r'[\n|\s+]', ' ', document[page].get_text())
        first_word = results[0][0]
        min_pos = min(results[0][1])
        all_words = set()
        for word, positions in results:
            all_words.add(word)
            if min(positions) < min_pos:
                min_pos = min(positions)
                first_word = word
        regex_match = re.search(rf'(?<![a-zA-Z]){first_word}(?![a-zA-Z])', text.lower())
        if regex_match is None:
            return "", all_words
        index = regex_match.start()
        start = max(0, index - CHARACTERS_BEFORE)
        end = min(len(text), index + CHARACTERS_AFTER)
        context = text[start:end]
        document.close()
        return context, all_words
    
    def complete(self, input_text: str):
        prefix = strip_text(input_text).lower().split()[-1]
        print(prefix)
        return self.trie.starts_with(prefix)[:5]
    
    def did_you_mean(self, input_text: str):
        words = strip_text(input_text).lower().split()
        spell = spellchecker.SpellChecker()
        made_corrections = False
        for word in words:
            if word in self.trie:
                continue
            best_suggestion = None
            best_suggestion_occurences = 0
            for suggestion in spell.candidates(word):
                if suggestion in self.trie:
                    if best_suggestion is None:
                        best_suggestion = suggestion
                        best_suggestion_occurences = self.__calucate_occurences(suggestion)
                        continue
                    current_suggestion_occurence = self.__calucate_occurences(suggestion)
                    if current_suggestion_occurence > best_suggestion_occurences:
                        best_suggestion = suggestion
                        best_suggestion_occurences = current_suggestion_occurence
            if best_suggestion is not None:
                input_text = re.sub(r'\b' + word + r'\b', best_suggestion, input_text)
                made_corrections = True
        return input_text, made_corrections


    def __calucate_occurences(self, word: str) -> int:
        trie_result = self.trie.search(word)
        if trie_result is None:
            return 0
        return sum(map(lambda x: x.occurrences, trie_result))

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



