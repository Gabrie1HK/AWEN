import asyncio
import sys
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.database.database import AsyncSessionLocal
from app.models.user_management import UserManagement
from sqlalchemy import select
from app.core.security import get_password_hash

async def main():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(UserManagement).where(UserManagement.id == 1))
        admin = result.scalar_one_or_none()
        if admin:
            admin.active = True
            admin.hashed_password = get_password_hash('awen123')
            print('Admin management updated')
        await session.commit()

asyncio.run(main())
