from urllib.parse import quote
from functools import wraps
from aiohttp_session import get_session
from aiohttp import web


def authentication_required(f):
    @wraps(f)
    async def wrapper(request: web.Request):
        session = await get_session(request)
        app = request.app
        if not session.get('user', None):
            return web.HTTPFound("{0}?source={1}".format(app.router['auth'].url(), quote(request.path_qs)))
        return await f(request)
    return wrapper
