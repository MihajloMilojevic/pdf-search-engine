

class WordResult:
    def __init__(self, word: str, occurrences: int, positions: set[int]):
        self.word = word
        self.occurrences = occurrences
        self.positions = positions




class PageResult:
    def __init__(self, page: int):
        self.page = page
        self._words: dict[str, WordResult] = {}


    def add(self, item: WordResult):
        if item.word not in self._words:
            self._words[item.word] = item
        else:
            self._words[item.word].occurrences += item.occurrences
            self._words[item.word].positions = self._words[item.word].positions.union(item.positions)

    def items(self):
        return set(self._words.values())

    def words(self):
        return set(self._words.keys())

    def __getitem__(self, word: str):
        return self._words[word]
    
    def __iter__(self):
        return iter(self._words)
    
    def __contains__(self, word: str):
        return word in self._words
    
    def __len__(self):
        return len(self._words)
    

class SearchResult:
    def __init__(self):
        self._data: dict[int, PageResult] = {}

    def add(self, page: int, item: WordResult):
        if page not in self._data:
            self._data[page] = PageResult(page)
        self._data[page].add(item)
    
    def pages(self):
        return set(self._data.keys())
    
    def words(self):
        words = set()
        for page in self:
            for word in self[page]:
                words.add(word)
        return words
    
    def remove(self, page: int):
        del self._data[page]

    def __getitem__(self, page: int):
        return self._data[page]
    
    def __iter__(self):
        return iter(self._data.keys())
    
    def __contains__(self, page: int):
        return page in self._data
    
    def __len__(self):
        return len(self._data)
    
    def union(self, other: 'SearchResult'):
        result = SearchResult()
        for page in self:
            for word in self[page]:
                result.add(page, self[page][word])
        for page in other:
            for word in other[page]:
                result.add(page, other[page][word])
        return result
    
    def intersection(self, other: 'SearchResult'):
        result = SearchResult()
        for page in self:
            if page in other:
                for word in self[page]:
                    result.add(page, self[page][word])
                for word in other[page]:
                    result.add(page, other[page][word])
        return result
    
    def difference(self, other: 'SearchResult'):
        result = SearchResult()
        for page in self:
            if page not in other:
                for word in self[page]:
                    result.add(page, self[page][word])
        return result