from app.core.security import get_password_hash
from app.schemas.user import UserInDB


def seed_users() -> list[UserInDB]:
    password_hash = get_password_hash("123456")
    return [
        UserInDB(
            id=1,
            name="Admin Principal",
            email="admin@awen.cl",
            role="Admin",
            branch="Sucursal Central",
            active=True,
            hashed_password=password_hash,
        ),
        UserInDB(
            id=2,
            name="Operador Carlos",
            email="operador.carlos@awen.cl",
            role="Warehouse Operator",
            branch="Sucursal Central",
            active=True,
            hashed_password=password_hash,
        ),
        UserInDB(
            id=4,
            name="Conductor Pedro",
            email="conductor.pedro@awen.cl",
            role="Driver",
            branch="Sucursal Central",
            active=True,
            hashed_password=password_hash,
        ),
        UserInDB(
            id=6,
            name="Cliente Juan",
            email="juan@email.com",
            role="Client",
            branch=None,
            active=True,
            hashed_password=password_hash,
        ),
    ]
