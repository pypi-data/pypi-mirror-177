from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse


async def process(request: Request, call_next):
    if request.url.path == '/':
        return RedirectResponse(request.base_url._url + 'static/index.html')

    return await call_next(request)
