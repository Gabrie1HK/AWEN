from app.schemas.user_management import UserPublic, UserRole


def seed_users_management() -> list[UserPublic]:
    return [
        UserPublic(id=1, name="Admin", last_name="Principal", ci="V-12345678", email="admin@awen.com", role=UserRole.ADMIN, branch="Sucursal Central", phone="+58 212 212 3456", active=True, lastLogin="2026-05-12 09:30"),
        UserPublic(id=2, name="Carlos", last_name="Operador", ci="V-23456789", email="operador.carlos@awen.com", role=UserRole.WAREHOUSE, branch="Sucursal Central", phone="+58 412 123 4567", active=True, lastLogin="2026-05-13 07:15"),
        UserPublic(id=3, name="Maria", last_name="Operador", ci="V-98765432", email="operador.maria@awen.com", role=UserRole.WAREHOUSE, branch="Sucursal Norte", phone="+58 416 765 4321", active=True, lastLogin="2026-05-12 22:40"),
        UserPublic(id=4, name="Pedro", last_name="Conductor", ci="V-34567890", email="conductor.pedro@awen.com", role=UserRole.DRIVER, branch="Sucursal Central", phone="+58 414 987 6543", active=True, lastLogin="2026-05-13 06:00"),
        UserPublic(id=5, name="Ana", last_name="Conductor", ci="V-56789012", email="conductor.ana@awen.com", role=UserRole.DRIVER, branch="Sucursal Sur", phone="+58 424 456 7890", active=True, lastLogin="2026-05-12 18:20"),
        UserPublic(id=6, name="Juan", last_name="Cliente", ci="V-67890123", email="juan@email.com", role=UserRole.CLIENT, branch=None, phone="+58 412 789 0123", address="Calle 60 123, Merida", active=True, lastLogin="2026-05-10 14:00"),
        UserPublic(id=7, name="Marta", last_name="Cliente", ci="V-78901234", email="marta@email.com", role=UserRole.CLIENT, branch=None, phone="+58 414 321 0987", address="Av. Bolivar 456, Merida", active=False, lastLogin="2026-04-28 11:30"),
    ]
