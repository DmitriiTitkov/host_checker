import asyncpg
import json


class Hosts:
    def __init__(self, pool: asyncpg.pool.Pool) -> None:
        self.__pool = pool

    async def get_hosts(self) -> list:
        async with self.__pool.acquire() as con:  # type: asyncpg.connection.Connection
            con.set_type_codec(
                'json',
                encoder=json.dumps,
                decoder=json.loads,
                schema='pg_catalog'
            )
            rows = await con.fetch("""
                SELECT * 
                FROM 
                    hosts
                """)
            data = []
            print(rows)
            for row in rows:
                data.append({
                    'host': row[0],
                    'port': row[1],
                    'host': row[2],
                    'port': row[3]
                })
        return data

    async def add_host(self, host: str, port: int, protocol: str, status: str):
        async with self.__pool.acquire() as con:  # type: asyncpg.Connection
            print(host, port, protocol, status)
            await con.execute("""INSERT INTO hosts (host, port, protocol, status) values ($1, $2, $3, $4)""", host,
                              port, protocol, status)

            # await con.execute("""with new_host as (
            #         insert into hosts (host, port) values ($1, $2)
            #         returning host_id)
            # insert into user_host (login, host_id)
            # values( $3,  (select host_id from new_host));""", host, port, login)

    async def remove_host(self, login, host, port):
        async with self.__pool.acquire() as con:
            con.exequte()
