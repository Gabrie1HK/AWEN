from app.schemas.branch import BranchPublic


def seed_branches() -> list[BranchPublic]:
    return [
        BranchPublic(id=1, name="Sucursal Central", city="Caracas", address="Av. Libertador 1234, Urb. El Rosal", manager="Carlos Munoz", phone="+58 212 212 3456", active=True),
        BranchPublic(id=2, name="Sucursal Norte", city="Maracaibo", address="Calle 72 con Av. 5 de Julio", manager="Maria Soto", phone="+58 261 212 3456", active=True),
        BranchPublic(id=3, name="Sucursal Sur", city="Ciudad Guayana", address="Av. Principal de Castillito", manager="Pedro Torres", phone="+58 286 212 3456", active=True),
        BranchPublic(id=4, name="Sucursal Este", city="Barcelona", address="Av. Fuerzas Armadas 2345", manager="Ana Lopez", phone="+58 281 234 5678", active=True),
        BranchPublic(id=5, name="Sucursal Costa", city="Maracay", address="Av. Las Delicias 678", manager="Jose Rivas", phone="+58 243 212 3456", active=False),
        BranchPublic(id=6, name="Sucursal Occidental", city="Barquisimeto", address="Av. Vargas con Carrera 19", manager="Luis Vargas", phone="+58 251 212 3456", active=True),
    ]
