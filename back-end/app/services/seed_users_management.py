from app.schemas.user_management import UserPublic, UserRole


def seed_users_management() -> list[UserPublic]:
    return [
        UserPublic(id=1, name="Admin Principal", email="admin@awen.cl", role=UserRole.ADMIN, branch="Sucursal Central", active=True, lastLogin="2026-05-12 09:30"),
        UserPublic(id=2, name="Operador Carlos", email="operador.carlos@awen.cl", role=UserRole.WAREHOUSE, branch="Sucursal Central", active=True, lastLogin="2026-05-13 07:15"),
        UserPublic(id=3, name="Operador Maria", email="operador.maria@awen.cl", role=UserRole.WAREHOUSE, branch="Sucursal Norte", active=True, lastLogin="2026-05-12 22:40"),
        UserPublic(id=4, name="Conductor Pedro", email="conductor.pedro@awen.cl", role=UserRole.DRIVER, branch="Sucursal Central", active=True, lastLogin="2026-05-13 06:00"),
        UserPublic(id=5, name="Conductor Ana", email="conductor.ana@awen.cl", role=UserRole.DRIVER, branch="Sucursal Sur", active=True, lastLogin="2026-05-12 18:20"),
        UserPublic(id=6, name="Cliente Juan", email="juan@email.com", role=UserRole.CLIENT, branch=None, active=True, lastLogin="2026-05-10 14:00"),
        UserPublic(id=7, name="Cliente Marta", email="marta@email.com", role=UserRole.CLIENT, branch=None, active=False, lastLogin="2026-04-28 11:30"),
    ]
