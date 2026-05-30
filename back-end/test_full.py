import asyncio
import sys
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# 1) Login as admin
r = client.post('/api/v1/auth/login', json={'email': 'admin@awen.com', 'password': 'awen123'})
print('1. Admin login:', r.status_code)
if r.status_code == 200:
    token = r.json()['access_token']
    print('   user:', r.json()['user']['name'], 'role:', r.json()['user']['role'])

    # 2) Reset Marta's password
    r2 = client.patch('/api/v1/users/7/password', json={'new_password': 'marta2026'}, headers={'Authorization': f'Bearer {token}'})
    print('2. Reset Marta password:', r2.status_code, r2.text)

    # 3) Login as Marta
    r3 = client.post('/api/v1/auth/login', json={'email': 'marta@email.com', 'password': 'marta2026'})
    print('3. Marta login:', r3.status_code)
    if r3.status_code == 200:
        print('   user:', r3.json()['user']['name'], 'client_number:', r3.json()['user'].get('client_number'))
    else:
        print('   error:', r3.text)

    # 4) Login as Marta with old password (should fail)
    r4 = client.post('/api/v1/auth/login', json={'email': 'marta@email.com', 'password': 'awen123'})
    print('4. Marta old password (should fail):', r4.status_code)

    # 5) Toggle Marta inactive
    r5 = client.patch('/api/v1/users/7', json={'active': False}, headers={'Authorization': f'Bearer {token}'})
    print('5. Deactivate Marta:', r5.status_code)

    # 6) Login as Marta now (should fail - inactive)
    r6 = client.post('/api/v1/auth/login', json={'email': 'marta@email.com', 'password': 'marta2026'})
    print('6. Marta login after deactivation (should fail):', r6.status_code, r6.text)

    # 7) Reactivate Marta
    r7 = client.patch('/api/v1/users/7', json={'active': True}, headers={'Authorization': f'Bearer {token}'})
    print('7. Reactivate Marta:', r7.status_code)

    # 8) Login as Marta again (should work)
    r8 = client.post('/api/v1/auth/login', json={'email': 'marta@email.com', 'password': 'marta2026'})
    print('8. Marta login after reactivation (should work):', r8.status_code)
else:
    print('   error:', r.text)
