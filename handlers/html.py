import aiohttp_jinja2
from aiohttp import web
from model import Database
from aiohttp_session import get_session
from utils.validators import authentication_required


@authentication_required
async def home(request: web.Request):
    app: web.Application = request.app
    db: Database = app["database"]
    session = await get_session(request)
    hosts: list = await db.hosts.get_hosts_for_user(session["user"])
    template_vars:dict = {"hosttable": hosts, "user": {"name": session["user"]}, "links": {"logout": app.router['logout'].url()}}
    return aiohttp_jinja2.render_template('content_hosts.html', request, template_vars, app_key=aiohttp_jinja2.APP_KEY, encoding='utf-8')


