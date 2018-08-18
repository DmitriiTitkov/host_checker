import asyncpg


class AbstractDBModule:
    def __init__(self, pool: asyncpg.pool.Pool) -> None:
        self._pool = pool


class Database(AbstractDBModule):
    def __init__(self, pool: asyncpg.pool.Pool) -> None:
        super().__init__(pool)
        from .users import Users
        from .hosts import Hosts
        from .hosts_users import HostsUsers
        self.users = Users(self._pool)
        self.hosts = Hosts(self._pool)
        self.hosts_users = HostsUsers(self._pool)

    async def close(self) -> None:
        await self._pool.close()

