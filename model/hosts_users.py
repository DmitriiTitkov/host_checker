from model import AbstractDBModule
import asyncpg
from asyncpg import Record


class HostsUsers(AbstractDBModule):
    async def add_user_host(self, host_id: int, user_id: int):
        async with self._pool.acquire() as con:  # type: asyncpg.connection.Connection
            res: Record = await con.fetchrow(
                """INSERT INTO users_hosts (host_id, user_id) VALUES ($1, $2);""",
                host_id, user_id)

    async def remove_user_host(self, host_id: int, user_id: int):
        # TODO: functionality for deletion the host from hosts if no users assigned; Probably need to add trigger to DB
        async with self._pool.acquire() as con:  # type: asyncpg.connection.Connection
            res: str = await con.execute(
                """DELETE FROM users_hosts WHERE host_id = $1 AND user_id = $2;""",
                host_id, user_id)
            return not res == "DELETE 0"
