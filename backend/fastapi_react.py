
def frontend(build_dir="./build"):
    """
     FASTAPI ROUTER FOR REACT FRONTEND
    :param build_dir: the path to your build folder for react
            we are assuming the "static" folder lives within your build folder
            if not, change it some lines below
    :return: fastapi.FastAPI
    """

    import pathlib
    import fastapi.exceptions
    from fastapi import FastAPI, Request, Response
    from fastapi.staticfiles import StaticFiles

    build_dir = pathlib.Path(build_dir)

    react = FastAPI(openapi_url="")
    react.mount('/static', StaticFiles(directory=build_dir / "static"))

    @react.get('/{path:path}')
    async def handle_catch_all(request: Request, path):

        if path and path != "/":
            disk_path = build_dir / path
            if disk_path.exists():
                return Response(disk_path.read_bytes(), 200)
            else:
                if disk_path.is_file():
                    raise fastapi.exceptions.HTTPException(404)

        return Response((build_dir / "index.html").read_bytes(), 200)

    return react