from src.utils.relative_path import relative_path
from src.search_engine import SearchEngine
from src.search_engine.searches import SearchResult, WordSearch, FrazeSearch

def main():
    file_path = relative_path("data", "book.pdf")
    # output_folder = relative_path("data", "pages")
    # extract_pages(file_path, output_folder)
    search_engine = SearchEngine(file_path, 23)
    words = [WordSearch("data"), WordSearch("structures"), WordSearch("and"), WordSearch("algorithms")]
    fraze_search = FrazeSearch(words)
    results = fraze_search.search(search_engine)
    for page in results:
        print(page)
        for word in results[page]:
            print(f"\t{word}: {results[page][word].occurrences} {results[page][word].positions}")
    # while(True):
    #     query = input("Search: ")
    #     if query == "exit":
    #         break
    #     results = search_engine.search(query)
    #     for result in results:
    #         print(result)
    #     print("\n\n")
    
    

if __name__ == "__main__":
    main()