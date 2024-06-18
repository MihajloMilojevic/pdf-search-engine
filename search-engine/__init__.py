from src.utils.relative_path import relative_path
from src.search_engine import SearchEngine
from src.search_engine.searches import SearchResult, WordSearch, PhraseSearch
from src.graph import PagesGraph, GraphNode
from src.trie import Trie, TrieNode, NodeData

import pickle
from pathlib import Path



def main():
    file_path = relative_path("data", "book.pdf")
    picke_file = relative_path("data", "engine.pkl")
    search_engine = init(file_path, picke_file)
    while(True):
        query = input("Search: ")
        if query == "exit":
            break
        results = search_engine.search(query)
        for result in results:
            print(result)
        print("\n\n")
    
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
    

if __name__ == "__main__":
    main()