import httpx, asyncio, sys

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def main():
    async with httpx.AsyncClient(timeout=5) as c:
        r = await c.post("http://127.0.0.1:8001/api/v1/auth/login", json={"email":"juan@email.com","password":"123456"})
        token = r.json()["access_token"]
        h = {"Authorization": f"Bearer {token}"}

        payload = {
            "sender": "Juan Perez",
            "senderId": "V-12345678",
            "senderPhone": "+58 414 111 2233",
            "recipient": "Maria Lopez",
            "recipientId": "V-87654321",
            "recipientPhone": "+58 416 999 8877",
            "recipientAddress": "Calle 5, Urb. Las Flores, Maracaibo",
            "originAddress": None,
            "originLat": 10.16,
            "originLng": -68.0,
            "destinationAddress": None,
            "destinationLat": 10.5,
            "destinationLng": -66.9,
            "originBranch": None,
            "destinationBranch": None,
            "weight": 2.5,
            "dimensions": "30x20x15 cm",
            "declaredValue": 50000,
            "description": "Documentos y libros",
        }
        r = await c.post("http://127.0.0.1:8001/api/v1/parcels", headers=h, json=payload)
        print(f"Status: {r.status_code}")
        print(f"Response: {r.text[:500]}")

asyncio.run(main())
