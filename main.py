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





async def create_pool(config: dict =json.load(open('config.json'))) -> asyncpg.pool.Pool:
    return await asyncpg.create_pool(config["databaseconfig"]["dsn"],
                                     min_size=config["databaseconfig"]["minsize"],
                                     timeout=config["databaseconfig"]["timeout"])


def main():
    router = SwaggerRouter(swagger_ui='/swagger/')
    app = web.Application(router=router, middlewares=[jsonify])
    add_routes(app)
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

    loop = asyncio.get_event_loop()
    pg_pool = loop.run_until_complete(create_pool())
    db = Database(pg_pool)
    app['database'] = db
    web.run_app(app)


if __name__ == "__main__":
    main()
