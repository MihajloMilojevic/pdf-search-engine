import fastapi
import uvicorn

from search_engine import init, SearchEngine
from search_engine.utils.relative_path import relative_path
from fastapi import Response

root = fastapi.FastAPI()

pdf_file_path = relative_path("data", "book.pdf")
pickle_file_path = relative_path("data", "engine.pickle")

search_engine: SearchEngine = init(pdf_file_path, pickle_file_path)

@root.get("/api/search") 
async def search(query: str = "", page: int = 1, page_size: int = 10):
    if not query:
        return Response(content="Query is required", status_code=400)
    results, total_results, total_pages, page, result_per_page = search_engine.search(query, page, page_size)
    did_you_mean, changed = search_engine.did_you_mean(query)
    return {
        "results": results,
        "total_results": total_results,
        "total_pages": total_pages,
        "page": page,
        "result_per_page": result_per_page,
        "did_you_mean": did_you_mean if changed else ""
    }

@root.get("/api/autocomplete")
async def auto_complete(query: str = ""):
    if not query:
        return []
    return search_engine.complete(query)

# moment of truth 

from fastapi_react import frontend
root.mount('/', frontend(build_dir='build'))  # we are MOUNTING it!

if __name__ == '__main__':
    uvicorn.run(root, port=8080) # maybe ?

