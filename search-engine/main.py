from src.utils.relative_path import relative_path
from src import init

def main():
    file_path = relative_path("data", "book.pdf")
    picke_file = relative_path("data", "engine.pkl")
    search_engine = init(file_path, picke_file)
    while(True):
        query = input("Search: ")
        if query == "exit":
            break
        if not query:
            continue
        if query[-1] == "?":
            complete = search_engine.complete(query)
            for i in range(len(complete)):
                print(f"{i + 1}. {complete[i]}")
            continue
        did_you_mean, changed = search_engine.did_you_mean(query)
        if changed:
            choice = input(f"Did you mean: '{did_you_mean}' (y/n)? ")
            if choice.lower() == "y":
                query = did_you_mean
        print(f"Searching for: {query}")
        results, total_results, total_pages, page, result_per_page = search_engine.search(query)
        start = (page - 1) * result_per_page + 1
        print("Found", total_results, "results")
        while True:
            print(f"Showing page {page} of {total_pages} with {result_per_page} results per page:")
            for i in range(len(results)):
                page_number, (context, all_words) = results[i]
                print(f"{start + i}. page: {page_number}")
                print(f"Context: ")
                print("="*20)
                print(f"...{context}...")
                print("="*20)
                print()
            print(f"Showing page {page} of {total_pages} with {result_per_page} results per page:")
            print()
            should_break = False
            while True:
                choice = input("Next page(n), Previous page(p), Search(s): ").lower()
                next_page = page
                if choice == "s":
                    should_break = True
                    break
                elif choice == "n":
                    if page == total_pages:
                        print("No more pages")
                        continue
                    next_page += 1
                elif choice == "p":
                    if page == 1:
                        print("No previous pages")
                        continue
                    next_page -= 1
                else:
                    print("Invalid choice")
                    continue
                results, total_results, total_pages, page, result_per_page = search_engine.search(query, next_page)
                start = (page - 1) * result_per_page + 1
                break
            if should_break:
                break

if __name__ == "__main__":
    main()