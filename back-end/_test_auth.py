import asyncio, sys

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.database.database import AsyncSessionLocal
from app.repositories.users import UserRepository
from app.services.auth import AuthService

async def main():
    async with AsyncSessionLocal() as session:
        repo = UserRepository(session)
        svc = AuthService(repo)
        try:
            result = await svc.authenticate("admin@awen.com", "admin123")
            print(f"Token: {result.access_token[:20]}...")
            print(f"User: {result.user.email}")
        except Exception as e:
            print(f"ERROR: {type(e).__name__}: {e}")

asyncio.run(main())
