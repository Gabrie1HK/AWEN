import httpx, asyncio

async def test():
    async with httpx.AsyncClient(timeout=5) as c:
        # Test through vite proxy (frontend -> proxy -> backend)
        r = await c.get("http://127.0.0.1:5173/api/v1/health")
        print(f"Via proxy: {r.status_code} {r.text[:200]}")

asyncio.run(test())
