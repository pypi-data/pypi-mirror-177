from starlette.responses import JSONResponse
import typing


class MyResponse(JSONResponse):
    """docstring for MyResponse."""

    def render(self, content: typing.Any):
        return super().render({'code': 200, 'data': content})
