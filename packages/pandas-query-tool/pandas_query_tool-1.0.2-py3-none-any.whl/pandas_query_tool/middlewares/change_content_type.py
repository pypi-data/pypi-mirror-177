from fastapi import FastAPI, Request, Response
from fastapi.responses import RedirectResponse


async def process_js(request: Request, call_next):
    response: Response = await call_next(request)
    if request.url.path[-3:] == '.js':
        response.headers["content-type"] = 'application/javascript'
    return response
