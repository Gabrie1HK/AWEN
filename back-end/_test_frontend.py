import httpx, asyncio

async def test():
    async with httpx.AsyncClient(timeout=5) as c:
        try:
            r = await c.get("http://[::1]:5173/")
            print(f"Frontend (IPv6): {r.status_code} {len(r.text)} bytes")
        except Exception as e:
            print(f"Frontend IPv6 error: {type(e).__name__}: {e}")
        try:
            r = await c.get("http://127.0.0.1:5173/")
            print(f"Frontend (IPv4): {r.status_code} {len(r.text)} bytes")
        except Exception as e:
            print(f"Frontend IPv4 error: {type(e).__name__}: {e}")

asyncio.run(test())
