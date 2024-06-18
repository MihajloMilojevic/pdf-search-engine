from ..engine import SearchEngine
from .convert import convert_to_result
from .base_search import BaseSearch
from .word_search import WordSearch
from .results import SearchResult

class FrazeSearch(BaseSearch):
    def __init__(self, words: list[WordSearch]):
        self.words = words

    def search(self, engine: SearchEngine):
        words_result = [word.search(engine) for word in self.words]
        possible_pages = words_result[0].pages().intersection(*[word_result.pages() for word_result in words_result[1:]])
        result = SearchResult()
        for page in possible_pages:
            indecies = []
            for word_result in words_result:
                if page not in word_result:
                    continue
            # find all indecies of the first word what is a start of the fraze
            for start_index in words_result[0][page][self.words[0].word].positions:
                found = True
                for i, word in enumerate(self.words[1:]):
                    if start_index + i + 1 not in words_result[i + 1][page][word.word].positions:
                        found = False
                        break
                if found:
                    indecies.append(start_index)
            if len(indecies) == 0:
                continue
            # delete all positions that are not a part of the fraze
            # print("Indecies: ",indecies)
            # print("Second word:", words_result[1][page][self.words[1].word].positions)
            for i in range(len(self.words)):    # loop over all words
                for position in set(words_result[i][page][self.words[i].word].positions): # loop over all positions of the word
                    if position - i not in indecies:
                        words_result[i][page][self.words[i].word].positions.remove(position)    # remove the position if it is not a part of the fraze
            for i in range(len(self.words)):
                result.add(page, words_result[i][page][self.words[i].word])
        return result
