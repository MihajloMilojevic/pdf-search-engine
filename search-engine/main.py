from src.utils.relative_path import relative_path
from src.search_engine import SearchEngine

def main():
    file_path = relative_path("data", "book.pdf")
    # output_folder = relative_path("data", "pages")
    # extract_pages(file_path, output_folder)
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