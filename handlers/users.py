from model import Database
from aiohttp import web
import asyncpg
from passlib.hash import sha512_crypt


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
        result_id: dict = await db.users.add_user(body['login'], sha512_crypt.hash(body['password']))
        return web.json_response(result_id, status=200)
    except asyncpg.exceptions.UniqueViolationError:
        return web.json_response({"error": "User with this login already exists"}, status=409)


async def get_hosts(request: web.Request, login: str) -> web.Response:
    """ Returns hosts for user
       ---
      tags:
      - Users
      description: Returns hosts for user
      parameters:
        - name: login
          in: path
          schema:
            type: string
      responses:
        200:
          description: OK
          content:
            application/json:
                type: array
                items:
                  type: object
                  properties:
                    host:
                      type: string
        '400':
          description: Validation error
    """
    print(login)
    db: Database = request.app["database"]
    result: dict = await db.hosts.get_hosts_for_user(login)
    return web.json_response(result, status=200)


async def add_host(request: web.Request, login: str, body: dict) -> web.Response:
    """ Adds host for user
       ---
      tags:
      - Users
      description: Adds host for user
      parameters:
        - name: login
          in: path
          schema:
            type: string
        - name: body
          in: body
          schema:
            type: object
            properties:
              host:
               type: string
              port:
               type: integer
              protocol:
               type: string
               enum:
                - tcp
                - udp
            required:
              - host
              - port
              - protocol
            maxProperties: 3
      responses:
        200:
          description: OK
          content:
            application/json:
                type: array
                items:
                  type: object
                  properties:
                    host:
                      type: string
        '400':
          description: Validation error
    """
    # check if host existss
    print(login)
    host, port, protocol = [val for val in body.values()]
    db: Database = request.app["database"]
    try:
        host_id = await db.hosts.add_host(host, port, protocol)
    except asyncpg.exceptions.UniqueViolationError:
        # duplicated value found
        pass
    if host:
        await db.hosts.ad
    result: dict = await db.hosts.get_hosts_for_user(login)
    return web.json_response(result, status=200)


