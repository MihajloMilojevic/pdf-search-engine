from ...trie import NodeData
from .results import SearchResult, WordResult

def convert_to_result(word: str, trie_data: list[NodeData]):
    result = SearchResult()
    if trie_data is None:
        return result
    for data in trie_data:
        page = data.page
        result.add(page, WordResult(word, data.occurrences, set(data.positions)))
    return result