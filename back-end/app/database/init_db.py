from __future__ import annotations

import asyncio
import sys

from app.database.database import AsyncSessionLocal, engine
from app.database.database import Base
from app.services.seed_loader import seed_all


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        await seed_all(session)


def main() -> None:
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(init_db())


if __name__ == "__main__":
    main()
