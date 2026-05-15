from app.schemas.branch import BranchPublic


def seed_branches() -> list[BranchPublic]:
    return [
        BranchPublic(id=1, name="Sucursal Central", city="Santiago", address="Av. Libertador 1234", manager="Carlos Munoz", phone="+56 2 2123 4567", active=True),
        BranchPublic(id=2, name="Sucursal Norte", city="Antofagasta", address="Calle Comercio 567", manager="Maria Soto", phone="+56 55 2123 4567", active=True),
        BranchPublic(id=3, name="Sucursal Sur", city="Concepcion", address="Av. Los Carrera 890", manager="Pedro Torres", phone="+56 41 2123 4567", active=True),
        BranchPublic(id=4, name="Sucursal Este", city="Providencia", address="Av. Providencia 2345", manager="Ana Lopez", phone="+56 2 2345 6789", active=True),
        BranchPublic(id=5, name="Sucursal Costa", city="Valparaiso", address="Av. Errazuriz 678", manager="Jose Rivas", phone="+56 32 2123 4567", active=False),
        BranchPublic(id=6, name="Sucursal Austral", city="Punta Arenas", address="Av. Colon 901", manager="Luis Vargas", phone="+56 61 2123 4567", active=True),
    ]
