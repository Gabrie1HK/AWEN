import httpx
import asyncio

async def main():
    url = "http://127.0.0.1:8000/api/v1/auth/login"
    body = {"email": "admin@awen.com", "password": "123456"}
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.post(url, json=body)
            print(f"Status: {r.status_code}")
            print(f"Response: {r.text[:500]}")
    except Exception as e:
        print(f"Error: {e}")

asyncio.run(main())
