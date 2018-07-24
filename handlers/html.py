import aiohttp_jinja2
from aiohttp import web
from model import Database
from aiohttp_session import get_session



async def home(request: web.Request):

    db: Database = request.app["database"]
    session = await get_session(request)
    hosts: list = await db.hosts.get_hosts_for_user(session["user"])
    return aiohttp_jinja2.render_template('content_hosts.html', request, {"hosttable": hosts}, app_key=aiohttp_jinja2.APP_KEY, encoding='utf-8')


