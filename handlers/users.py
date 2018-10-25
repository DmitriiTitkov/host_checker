from model import Database
from aiohttp import web
import asyncpg
from passlib.hash import sha512_crypt
from aiohttp_session import get_session
from utils.validators import authentication_required


@authentication_required
async def get(request: web.Request)-> web.Response:
    """ Returns all users
       ---
      tags:
      - Users
      description: Returns all users
      responses:
        200:
          description: OK
          schema:
            type: array
            items:
              $ref: swagger.yaml#/definitions/user
        '400':
          description: Validation error
    """

    db: Database = request.app['database']
    user_list: list = await db.users.get_users()
    return web.json_response(user_list, status=200)


@authentication_required
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
          schema:
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
        raise web.HTTPConflict(reason="User with this login already exists")


@authentication_required
async def get_hosts(request: web.Request, login: str) -> web.Response:
    """ Returns hosts for user
       ---
      tags:
      - Users
      description: Returns hosts for user
      parameters:
        - name: login
          in: path
          required: true
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
    db: Database = request.app["database"]
    result: dict = await db.hosts.get_hosts_for_user(login)
    return web.json_response(result, status=200)


@authentication_required
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
               minLength: 1
              port:
               type: integer
               minimum: 1
               maximum: 65535
            required:
              - host
              - port
            maxProperties: 2
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
        '409':
          description: Host has already been associated with user
        '400':
          description: Validation error
    """
    # check if host exists
    session = await get_session(request)
    db: Database = request.app["database"]
    try:
        host_record = await db.hosts.add_host(body["host"], body["port"])
    except asyncpg.exceptions.UniqueViolationError:
        host_record = await db.hosts.get_host(body["host"], body["port"])

    try:
        await db.hosts_users.add_user_host(host_record["id"], session["userID"])
        return web.json_response(host_record['id'], status=200)
    except asyncpg.exceptions.UniqueViolationError:
        raise web.HTTPConflict(reason="Host has already been added to user's list")


@authentication_required
async def remove_host(request: web.Request, login: str, host_id: int):
    """ Remove hosts for user
       ---
      tags:
      - Users
      description: Remove hosts for user
      parameters:
        - name: login
          in: path
          schema:
            type: string
        - name: host_id
          in: path
          schema:
            type: integer
            minimum: 1
      responses:
        '204':
          description: Host removed
        '400':
          description: Validation error
        '404':
          description: Not Found
    """
    db: Database = request.app["database"]
    session = await get_session(request)
    res = await db.hosts_users.remove_user_host(host_id, session["userID"])
    if res:
        return web.json_response({}, status=204)
    raise web.HTTPNotFound(reason="Host was not found for user '{}'".format(session["userID"]))






