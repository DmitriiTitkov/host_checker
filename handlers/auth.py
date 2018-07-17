import aiohttp_jinja2
from aiohttp_session import get_session
from aiohttp import web
from passlib.hash import sha512_crypt


async def auth_post(request: web.Request):
    """ Local user Authentication
       ---
      tags:
      - Authentication
      description: gLocal user Authentication
      parameters:
      - name: body
        in: body
        schema:
          type: object
          properties:
            login:
               type: string
            password:
                type: string
          required:
            - login
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
    json_data = await request.json()
    login = json_data.get("login", None)
    password = json_data.get("password", None)
    db = request.app['database']

    user_data = await db.users.get_user(login)
    if user_data:
        if sha512_crypt.verify(password, user_data["password"]):
            authenticated = True

    response_data = {
        "authenticated": authenticated
    }
    if authenticated:
        session = await get_session(request)
        session['user'] = login
        return web.json_response(response_data, status=200)
    else:
        return web.json_response(response_data, status=401)


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