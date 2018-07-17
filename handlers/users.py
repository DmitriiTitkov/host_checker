from model import Database
from aiohttp import web
import asyncpg


async def get(request: web.Request)-> web.Response:
    """ Returns all users
       ---
      tags:
      - Users
      description: Returns all users
      parameters: []
      responses:
        200:
          description: OK
          content:
            application/json:
                type: array
                items:
                  type: object
                  properties:
                    id:
                      type: integer
                    login:
                      type: string
        '400':
          description: Validation error
    """

    db: Database = request.app['database']
    user_list: list = await db.users.get_users()
    return web.json_response(user_list, status=200)


async def post(request: web.Request, body: dict)-> web.Response:
    """ Create user
       ---
      tags:
      - Users
      description: Create a new user
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
      responses:
        200:
          description: OK
          content:
            application/json:
                type: object
                properties:
                  id:
                    type: integer
        '400':
          description: Validation error
    """
    try:
        db: Database = request.app['database']
        result_id: dict = await db.users.add_user(body['login'], body['password'])
        return web.json_response(result_id, status=200)
    except asyncpg.exceptions.UniqueViolationError:
        return web.json_response({"error": "User with this login already exists"}, status=409)
