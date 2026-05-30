import asyncio
import sys
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.database.database import AsyncSessionLocal
from app.models.user import User
from sqlalchemy import select
from app.core.security import verify_password

async def main():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        for u in users:
            pwd = verify_password('awen123', u.hashed_password)
            print(f'{u.id}: {u.email} active={u.active} client_number={u.client_number} pwd_match={pwd}')

asyncio.run(main())
