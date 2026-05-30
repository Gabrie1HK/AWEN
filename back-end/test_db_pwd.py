import asyncio
import sys
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.database.database import AsyncSessionLocal
from sqlalchemy import text

async def main():
    async with AsyncSessionLocal() as session:
        res = await session.execute(text("SELECT id, email, active FROM users"))
        print('users:', res.fetchall())
        res = await session.execute(text("SELECT id, email, active FROM users_management"))
        print('users_management:', res.fetchall())

asyncio.run(main())
