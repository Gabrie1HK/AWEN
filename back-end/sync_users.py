import asyncio
import sys
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.database.database import AsyncSessionLocal
from app.models.user import User
from app.models.user_management import UserManagement
from sqlalchemy import select
from app.core.security import get_password_hash

async def main():
    async with AsyncSessionLocal() as session:
        # Get all users_management
        result = await session.execute(select(UserManagement))
        mgmt_users = result.scalars().all()
        
        # Get all auth users
        result = await session.execute(select(User))
        auth_users = {u.id: u for u in result.scalars().all()}
        
        default_pwd = get_password_hash("awen123")
        
        for m_u in mgmt_users:
            if m_u.id not in auth_users:
                print(f"Creating missing auth user: {m_u.email}")
                new_u = User(
                    id=m_u.id,
                    name=m_u.name,
                    email=m_u.email,
                    role=m_u.role,
                    branch=m_u.branch,
                    phone=m_u.phone,
                    address=m_u.address,
                    active=m_u.active,
                    hashed_password=m_u.hashed_password or default_pwd
                )
                session.add(new_u)
            else:
                # Sync fields
                a_u = auth_users[m_u.id]
                a_u.name = m_u.name
                a_u.email = m_u.email
                a_u.role = m_u.role
                a_u.branch = m_u.branch
                a_u.phone = m_u.phone
                a_u.address = m_u.address
                a_u.active = m_u.active
                if m_u.hashed_password:
                    a_u.hashed_password = m_u.hashed_password
        
        await session.commit()
        print("Done syncing.")

asyncio.run(main())
