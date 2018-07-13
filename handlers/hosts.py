from aiohttp import web
from model import Database



class Hosts:
    def __init__(self):
        pass

    async def get(self, request: web.Request) -> web.Response:
        """ Returns all hosts defined by user
           ---
          tags:
          - HostChecker
          description: Returns all hosts defined by user
          parameters: []
          responses:
            '200':
              description: OK
              schema:
                type: object
                properties:
                  host: string
                  port: string
                  status: string
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
          - HostChecker
          description: Returns all hosts defined by user
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
                  - snmp_oid
          responses:
            '200':
              description: OK
            '400':
              description: Validation error
        """
        db: Database = request.app['database']
        await db.hosts.add_host(body["host"], body["port"], body["protocol"], body["status"])

        print(body)
        pass


class Host:
    def __init__(self):
        pass

    async def get(self, request: web.Request):
        pass

    async def delete(self, request: web.Request) -> web.Response:
        pass

    async def put(self, request: web.Request) -> web.Response:
        pass

