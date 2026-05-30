import httpx, asyncio, sys

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def main():
    async with httpx.AsyncClient(timeout=3) as c:
        try:
            r = await c.get("http://127.0.0.1:8001/api/v1/health")
            print(f"OK: {r.status_code}")
        except httpx.TimeoutException:
            print("TIMEOUT")
        except Exception as e:
            print(f"ERROR: {e}")

asyncio.run(main())
