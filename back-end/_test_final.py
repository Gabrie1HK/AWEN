import httpx, asyncio, sys

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def main():
    async with httpx.AsyncClient(timeout=5) as c:
        # Health
        r = await c.get("http://127.0.0.1:8001/api/v1/health")
        print(f"Health: {r.status_code}")

        # Login
        r = await c.post("http://127.0.0.1:8001/api/v1/auth/login", json={"email":"admin@awen.com","password":"123456"})
        data = r.json()
        token = data["access_token"]
        h = {"Authorization": f"Bearer {token}"}
        print(f"Login: {data['user']['name']} ({data['user']['role']})")

        # Parcels
        r = await c.get("http://127.0.0.1:8001/api/v1/parcels?pageSize=1", headers=h)
        guide = r.json()["data"][0]["guide"]
        print(f"Guide: {guide}")

        # Add note
        r = await c.post(f"http://127.0.0.1:8001/api/v1/parcels/{guide}/notes", headers=h, json={"text":"Test nota"})
        print(f"Add note: {r.status_code}")

        # Get notes
        r = await c.get(f"http://127.0.0.1:8001/api/v1/parcels/{guide}/notes", headers=h)
        print(f"Get notes: {r.json()}")

asyncio.run(main())
