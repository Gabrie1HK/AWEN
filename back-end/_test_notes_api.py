import httpx, asyncio, sys

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def test():
    async with httpx.AsyncClient(timeout=5) as c:
        # Login as driver
        r = await c.post("http://127.0.0.1:8001/api/v1/auth/login", json={"email":"conductor.pedro@awen.com","password":"123456"})
        token = r.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Get a parcel guide
        r = await c.get("http://127.0.0.1:8001/api/v1/parcels?pageSize=1", headers=headers)
        guide = r.json()["data"][0]["guide"]
        print(f"Guide: {guide}")

        # Add a note
        r = await c.post(f"http://127.0.0.1:8001/api/v1/parcels/{guide}/notes", headers=headers, json={"text": "Nota de prueba"})
        print(f"Add note status: {r.status_code}")
        if r.status_code == 201:
            print(f"Note created: {r.json()}")

        # Get notes
        r = await c.get(f"http://127.0.0.1:8001/api/v1/parcels/{guide}/notes", headers=headers)
        print(f"Notes: {r.json()}")

asyncio.run(test())
