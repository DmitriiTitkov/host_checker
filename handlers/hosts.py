from aiohttp import web
from model import Database



class Hosts:
    def __init__(self):
        pass

    async def get(self, request: web.Request) -> web.Response:
        """ Returns all hosts defined by user
           ---
          tags:
          - Hosts
          description: Returns all hosts defined by user
          parameters: []
          responses:
            200:
              description: OK
              content:
                application/json:
                    type: object
                    properties:
                      host:
                       type: string

            '400':
              description: Validation error
        """
        db: Database = request.app['database']
        host_list: list = await db.hosts.get_hosts()
        return web.json_response(host_list, status=200)

    async def post(self, request: web.Request, body: dict) -> web.Response:
        """ Returns all hosts defined by user
           ---
          tags:
          - Hosts
          description: Create new host record
          parameters:
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
                  status:
                   type: string
              required:
                  - host, port, protocol
          responses:
            '200':
              description: OK
            '400':
              description: Validation error
        """
        db: Database = request.app['database']
        resp = await db.hosts.add_host(body["host"], body["port"], body["protocol"], body["status"])
        return web.json_response(resp, status=200)


class Host:
    def __init__(self):
        pass

    async def get(self, request: web.Request, host_id: int):
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
              '400':
                description: Validation error
        """
        db: Database = request.app['database']
        return await db.hosts.get_host(host_id)

    async def put(self, request: web.Request, host_id: int, body: dict) -> web.Response:
        """ Update existing host record otr create new if not exist
        ---
          tags:
          - Hosts
          description: Update existing host record otr create new if not exist
          parameters:
            - name: host_id
              in: path
              schema:
                type: integer
                minimum: 1
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
              required:
                  - host_id, host, port, protocol
          responses:
            '200':
              description: OK
            '400':
              description: Validation error
        """
        db: Database = request.app['database']
        resp = await db.hosts.update_host(host_id, body["host"], body["port"], body["protocol"])
        return web.json_response(resp, status=200)

    async def delete(self, request: web.Request, host_id: int) -> web.Response:
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
        return web.Response(status=404)
