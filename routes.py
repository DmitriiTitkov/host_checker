from aiohttp import web
from handlers import html
from handlers.hosts import Hosts, Host
from aiohttp import hdrs


def add_routes(app: web.Application):
    app.router.add_route(hdrs.METH_GET, '/', html.home)

    # hosts
    app.router.add_route(hdrs.METH_GET, '/hosts', Hosts.get)
    app.router.add_route(hdrs.METH_POST, '/hosts', Hosts.post)
    app.router.add_route(hdrs.METH_GET, '/hosts/{host_name}', Host.get)
    app.router.add_route(hdrs.METH_DELETE, '/hosts/{host_name}', Host.delete)
    app.router.add_route(hdrs.METH_PUT, '/hosts/{host_name}', Host.put)


