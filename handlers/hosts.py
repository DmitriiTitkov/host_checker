from aiohttp import web
from model import Database
from utils.validators import authentication_required
from asyncpg.exceptions import UniqueViolationError


class Hosts:

    @staticmethod
    @authentication_required
    async def get(request: web.Request) -> web.Response:
        """ Returns all hosts.
           ---
          tags:
          - Hosts
          description: Returns all hosts.
          responses:
            200:
              description: OK
              schema:
                type: array
                items:
                  $ref: swagger.yaml#/definitions/host
        """
        db: Database = request.app['database']
        host_list: list = await db.hosts.get_hosts()
        return web.json_response(host_list, status=200)

    @staticmethod
    @authentication_required
    async def post(request: web.Request, body: dict) -> web.Response:
        """ Creates a new host record
           ---
          tags:
          - Hosts
          description: Creates a new host record
          parameters:
            - name: body
              in: body
              required: true
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
            '200':
              description: OK
            '400':
              description: Validation error
        """
        db: Database = request.app['database']
        try:
            resp = await db.hosts.add_host(body["host"], body["port"])
            return web.json_response(resp, status=200)
        except UniqueViolationError:
            raise web.HTTPConflict(reason="Host already exists")


class Host:

    @staticmethod
    @authentication_required
    async def get(request: web.Request, host_id: int):
        """ Returns all hosts defined by user
             ---
            tags:
            - Hosts
            description: Returns host by given id
            parameters:
              - name: host_id
                in: path
                schema:
                   type: integer
                   minimum: 1
                required:
                    - id
            responses:
              '200':
                description: OK
                schema:
                  $ref: swagger.yaml#/definitions/host
              '400':
                description: Validation error
              '404':
                description: Host Not Found
        """
        db: Database = request.app['database']
        resp = await db.hosts.get_host_by_id(host_id)
        if resp:
            return web.json_response(resp, status=200)

        raise web.HTTPNotFound(reason="Host not found")

    @staticmethod
    @authentication_required
    async def put(request: web.Request, host_id: int, body: dict) -> web.Response:
        """ Update existing host record otr create new if not exist
        ---
          tags:
          - Hosts
          description: Update existing host
          parameters:
            - name: host_id
              in: path
              schema:
                type: integer
                minimum: 1
              required: true
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
          responses:
            '204':
              description: Host updated
            '400':
              description: Validation error
        """
        db: Database = request.app['database']
        resp = await db.hosts.update_host(host_id, body["host"], body["port"])
        if resp:
            return web.json_response(status=204)

        raise web.HTTPNotFound(reason="Host with id = '{}' doesn't exist ".format(host_id))

    @staticmethod
    @authentication_required
    async def delete(request: web.Request, host_id: int) -> web.Response:
        """ Remove host by id
             ---
            tags:
            - Hosts
            description: Remove host by id
            parameters:
              - name: host_id
                in: path
                schema:
                   type: integer
                   minimum: 1
                required:
                    - id
            responses:
              '204':
                description: Host removed
              '400':
                description: Validation error
              '404':
                description: Not Found
        """

        db: Database = request.app['database']

        resp = await db.hosts.remove_host(host_id)
        if resp:
            return web.Response(status=200)

        raise web.HTTPNotFound(reason="Could not find the host")
