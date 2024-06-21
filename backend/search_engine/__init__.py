from .utils.relative_path import relative_path
from .search_engine import SearchEngine
from .search_engine.searches import SearchResult, WordSearch, PhraseSearch
from .graph import PagesGraph, GraphNode
from .trie import Trie, TrieNode, NodeData

import pickle
from pathlib import Path

    
def init(book_file_path: str, pickle_file_path: str):
    pickle_file =  Path(pickle_file_path)
    if pickle_file.is_file():
        try:
            with open(pickle_file_path, "rb") as file:
                loaded_engine = pickle.load(file)
                print("Engine loaded from file")
                return loaded_engine
        except:
            print("Unable to deseriliaze engine, creating new now")
    engine = SearchEngine(book_file_path, 23)
    try:
        with open(pickle_file_path, "wb") as file:
            pickle.dump(engine, file)
    except Exception as e:
        print(e)
        print("Unable to serialize engine")
    return engine