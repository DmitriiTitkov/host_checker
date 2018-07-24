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


async def auth_post(request: web.Request, body):
    """ Local user Authentication
       ---
      tags:
      - Authentication
      description: Local user Authentication
      parameters:
      - name: body
        in: body
        type: object
        schema:
          type: object
          properties:
            login:
               type: string
            password:
                type: string
          required:
            - login
            - password
        required:
          - body
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
    print(body)
    authenticated = False
    db = request.app['database']

    user_data = await db.users.get_user(body['login'])
    if user_data:
        if sha512_crypt.verify(body['password'], user_data["password"]):
            authenticated = True

    response_data = {
        "authenticated": authenticated
    }

    if not authenticated:
        return web.json_response(response_data, status=401)

    session = await get_session(request)
    session['user'] = body['login']
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