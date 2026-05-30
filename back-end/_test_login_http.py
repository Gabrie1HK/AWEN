import httpx, asyncio, sys

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def test():
    async with httpx.AsyncClient(timeout=5) as c:
        r = await c.post("http://127.0.0.1:8001/api/v1/auth/login", json={"email":"admin@awen.com","password":"123456"})
        print(f"Status: {r.status_code}")
        data = r.json()
        print(f"User: {data['user']['name']} - Role: {data['user']['role']}")
        print(f"Token: {data['access_token'][:30]}...")

asyncio.run(test())
