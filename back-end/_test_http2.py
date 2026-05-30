import httpx, asyncio, traceback

async def main():
    url = "http://127.0.0.1:8000/api/v1/health"
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(url)
            print(f"Status: {r.status_code}")
            print(f"Response: {r.text[:200]}")
    except httpx.TimeoutException:
        print("TIMEOUT - server not responding")
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")
        traceback.print_exc()

asyncio.run(main())
