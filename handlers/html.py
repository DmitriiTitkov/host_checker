import aiohttp_jinja2
from aiohttp import web
from utils.validators import authentication_required


@authentication_required
async def home(request: web.Request):
    """
    ---
    tags:
      - HTML Pages
    description: Returns default home page
    """
    return aiohttp_jinja2.render_template('react.master.html', request, {}, app_key=aiohttp_jinja2.APP_KEY, encoding='utf-8')


