import asyncpg
from typing import Union, Dict
from model import AbstractDBModule

class Users(AbstractDBModule):
    async def get_users(self) -> list:
        async with self._pool.acquire() as con:
            rows = await con.fetch("""
                SELECT
                    id, 
                    login 
                FROM 
                    users
                """)
            return [dict(r) for r in rows]

    async def add_user(self, login: str, password: str) -> dict:
        async with self._pool.acquire() as con:  # type: asyncpg.Connection
            res: asyncpg.Record = await con.fetchrow(
                """INSERT INTO users (login, password) VALUES ($1, $2) RETURNING id;""", login, password)
            return dict(res)

    async def get_user(self, user_name: str) -> Union[Dict[str, str], None]:
        async with self._pool.acquire() as con:
            row = await con.fetchrow("""
                SELECT 
                    id,
                    login,
                    password 
                FROM 
                    users
                WHERE
                    login = $1
                """, user_name)
            if row:
                return {
                    'id': row[0],
                    'login': row[1],
                    'password': row[2]
                }
            return None
