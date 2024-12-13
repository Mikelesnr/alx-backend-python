#!/usr/bin/python3

import asyncio
import aiosqlite

async def async_fetch_users():
    async with aiosqlite.connect('example.db') as db:
        async with db.execute('SELECT * FROM users') as cursor:
            return await cursor.fetchall()

async def async_fetch_older_users():
    async with aiosqlite.connect('example.db') as db:
        async with db.execute('SELECT * FROM users WHERE age > 40') as cursor:
            return await cursor.fetchall()

async def fetch_concurrently():
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return results

if __name__ == "__main__":
    all_users, older_users = asyncio.run(fetch_concurrently())
    print("All Users:", all_users)
    print("Users older than 40:", older_users)
