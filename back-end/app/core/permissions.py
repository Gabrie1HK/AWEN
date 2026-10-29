"""
Matriz centralizada de permisos por rol (R3).

Este módulo define qué roles pueden acceder a qué endpoints.
Es la única fuente de verdad para la autorización (RBAC).
"""

from typing import Dict, Set


# Definición de roles válidos
class Role:
    ADMIN = "Admin"
    WAREHOUSE_OPERATOR = "Warehouse Operator"
    DRIVER = "Driver"
    CLIENT = "Client"

    ALL = [ADMIN, WAREHOUSE_OPERATOR, DRIVER, CLIENT]


# Matriz de permisos: endpoint_path -> set de roles permitidos
# Los paths que terminan en / son prefijos (match por startswith)
# Los paths con {param} son patrones con placeholders
# Los paths sin / al final y sin placeholders son coincidencias exactas
PERMISSION_MATRIX: Dict[str, Set[str]] = {
    # ===== PARCELS =====
    # Listar encomiendas
    "GET /api/v1/parcels": {Role.ADMIN, Role.WAREHOUSE_OPERATOR, Role.DRIVER, Role.CLIENT},
    # Obtener/actualizar/eliminar encomienda por ID (prefijo)
    "GET /api/v1/parcels/": {Role.ADMIN, Role.WAREHOUSE_OPERATOR, Role.DRIVER, Role.CLIENT},
    "PATCH /api/v1/parcels/": {Role.ADMIN, Role.WAREHOUSE_OPERATOR},
    "DELETE /api/v1/parcels/": {Role.ADMIN},
    # Crear encomienda
    "POST /api/v1/parcels": {Role.ADMIN, Role.WAREHOUSE_OPERATOR, Role.CLIENT},
    # Cambiar estado (driver puede solo "en ruta" -> "entregado")
    "POST /api/v1/parcels/{id}/status": {Role.ADMIN, Role.WAREHOUSE_OPERATOR, Role.DRIVER},
    # Cancelar encomienda
    "POST /api/v1/parcels/{id}/cancel": {Role.ADMIN, Role.WAREHOUSE_OPERATOR, Role.CLIENT},
    # Notas de encomienda
    "POST /api/v1/parcels/{guide}/notes": {Role.ADMIN, Role.WAREHOUSE_OPERATOR, Role.DRIVER, Role.CLIENT},
    "GET /api/v1/parcels/{guide}/notes": {Role.ADMIN, Role.WAREHOUSE_OPERATOR, Role.DRIVER, Role.CLIENT},
    # Subir evidencia
    "POST /api/v1/parcels/upload-evidence": {Role.ADMIN, Role.WAREHOUSE_OPERATOR, Role.DRIVER, Role.CLIENT},
    # Mis encomiendas (cliente)
    "GET /api/v1/parcels/my-parcels": {Role.ADMIN, Role.DRIVER, Role.CLIENT},
    # Tracking por guía (público)
    "GET /api/v1/parcels/{guide}/tracking": set(),

    # ===== TRACKING PÚBLICO =====
    "GET /api/v1/tracking/": set(),

    # ===== USERS =====
    # Listar usuarios
    "GET /api/v1/users": {Role.ADMIN, Role.WAREHOUSE_OPERATOR},
    # Mi perfil
    "GET /api/v1/users/me": {Role.ADMIN, Role.WAREHOUSE_OPERATOR, Role.DRIVER, Role.CLIENT},
    "PATCH /api/v1/users/me": {Role.ADMIN, Role.WAREHOUSE_OPERATOR, Role.DRIVER, Role.CLIENT},
    # Usuario por ID (prefijo)
    "GET /api/v1/users/": {Role.ADMIN, Role.WAREHOUSE_OPERATOR},
    "PATCH /api/v1/users/": {Role.ADMIN},
    "DELETE /api/v1/users/": {Role.ADMIN},
    # Crear usuario
    "POST /api/v1/users": {Role.ADMIN},
    # Cambiar contraseña (admin)
    "PATCH /api/v1/users/password": {Role.ADMIN},

    # ===== BRANCHES =====
    "GET /api/v1/branches": {Role.ADMIN, Role.WAREHOUSE_OPERATOR, Role.DRIVER},
    "GET /api/v1/branches/": {Role.ADMIN, Role.WAREHOUSE_OPERATOR, Role.DRIVER},
    "POST /api/v1/branches": {Role.ADMIN},
    "PATCH /api/v1/branches/": {Role.ADMIN},
    "DELETE /api/v1/branches/": {Role.ADMIN},

    # ===== DELIVERIES (POD) =====
    "GET /api/v1/deliveries": {Role.ADMIN, Role.WAREHOUSE_OPERATOR, Role.DRIVER, Role.CLIENT},
    "GET /api/v1/deliveries/": {Role.ADMIN, Role.WAREHOUSE_OPERATOR, Role.DRIVER, Role.CLIENT},
    "PATCH /api/v1/deliveries/": {Role.ADMIN, Role.WAREHOUSE_OPERATOR},
    # Prefijo para /deliveries/{id}/pod
    "POST /api/v1/deliveries/{id}/pod": {Role.ADMIN, Role.WAREHOUSE_OPERATOR, Role.DRIVER},
    # Prefijo para /deliveries/{id}/upload
    "POST /api/v1/deliveries/{id}/upload": {Role.ADMIN, Role.WAREHOUSE_OPERATOR, Role.DRIVER, Role.CLIENT},

    # ===== LOGISTICS =====
    "GET /api/v1/logistics/batches": {Role.ADMIN, Role.WAREHOUSE_OPERATOR, Role.DRIVER},
    "GET /api/v1/logistics/batches/": {Role.ADMIN, Role.WAREHOUSE_OPERATOR, Role.DRIVER},
    "POST /api/v1/logistics/batches": {Role.ADMIN, Role.WAREHOUSE_OPERATOR},
    "PATCH /api/v1/logistics/batches/": {Role.ADMIN, Role.WAREHOUSE_OPERATOR},
    # Prefijo para /logistics/batches/{id}/assign
    "POST /api/v1/logistics/batches/{id}/assign": {Role.ADMIN, Role.WAREHOUSE_OPERATOR},
    "GET /api/v1/logistics/vehicles": {Role.ADMIN, Role.WAREHOUSE_OPERATOR, Role.DRIVER},
    "POST /api/v1/logistics/vehicles": {Role.ADMIN, Role.WAREHOUSE_OPERATOR},

    # ===== NOTIFICATIONS =====
    "GET /api/v1/notifications": {Role.ADMIN, Role.WAREHOUSE_OPERATOR, Role.DRIVER, Role.CLIENT},
    # Prefijo para /notifications/{id}/read
    "PATCH /api/v1/notifications/{id}/read": {Role.ADMIN, Role.WAREHOUSE_OPERATOR, Role.DRIVER, Role.CLIENT},
    "PATCH /api/v1/notifications/read-all": {Role.ADMIN, Role.WAREHOUSE_OPERATOR, Role.DRIVER, Role.CLIENT},
    "GET /api/v1/notifications/stream": {Role.ADMIN, Role.WAREHOUSE_OPERATOR, Role.DRIVER, Role.CLIENT},

    # ===== REPORTS / DASHBOARD =====
    "GET /api/v1/reports/kpis": {Role.ADMIN, Role.WAREHOUSE_OPERATOR},
    "GET /api/v1/reports/daily-volume": {Role.ADMIN, Role.WAREHOUSE_OPERATOR},
    "GET /api/v1/reports/deliveries-by-branch": {Role.ADMIN, Role.WAREHOUSE_OPERATOR},
    "GET /api/v1/reports/activity": {Role.ADMIN, Role.WAREHOUSE_OPERATOR},
    "GET /api/v1/reports/summary": {Role.ADMIN, Role.WAREHOUSE_OPERATOR},
    "GET /api/v1/reports/top-routes": {Role.ADMIN, Role.WAREHOUSE_OPERATOR},
    "GET /api/v1/reports/export": {Role.ADMIN, Role.WAREHOUSE_OPERATOR},
    "GET /api/v1/dashboard": {Role.ADMIN, Role.WAREHOUSE_OPERATOR, Role.DRIVER},

    # ===== MAPS =====
    "GET /api/v1/maps/route": {Role.ADMIN, Role.WAREHOUSE_OPERATOR, Role.DRIVER, Role.CLIENT},

    # ===== AUTH =====
    "POST /api/v1/auth/login": set(),  # público
    "GET /api/v1/auth/me": {Role.ADMIN, Role.WAREHOUSE_OPERATOR, Role.DRIVER, Role.CLIENT},

    # ===== HEALTH =====
    "GET /api/v1/health": set(),  # público
}


# Endpoints que son públicos (no requieren autenticación)
# Estos paths se usan para match exacto, prefijo (si terminan en /) o placeholder {param}
PUBLIC_ENDPOINTS: Set[str] = {
    "POST /api/v1/auth/login",
    "GET /api/v1/parcels/{guide}/tracking",  # tracking por guía
    "GET /api/v1/tracking/",  # tracking público (prefijo)
    "GET /api/v1/health",
    "GET /api/v1/maps/route",
}


def get_required_roles(method: str, path: str) -> Set[str] | None:
    """
    Obtiene los roles requeridos para un endpoint dado.

    Args:
        method: Método HTTP (GET, POST, PATCH, DELETE)
        path: Path completo del endpoint (ej: /api/v1/parcels/ENV-001)

    Returns:
        Set de roles permitidos. Set vacío = público (no requiere auth).
        None = endpoint no encontrado en matriz (denegar por defecto).
    """
    # Normalizar path: remover query params y trailing slashes
    normalized_path = _normalize_path(path)
    key = f"{method} {normalized_path}"

    # Buscar coincidencia exacta
    if key in PERMISSION_MATRIX:
        return PERMISSION_MATRIX[key]

    # Buscar por prefijo (para paths con IDs variables)
    for matrix_key, roles in PERMISSION_MATRIX.items():
        matrix_method, matrix_path = matrix_key.split(" ", 1)
        if matrix_method == method and _path_matches(normalized_path, matrix_path):
            return roles

    # Endpoint no definido en matriz -> denegar por seguridad
    return None


def is_public_endpoint(method: str, path: str) -> bool:
    """Verifica si un endpoint es público (no requiere autenticación)."""
    normalized_path = _normalize_path(path)
    key = f"{method} {normalized_path}"

    # Match exacto en PUBLIC_ENDPOINTS
    if key in PUBLIC_ENDPOINTS:
        return True

    # Match por prefijo en PUBLIC_ENDPOINTS
    for pub in PUBLIC_ENDPOINTS:
        pub_method, pub_path = pub.split(" ", 1)
        if pub_method == method and _path_matches(normalized_path, pub_path):
            return True

    return False


def _normalize_path(path: str) -> str:
    """Normaliza el path removiendo query params y trailing slashes."""
    # Remover query string
    if "?" in path:
        path = path.split("?")[0]
    # Remover trailing slash excepto root
    if path != "/" and path.endswith("/"):
        path = path[:-1]
    return path


def _path_matches(request_path: str, matrix_path: str) -> bool:
    """
    Verifica si el path de la request coincide con el patrón de la matriz.

    La matriz puede tener patrones como:
    - /api/v1/parcels (exacto)
    - /api/v1/parcels/ (prefijo para /api/v1/parcels/ENV-001, /api/v1/parcels/ENV-001/tracking, etc.)
    - /api/v1/parcels/{id}/status (patrón con placeholder para POST /parcels/ENV-001/status)
    """
    # Si el path de la matriz termina en /, es un prefijo simple
    if matrix_path.endswith("/"):
        return request_path.startswith(matrix_path)

    # Si el path de la matriz contiene placeholders {param}, convertir a regex
    if "{" in matrix_path and "}" in matrix_path:
        # Convertir {param} a regex que coincida con un segmento de path
        import re
        pattern = matrix_path
        # Escapar caracteres especiales de regex excepto { y }
        pattern = re.escape(pattern)
        # Reemplazar \{param\} con regex para un segmento
        pattern = pattern.replace(r"\{", "{").replace(r"\}", "}")
        pattern = re.sub(r"\{[^}]+\}", r"[^/]+", pattern)
        # Anclar al inicio y final
        pattern = "^" + pattern + "$"
        return bool(re.match(pattern, request_path))

    # Coincidencia exacta
    return request_path == matrix_path


def user_has_permission(user_role: str, method: str, path: str) -> bool:
    """
    Verifica si un usuario con el rol dado tiene permiso para el endpoint.

    Args:
        user_role: Rol del usuario (ej: "Admin", "Client")
        method: Método HTTP
        path: Path del endpoint

    Returns:
        True si tiene permiso, False en caso contrario.
    """
    # Endpoint público -> permitir
    if is_public_endpoint(method, path):
        return True

    required_roles = get_required_roles(method, path)

    # Endpoint no definido en matriz -> denegar
    if required_roles is None:
        return False

    # Si no requiere roles específicos (set vacío pero no público), permitir autenticados
    if not required_roles:
        return True

    return user_role in required_roles