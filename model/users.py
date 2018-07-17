import asyncpg
from typing import Union, Dict


class Users:
    def __init__(self, pool: asyncpg.pool.Pool) -> None:
        self.__pool = pool

    async def get_users(self) -> list:
        async with self.__pool.acquire() as con:
            rows = await con.fetch("""
                SELECT 
                    login,
                    password 
                FROM 
                    users
                """)
            data = [r["login"] for r in iter(rows)]
        return data

    async def add_user(self, login: str, password: str) -> dict:
        async with self.__pool.acquire() as con:  # type: asyncpg.Connection
            res: asyncpg.Record = await con.fetchrow(
                """INSERT INTO users (login, password) VALUES ($1, $2) RETURNING id;""", login, password)
            return dict(res)

    async def get_user(self, user_name: str) -> Union[Dict[str, str], None]:
        async with self.__pool.acquire() as con:
            row = await con.fetchrow("""
                SELECT 
                    login,
                    password 
                FROM 
                    users
                WHERE
                    login = $1
                """, user_name)
            if row:
                return {
                    'login': row[0],
                    'password': row[1]
                }
            return None
