import asyncpg
from asyncpg import Record, exceptions
from model import AbstractDBModule

class Hosts(AbstractDBModule):
    async def get_hosts(self) -> list:
        async with self._pool.acquire() as con:  # type: asyncpg.connection.Connection
            rows: list[Record] = await con.fetch("""
                SELECT * 
                FROM 
                    hosts
                """)
            data = [dict(r) for r in iter(rows)]
        return data

    async def get_hosts_for_user(self, login: str) -> list:
        async with self._pool.acquire() as con:  # type: asyncpg.connection.Connection
            rows: list[Record] = await con.fetch("""
                SELECT h.host, h.port, h.protocol, h.status
                FROM users u
                JOIN users_hosts uh ON u.id = uh.user_id
                JOIN hosts h ON h.id = uh.host_id
                WHERE login = $1;
                """, login)
            data = [dict(r) for r in iter(rows)]
        return data

    async def add_host(self, host: str, port: int, protocol: str):
        try:
            async with self._pool.acquire() as con:  # type: asyncpg.connection.Connection
                res: Record = await con.fetchrow(
                    """INSERT INTO hosts (host, port, protocol) VALUES ($1, $2, $3) ON CONFLICT DO NOTHING RETURNING id SELECT 'i' AS source, id""",
                    host, port, protocol)
                return dict(res)
        except asyncpg.exceptions.UniqueViolationError:
            raise

    async def get_host(self, host_id: str) -> dict:
        async with self._pool.acquire() as con:  # type: asyncpg.connection.Connection
            res: Record = await con.fetchrow("""
                SELECT * 
                FROM 
                    hosts
                WHERE id = $1
                """, host_id)
            return dict(res)

    async def update_host(self, host_id: int, host: str, port: int, protocol: str) -> dict:
        async with self._pool.acquire() as con:  # type: asyncpg.connection.Connection
            res: Record = await con.fetchrow(
                """INSERT INTO hosts (id, host, port, protocol) VALUES ($1, $2, $3, $4) 
                ON CONFLICT (id) DO UPDATE SET host = $2, port = $3, protocol = $4 RETURNING id;""",
                host_id, host, port, protocol)
            return dict(res)

    async def remove_host(self, host_id: str) -> dict:
        async with self._pool.acquire() as con:  # type: asyncpg.connection.Connection
            resp = await con.execute("""DELETE FROM hosts WHERE id = $1""", host_id)
            if resp == 'DELETE 0':
                return False
            return True


    async def get_host_by_name(self, host_name: str) -> dict:
        async with self._pool.acquire() as con:  # type: asyncpg.connection.Connection
            res: Record = await con.fetchrow("""
                SELECT * 
                FROM 
                    hosts
                WHERE host = $1
                """, host_name)
            return dict(res)