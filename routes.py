from aiohttp import web
from handlers import html
from handlers.hosts import Hosts, Host
from handlers import users
from aiohttp import hdrs


def add_routes(app: web.Application):
    app.router.add_route(hdrs.METH_GET, '/', html.home)

    # hosts
    app.router.add_route(hdrs.METH_GET, '/hosts', Hosts.get)
    app.router.add_route(hdrs.METH_POST, '/hosts', Hosts.post)
    app.router.add_route(hdrs.METH_GET, '/hosts/{host_id}', Host.get)
    app.router.add_route(hdrs.METH_DELETE, '/hosts/{host_id}', Host.delete)
    app.router.add_route(hdrs.METH_PUT, '/hosts/{host_id}', Host.put)

    app.router.add_route(hdrs.METH_GET, '/users', users.get)
    app.router.add_route(hdrs.METH_POST, '/users', users.post)


