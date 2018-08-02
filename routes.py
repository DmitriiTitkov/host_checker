from aiohttp import web
from handlers import html, auth
from handlers.hosts import Hosts, Host
from handlers import users
from aiohttp import hdrs



def add_routes(app: web.Application):
    # html
    app.router.add_route(hdrs.METH_GET, '/', html.home)
    app.router.add_route(hdrs.METH_GET, '/auth', auth.auth_get, name='auth')
    app.router.add_route(hdrs.METH_POST, '/auth', auth.auth_post)
    app.router.add_route(hdrs.METH_GET, '/logout', auth.logout, name='logout')


    # static
    # app.router.add_route([web.static('/static', '/home/dmitrii/code/host_checker/static', show_index=True)])
    app.router.add_static('/static', 'static')
    #  hosts
    app.router.add_route(hdrs.METH_GET, '/hosts', Hosts.get)
    app.router.add_route(hdrs.METH_POST, '/hosts', Hosts.post)
    app.router.add_route(hdrs.METH_GET, '/hosts/{host_id}', Host.get)
    app.router.add_route(hdrs.METH_DELETE, '/hosts/{host_id}', Host.delete)
    app.router.add_route(hdrs.METH_PUT, '/hosts/{host_id}', Host.put)

    # users
    app.router.add_route(hdrs.METH_GET, '/users', users.get)
    app.router.add_route(hdrs.METH_POST, '/users', users.post)
    app.router.add_route(hdrs.METH_GET, '/users/{login}/hosts', users.get_hosts)


