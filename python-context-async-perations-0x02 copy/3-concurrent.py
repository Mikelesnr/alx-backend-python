#!/myenv/bin/python3

import aiosqlite
import asyncio

async def async_fetch_users(db_name):
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            return users

async def async_fetch_older_users(db_name):
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            older_users = await cursor.fetchall()
            return older_users

async def fetch_concurrently():
    db_name = 'example.db'
    results = await asyncio.gather(
        async_fetch_users(db_name),
        async_fetch_older_users(db_name)
    )
    all_users, older_users = results
    print("All Users:")
    for user in all_users:
        print(user)
    print("\nUsers Older Than 40:")
    for user in older_users:
        print(user)

# Run the concurrent fetch
asyncio.run(fetch_concurrently())
