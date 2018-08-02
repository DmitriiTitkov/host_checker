import aiohttp_jinja2
from aiohttp_session import get_session
from aiohttp import web
from passlib.hash import sha512_crypt


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


async def auth_post(request: web.Request, source: str, login: str, password: str):
    """ Local user Authentication
       ---
      tags:
      - Authentication
      description: Local user Authentication
      parameters:
      - in: formData
        name: login
        type: string
      - in: formData
        name: password
        type: string

      - name: source
        in: query
        schema:
          type: string
      responses:
        '200':
          description: OK
          schema:
            type: object
            properties:
              authenticated: string
        '400':
          description: Validation error
    """
    authenticated = False
    db = request.app['database']

    user_data = await db.users.get_user(login)
    if user_data:
        if sha512_crypt.verify(password, user_data["password"]):
            authenticated = True

    response_data = {
        "authenticated": authenticated
    }

    if not authenticated:
        return web.HTTPUnauthorized()

    session = await get_session(request)
    session['user'] = login
    if source:
        print(source)
        return web.HTTPFound(source)
    return web.json_response(response_data, status=200)


async def logout(request: web.Request):
    """ Logout page
       ---
      tags:
      - Authentication
      description: Logout page
      responses:
        '200':
          description: OK
    """
    session = await get_session(request)
    if session.get("user", None):
        session.clear()

    return aiohttp_jinja2.render_template('logout.html', request, {}, app_key=aiohttp_jinja2.APP_KEY, encoding='utf-8')