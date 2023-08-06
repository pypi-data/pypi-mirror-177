from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse


async def process(request: Request, call_next):

    parts = request.url.path.split('/')
    first_part = parts[0]
    if len(parts) > 1 and parts[0] == '':
        first_part = parts[1]

    if first_part == 'assets':
        return RedirectResponse(request.base_url._url + 'static' + request.url.path)

    return await call_next(request)
