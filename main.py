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
import concurrent.futures


async def create_pool(config: dict =json.load(open('config.json'))) -> asyncpg.pool.Pool:
    return await asyncpg.create_pool(config["databaseconfig"]["dsn"],
                                     min_size=config["databaseconfig"]["minsize"],
                                     timeout=config["databaseconfig"]["timeout"])


async def check_connection(host: dict) -> bool:
    w_stream = None
    try:
        conn = asyncio.open_connection(host["host"], host["port"])
        r_stream, w_stream = await asyncio.wait_for(conn, timeout=5)
        return True

    except concurrent.futures.TimeoutError:
        return False

    finally:
        if w_stream is not None:
            w_stream.close()


async def check_host_background_job(app: web.Application) -> None:
    db: Database = app['database']
    while True:
        hosts: list = await db.hosts.get_hosts()
        responses = await asyncio.gather(*[check_connection(host) for host in hosts], return_exceptions=True)
        for r_index in range(len(responses)):
            await db.hosts.update_host_status(hosts[r_index]["id"], responses[r_index])

        await asyncio.sleep(1)


async def start_background_tasks(app):
        app['host_status_checker'] = app.loop.create_task(check_host_background_job(app))


async def cleanup_background_tasks(app):
    app['host_status_checker'].cancel()
    await app['host_status_checker']


def main():
    router = SwaggerRouter(swagger_ui='/swagger/')
    router.include(spec='swagger.yaml')
    session_middleware = aiohttp_session.session_middleware(aiohttp_session.SimpleCookieStorage())
    app = web.Application(router=router, middlewares=[jsonify, session_middleware])
    add_routes(app)
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
    loop = asyncio.get_event_loop()
    loop.set_debug(True)

    pg_pool = loop.run_until_complete(create_pool())
    db = Database(pg_pool)
    app['database'] = db
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
    web.run_app(app)


if __name__ == "__main__":
    main()
