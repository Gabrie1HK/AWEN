import asyncio
import sys
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
res = client.post('/api/v1/auth/login', json={'email': 'admin@awen.com', 'password': 'admin'})
if res.status_code == 200:
    token = res.json()['access_token']
    res2 = client.get('/api/v1/users', headers={'Authorization': f'Bearer {token}'})
    print('Users status:', res2.status_code)
    print('Users text:', res2.text)
else:
    print('Login failed:', res.text)
