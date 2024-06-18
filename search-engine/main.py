from src.utils.relative_path import relative_path
from src.search_engine import SearchEngine
from src.search_engine.searches import SearchResult, WordSearch, PhraseSearch

def main():
    file_path = relative_path("data", "book.pdf")
    search_engine = SearchEngine(file_path, 23)
    while(True):
        query = input("Search: ")
        if query == "exit":
            break
        results = search_engine.search(query)
        for result in results:
            print(result)
        print("\n\n")
    
    

if __name__ == "__main__":
    main()