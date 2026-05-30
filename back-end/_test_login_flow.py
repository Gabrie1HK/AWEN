import asyncio, sys
if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.services.auth import AuthService
from app.repositories.users import SqlAlchemyUserRepository
from app.database.database import AsyncSessionLocal

async def main():
    async with AsyncSessionLocal() as session:
        repo = SqlAlchemyUserRepository(session)
        service = AuthService(repo)
        try:
            result = await service.authenticate("admin@awen.com", "123456")
            print(f"LOGIN OK: token={result.access_token[:20]}... user={result.user.name} role={result.user.role}")
        except Exception as e:
            print(f"LOGIN FAILED: {type(e).__name__}: {e}")

asyncio.run(main())
