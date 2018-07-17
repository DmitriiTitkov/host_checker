import asyncpg
from asyncpg import Record
import json


class Hosts:
    def __init__(self, pool: asyncpg.pool.Pool) -> None:
        self.__pool = pool

    async def get_hosts(self) -> list:
        async with self.__pool.acquire() as con:  # type: asyncpg.connection.Connection
            rows: list[Record] = await con.fetch("""
                SELECT * 
                FROM 
                    hosts
                """)
            data = [dict(r) for r in iter(rows)]
        return data

    async def add_host(self, host: str, port: int, protocol: str, status: str):
        async with self.__pool.acquire() as con:  # type: asyncpg.connection.Connection
            res: Record = await con.fetchrow(
                """INSERT INTO hosts (host, port, protocol, status) VALUES ($1, $2, $3, $4) RETURNING id;""",
                host, port, protocol, status)
            return dict(res)

    async def get_host(self, host_id: str) -> dict:
        async with self.__pool.acquire() as con:  # type: asyncpg.connection.Connection
            res: Record = await con.fetchrow("""
                SELECT * 
                FROM 
                    hosts
                WHERE id = $1
                """, host_id)
            return dict(res)

    async def update_host(self, host_id: int, host: str, port: int, protocol: str) -> dict:
        async with self.__pool.acquire() as con:  # type: asyncpg.connection.Connection
            res: Record = await con.fetchrow(
                """INSERT INTO hosts (id, host, port, protocol) VALUES ($1, $2, $3, $4) 
                ON CONFLICT (id) DO UPDATE SET host = $2, port = $3, protocol = $4 RETURNING id;""",
                host_id, host, port, protocol)
            return dict(res)

    async def remove_host(self, host_id: str) -> dict:
        async with self.__pool.acquire() as con:  # type: asyncpg.connection.Connection
            resp = await con.execute("""DELETE FROM hosts WHERE id = $1""", host_id)
            if resp == 'DELETE 0':
                return False
            return True
