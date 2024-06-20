import fastapi
import uvicorn

root = fastapi.FastAPI()
@root.get('/some/path')
def some_path():
    return {'some': 'data'}
@root.get('/some/other/path')
def some_other_path():
    return {'some': 'data 2'}

# moment of truth 

from src.fastapi_react import frontend
root.mount('/', frontend(build_dir='build'))  # we are MOUNTING it!

uvicorn.run(root, port=8080) # maybe ?

