import aiohttp_jinja2
from aiohttp import web


async def home(request: web.Request):
    return aiohttp_jinja2.render_template('home.html', request, {}, app_key=aiohttp_jinja2.APP_KEY, encoding='utf-8')


async def auth_get(request: web.Request):
    """ Returns default auth page
       ---
      tags:
      - HTML Pages
      description: Returns authentication page

      responses:
        '200':
          description: OK
    """
    return aiohttp_jinja2.render_template('auth.html', request, {}, app_key=aiohttp_jinja2.APP_KEY, encoding='utf-8')
