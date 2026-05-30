import asyncio
from app.database.database import get_db, AsyncSessionLocal
from sqlalchemy import text

async def main():
    async with AsyncSessionLocal() as session:
        try:
            res = await session.execute(text('SELECT * FROM users_management limit 1'))
            print('ok', res.fetchall())
        except Exception as e:
            print('error', e)

asyncio.run(main())
