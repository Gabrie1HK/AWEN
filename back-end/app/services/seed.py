from app.core.security import get_password_hash
from app.schemas.user import UserInDB


def seed_users() -> list[UserInDB]:
    password_hash = get_password_hash("123456")
    return [
        UserInDB(
            id=1,
            name="Admin",
            last_name="Principal",
            ci="V-12345678",
            email="admin@awen.com",
            role="Admin",
            branch="Sucursal Central",
            phone="+58 212 212 3456",
            address="Av. Libertador 1234, Caracas",
            active=True,
            hashed_password=password_hash,
        ),
        UserInDB(
            id=2,
            name="Carlos",
            last_name="Operador",
            ci="V-23456789",
            email="operador.carlos@awen.com",
            role="Warehouse Operator",
            branch="Sucursal Central",
            phone="+58 412 123 4567",
            address="Urb. El Rosal, Caracas",
            active=True,
            hashed_password=password_hash,
        ),
        UserInDB(
            id=4,
            name="Pedro",
            last_name="Conductor",
            ci="V-34567890",
            email="conductor.pedro@awen.com",
            role="Driver",
            branch="Sucursal Central",
            phone="+58 414 987 6543",
            address="Av. Universidad 742, Caracas",
            active=True,
            hashed_password=password_hash,
        ),
        UserInDB(
            id=6,
            name="Juan",
            last_name="Cliente",
            ci="V-67890123",
            email="juan@email.com",
            role="Client",
            branch=None,
            phone="+58 412 789 0123",
            address="Calle 60 123, Merida",
            active=True,
            hashed_password=password_hash,
        ),
    ]
