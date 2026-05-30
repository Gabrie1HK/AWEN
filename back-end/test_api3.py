import asyncio
import sys
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi.testclient import TestClient
from app.main import app
from app.core.dependencies import get_current_user
from app.schemas.user import UserInDB

def override_get_current_user():
    return UserInDB(id=1, name='admin', email='admin@awen.com', role='Admin', hashed_password='foo', client_number=1)

app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)
res = client.get('/api/v1/users')
print('Status:', res.status_code)
print('Response:', res.text)
