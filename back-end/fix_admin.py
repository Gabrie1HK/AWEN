import asyncio
import sys
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.database.database import AsyncSessionLocal
from app.models.user import User
from sqlalchemy import select
from app.core.security import get_password_hash

async def main():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.id == 1))
        admin = result.scalar_one_or_none()
        if admin:
            admin.active = True
            admin.hashed_password = get_password_hash('awen123')
            print('Admin updated: active=True, password=awen123')
        await session.commit()

asyncio.run(main())
