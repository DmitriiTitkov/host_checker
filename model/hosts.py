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
            data = [dict(r) for r in rows]
        return data

    async def get_hosts_for_user(self, login: str) -> list:
        async with self._pool.acquire() as con:  # type: asyncpg.connection.Connection
            rows: list[Record] = await con.fetch("""
                SELECT h.id, h.host, h.port, h.is_active
                FROM users u
                JOIN users_hosts uh ON u.id = uh.user_id
                JOIN hosts h ON h.id = uh.host_id
                WHERE login = $1;
                """, login)
            data = [dict(r) for r in iter(rows)]
        return data

    async def add_host(self, host: str, port: int) -> dict:
        try:
            async with self._pool.acquire() as con:  # type: asyncpg.connection.Connection
                res: Record = await con.fetchrow(
                    """INSERT INTO hosts (host, port) VALUES ($1, $2) 
                       RETURNING id;""",
                    host, port)
                return dict(res)
        except asyncpg.exceptions.UniqueViolationError:
            raise

    async def get_host_by_id(self, host_id: str) -> dict:
        async with self._pool.acquire() as con:  # type: asyncpg.connection.Connection
            res: Record = await con.fetchrow("""
                SELECT id, host, port, is_active  
                FROM 
                    hosts
                WHERE id = $1
                """, host_id)
            if res:
                return dict(res)


    async def get_host(self, host: str, port: int) -> dict:
        async with self._pool.acquire() as con:  # type: asyncpg.connection.Connection
            res: Record = await con.fetchrow("""
                SELECT id, host, port, is_active 
                FROM 
                    hosts
                WHERE host = $1 AND
                      port = $2
                """, host, port)
            return dict(res)

    async def update_host(self, host_id: int, host: str, port: int) -> bool:
        async with self._pool.acquire() as con:  # type: asyncpg.connection.Connection
            res: str= await con.execute(
                """ UPDATE hosts SET host = $2, port = $3 WHERE id = $1;""",
                host_id, host, port)
            if res == 'UPDATE 0':
                return False
            return True

    async def update_host_status(self, host_id: int, is_active: str) -> bool:
        async with self._pool.acquire() as con:  # type: asyncpg.connection.Connection
            res: str = await con.execute(
                """UPDATE hosts SET is_active = $2 WHERE id = $1;""",
                host_id, is_active)
            if res == 'UPDATE 0':
                return False
            return True


    async def remove_host(self, host_id: str) -> bool:
        async with self._pool.acquire() as con:  # type: asyncpg.connection.Connection
            res = await con.execute("""DELETE FROM hosts WHERE id = $1""", host_id)
            if res == 'DELETE 0':
                return False
            return True
