import httpx, asyncio, sys

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def test():
    async with httpx.AsyncClient(timeout=3) as c:
        try:
            r = await c.get("http://127.0.0.1:8001/api/v1/health")
            print(f"Health: {r.status_code}")
        except Exception as e:
            print(f"Error: {type(e).__name__}")

asyncio.run(test())
