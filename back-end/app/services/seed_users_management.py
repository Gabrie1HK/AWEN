from app.schemas.user_management import UserPublic, UserRole


def seed_users_management() -> list[UserPublic]:
    return [
        UserPublic(id=1, name="Admin Principal", email="admin@awen.com", role=UserRole.ADMIN, branch="Sucursal Central", phone="+58 212 212 3456", active=True, lastLogin="2026-05-12 09:30"),
        UserPublic(id=2, name="Operador Carlos", email="operador.carlos@awen.com", role=UserRole.WAREHOUSE, branch="Sucursal Central", phone="+58 412 123 4567", active=True, lastLogin="2026-05-13 07:15"),
        UserPublic(id=3, name="Operador Maria", email="operador.maria@awen.com", role=UserRole.WAREHOUSE, branch="Sucursal Norte", phone="+58 416 765 4321", active=True, lastLogin="2026-05-12 22:40"),
        UserPublic(id=4, name="Conductor Pedro", email="conductor.pedro@awen.com", role=UserRole.DRIVER, branch="Sucursal Central", phone="+58 414 987 6543", active=True, lastLogin="2026-05-13 06:00"),
        UserPublic(id=5, name="Conductor Ana", email="conductor.ana@awen.com", role=UserRole.DRIVER, branch="Sucursal Sur", phone="+58 424 456 7890", active=True, lastLogin="2026-05-12 18:20"),
        UserPublic(id=6, name="Cliente Juan", email="juan@email.com", role=UserRole.CLIENT, branch=None, phone="+58 412 789 0123", address="Calle 60 123, Merida", active=True, lastLogin="2026-05-10 14:00"),
        UserPublic(id=7, name="Cliente Marta", email="marta@email.com", role=UserRole.CLIENT, branch=None, phone="+58 414 321 0987", address="Av. Bolivar 456, Merida", active=False, lastLogin="2026-04-28 11:30"),
    ]
