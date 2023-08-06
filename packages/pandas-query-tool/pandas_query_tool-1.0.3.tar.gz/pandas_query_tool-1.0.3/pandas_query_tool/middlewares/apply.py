from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI
import functools

from .defaultIndex import process as defaultIndex_process
from .change_content_type import process_js
from .change_assets_path import process as assets_process


def apply(app: FastAPI):
    add = functools.partial(app.add_middleware, BaseHTTPMiddleware)

    add(dispatch=assets_process)
    add(dispatch=defaultIndex_process)
    add(dispatch=process_js)
