import asyncio
from aiohttp import web
from routes import add_routes
import aiohttp_jinja2
import jinja2
import asyncpg
import json
from model import Database
from aiohttp_apiset.middlewares import jsonify
from aiohttp_apiset import SwaggerRouter
import aiohttp_session




async def create_pool(config: dict =json.load(open('config.json'))) -> asyncpg.pool.Pool:
    return await asyncpg.create_pool(config["databaseconfig"]["dsn"],
                                     min_size=config["databaseconfig"]["minsize"],
                                     timeout=config["databaseconfig"]["timeout"])


async def check_host_status(app: web.Application):
    try:
        db: Database = app['database']
        hosts: list = await db.hosts.get_hosts()
        while True:
            # for host in hosts:
            #     ip = host["host"]
            #     port = 80
            #     loop = app.loop
            #     # asyncio.create_con asyncio.Protocol
            #     conn = asyncio.open_connection(ip, port, loop=loop)
            #     try:
            #         _, _ = await asyncio.wait_for(conn, timeout=3)
            #         print(ip, port, 'ok')
            #
            #     except:
            #         print(ip, port, 'nok')
            #
            #     finally:
            #         conn.close()

            await asyncio.sleep(10)
            # with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            #     sock.setblocking(False)
            #     print("asdasd")
            #     # result = sock.connect_ex((host.host, host.port))
            #     # print(result)
            #     print(await app.loop.sock_connect(sock, ("google.com", 80)))

    except asyncio.CancelledError:
        pass

    finally:
        pass

async def start_background_tasks(app):
    app['host_status_checker'] = app.loop.create_task(check_host_status(app))


async def cleanup_background_tasks(app):
    app['host_status_checker'].cancel()

def main():
    router = SwaggerRouter(swagger_ui='/swagger/')
    session_middleware = aiohttp_session.session_middleware(aiohttp_session.SimpleCookieStorage())
    app = web.Application(router=router, middlewares=[jsonify, session_middleware])
    add_routes(app)
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

    loop = asyncio.get_event_loop()

    pg_pool = loop.run_until_complete(create_pool())
    db = Database(pg_pool)
    app['database'] = db
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
    web.run_app(app)


if __name__ == "__main__":
    main()
