from app.core.security import get_password_hash
from app.schemas.user import UserInDB


def seed_users() -> list[UserInDB]:
    password_hash = get_password_hash("123456")
    return [
        UserInDB(
            id=1,
            name="Admin Principal",
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
            name="Operador Carlos",
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
            name="Conductor Pedro",
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
            name="Cliente Juan",
            email="juan@email.com",
            role="Client",
            branch=None,
            phone="+58 412 789 0123",
            address="Calle 60 123, Merida",
            active=True,
            hashed_password=password_hash,
        ),
    ]
