import asyncio
import sys
if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.database.database import AsyncSessionLocal
from app.models.user import User
from sqlalchemy import select

async def main():
    async with AsyncSessionLocal() as s:
        r = await s.execute(select(User))
        users = r.scalars().all()
        print(f'Total users: {len(users)}')
        for u in users:
            print(f'{u.email} - {u.role}')

asyncio.run(main())
