import sys

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import webbrowser

import pandas_query_tool.middlewares.apply as middlewares
from pandas_query_tool.routers.methods import router as router_methods
from pandas_query_tool.libs.startHelper import find_free_port

from pathlib import Path


def run():
    pass

    app = FastAPI()
    middlewares.apply(app)

    app.include_router(router_methods)

    static_path = str(Path(__file__).parent / 'static')
    # print(static_path)

    app.mount('/static', StaticFiles(directory=static_path))

    # print(__name__)
    # print('argv:', sys.argv[0])

    # if len(sys.argv) > 0 and sys.argv[1] == 'by_run':
    port = find_free_port()
    print('port:', port)

    webbrowser.open_new(
        f'http://localhost:{port}/static/index.html')

    uvicorn.run(app, host='localhost', port=port, use_colors=False)
    exit()

# if __name__ == '__main__':

#     port = 3000
#     print(port)
#     uvicorn.run('main:app', host='localhost', port=port, reload=True)
