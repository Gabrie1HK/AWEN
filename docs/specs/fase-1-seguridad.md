---
fase: 1
nombre: seguridad
estado: aprobada
rama: fix/fase-1-seguridad
autor: Gabriel Espinoza
fecha: 2026-10-29
---

# Fase 1 — Seguridad y autorización

> **Estado: aprobada.** Preguntas resueltas. Se puede crear rama, escribir tests RED e implementar.

## 1. Contexto y problema

La API ya autentica con JWT, pero **no autoriza por rol**: cualquier usuario autenticado puede
llamar a cualquier endpoint protegido. Los cuatro roles del sistema (Admin, Warehouse Operator,
Driver, Client) existen en los datos pero no se aplican en las rutas. Además hay detalles de
endurecimiento pendientes (rate limit en memoria, mensajes inconsistentes, secretos por defecto).

## 2. Alcance

### Dentro del alcance

- Autorización por rol en los endpoints que lo requieran (matriz definida abajo).
- Endurecimiento de la autenticación existente (usuario inactivo, secret key obligatoria).
- Tests de autorización (no solo de autenticación).

### Fuera del alcance (no-goals)

- Reescritura del modelo de usuarios.
- OAuth externo / SSO.
- Refresh tokens (se posponen a fase 2).
- Rate limit distribuido con Redis (se pospone; R6 = could).
- Cambios de UI más allá de reflejar los 403.

## 3. Comportamiento actual

| Área | Estado actual | Referencia |
| --- | --- | --- |
| Hash de password | bcrypt (`hashpw`/`checkpw`) | `back-end/app/core/security.py:10` |
| Token | JWT HS256 con `sub` y `exp`; expiración 60 min | `back-end/app/core/security.py:18` |
| Login | `POST /api/v1/auth/login` devuelve token | `back-end/app/api/routes/auth.py:12` |
| Usuario actual | `GET /api/v1/auth/me` | `back-end/app/api/routes/auth.py:18` |
| Protección | `get_current_user` vía `OAuth2PasswordBearer` | `back-end/app/core/dependencies.py:82` |
| Autorización por rol | **No existe**. Las rutas solo verifican autenticación | `_user=Depends(get_current_user)` en todas las rutas |
| `ForbiddenError` | Definido pero sin uso en rutas | `back-end/app/core/errors.py:22` |
| Rate limit | 100 req / 60 s por IP, en memoria, por proceso | `back-end/app/core/ratelimit.py:10` |
| CORS | Orígenes por `AWEN_CORS_ORIGINS` | `back-end/app/main.py:44` |
| Secret key | `CHANGE_ME` por defecto en config | `back-end/app/core/config.py:16` |

Los tests actuales de `back-end/tests/test_authorization.py` solo comprueban 401 sin token o con
token inválido; no comprueban 403 por rol.

## 4. Comportamiento deseado

Cada endpoint declara qué roles pueden usarlo. Un usuario autenticado sin permiso recibe `403`
con un mensaje claro. Un usuario no autenticado sigue recibiendo `401`.

## 5. Requisitos

| ID | Requisito | Prioridad |
| --- | --- | --- |
| R1 | Un usuario sin token o con token inválido recibe `401` en todo endpoint protegido (comportamiento actual, se mantiene). | must |
| R2 | Un usuario autenticado sin el rol requerido recibe `403`. | must |
| R3 | La matriz de permisos por rol está declarada en un único lugar y es testeable. | must |
| R4 | Un usuario con `active = false` no puede autenticarse ni usar un token vigente. | must |
| R5 | El arranque falla si `AWEN_SECRET_KEY` es el valor por defecto `CHANGE_ME` (sin excepción para dev). | should |
| R6 | Rate limit distribuido con Redis. | could (pospuesto) |

## 6. Matriz de permisos (para R2 y R3)

| Endpoint / Área | Admin | Warehouse Operator | Driver | Client |
|---|---|---|---|---|
| **Parcels** | | | | |
| `GET /api/v1/parcels` (listar) | ✅ | ✅ | ✅ (solo sus lotes) | ✅ (solo propias) |
| `GET /api/v1/parcels/{id}` | ✅ | ✅ | ✅ (si está en sus lotes) | ✅ (si es suya) |
| `POST /api/v1/parcels` (crear) | ✅ | ✅ | ❌ | ✅ |
| `PATCH /api/v1/parcels/{id}` | ✅ | ✅ | ❌ | ❌ |
| `POST /api/v1/parcels/{id}/status` | ✅ | ✅ | ✅ (solo "en ruta" → "entregado") | ❌ |
| `POST /api/v1/parcels/{id}/cancel` | ✅ | ✅ | ❌ | ✅ (solo propias y en estado "pendiente") |
| **Tracking** | | | | |
| `GET /api/v1/parcels/{tracking}/tracking` | público | público | público | público |
| **Users** | | | | |
| `GET /api/v1/users` (listar) | ✅ | ✅ | ❌ | ❌ |
| `GET /api/v1/users/{id}` | ✅ | ✅ (misma sucursal) | ❌ | ❌ |
| `POST /api/v1/users` (crear) | ✅ | ❌ | ❌ | ❌ |
| `PATCH /api/v1/users/{id}` | ✅ | ❌ | ❌ | ❌ (solo su perfil: tel, dir) |
| `DELETE /api/v1/users/{id}` | ✅ | ❌ | ❌ | ❌ |
| **Branches** | | | | |
| `GET /api/v1/branches` | ✅ | ✅ | ✅ | ❌ |
| `POST /api/v1/branches` | ✅ | ❌ | ❌ | ❌ |
| `PATCH /api/v1/branches/{id}` | ✅ | ❌ | ❌ | ❌ |
| `DELETE /api/v1/branches/{id}` | ✅ | ❌ | ❌ | ❌ |
| **Deliveries (POD)** | | | | |
| `GET /api/v1/deliveries` | ✅ | ✅ | ✅ (solo propias) | ✅ (solo propias) |
| `PATCH /api/v1/deliveries/{id}` | ✅ | ✅ | ❌ | ❌ |
| `POST /api/v1/deliveries/{id}/pod` (subir comprobante) | ✅ | ✅ | ✅ (solo propias) | ❌ |
| **Logistics** | | | | |
| `GET /api/v1/logistics/batches` | ✅ | ✅ | ✅ (solo asignados) | ❌ |
| `POST /api/v1/logistics/batches` | ✅ | ✅ | ❌ | ❌ |
| `POST /api/v1/logistics/batches/{id}/assign` | ✅ | ✅ | ❌ | ❌ |
| `GET /api/v1/logistics/vehicles` | ✅ | ✅ | ✅ (solo asignados) | ❌ |
| **Notifications** | | | | |
| `GET /api/v1/notifications` | ✅ | ✅ | ✅ | ✅ (solo propias) |
| `PATCH /api/v1/notifications/read-all` | ✅ | ✅ | ✅ | ✅ |
| **Reports / Dashboard** | | | | |
| `GET /api/v1/reports/kpis` | ✅ | ✅ | ❌ | ❌ |
| `GET /api/v1/dashboard` | ✅ | ✅ | ✅ (filtrado a sus datos) | ❌ |

**Regla de filtro por sucursal**: `Warehouse Operator` y `Driver` solo ven datos de su `branch`. `Client` solo ve sus propias encomiendas. `Admin` ve todo.

## 7. Criterios de aceptación

### R1

- **Dado** un request sin `Authorization`, **cuando** llama a un endpoint protegido,
  **entonces** responde `401`.
- **Dado** un token inválido o expirado, **entonces** responde `401`.

### R2

- **Dado** un token de rol `Client`, **cuando** llama a `POST /api/v1/users`,
  **entonces** responde `403` con `{"message": "No tiene permisos para esta operacion"}`.
- **Dado** un token de rol `Admin`, **cuando** llama al mismo endpoint, **entonces** no recibe `403`.
- La matriz de la sección 6 se cumple para todos los endpoints listados.

### R3

- **Dado** un endpoint nuevo, **cuando** se revisa el código, **entonces** su permiso se declara
  junto a la ruta mediante una dependencia reutilizable, no con `if` ad hoc.
- Existe un módulo/archivo único que define la matriz y es importado por las rutas.

### R4

- **Dado** un usuario con `active = false`, **cuando** intenta login, **entonces** responde `403`
  con `{"message": "Usuario inactivo"}`.
- **Dado** un token emitido antes de desactivar al usuario, **cuando** lo usa, **entonces** responde `403`.

### R5

- **Dado** `AWEN_SECRET_KEY` sin definir o igual a `CHANGE_ME`, **cuando** arranca la app,
  **entonces** falla con un error explícito. No hay excepción para `AWEN_ENV=dev` ni `AWEN_DEBUG=true`.

### R6

- Pospuesto. El rate limit actual (en memoria por proceso) se mantiene. Se documenta en NOTAS.md
  como limitación conocida.

## 8. Contratos de API

### Endpoints afectados

| Método | Ruta | Cambia | Notas |
| --- | --- | --- | --- |
| POST | `/api/v1/auth/login` | sí (403 usuario inactivo) | mismo body |
| GET | `/api/v1/auth/me` | no | — |
| Todas las rutas protegidas | — | sí (403 por rol) | nuevo código de error |

### Errores exactos

| Código | Mensaje (sin tildes) | Cuándo |
| --- | --- | --- |
| 401 | `No autenticado` | Sin token o token invalido |
| 403 | `No tiene permisos para esta operacion` | Rol sin permiso |
| 403 | `Usuario inactivo` | Login o token de usuario desactivado |
| 429 | `Demasiadas solicitudes. Intente de nuevo mas tarde.` | Rate limit (existente) |

> `notifications_stream.py:21` hoy usa `Not authenticated` en inglés; debe alinearse con esta tabla.

## 9. Casos de borde

- Token válido de un usuario borrado.
- Token válido con rol desconocido (string fuera del enum).
- Usuario que cambia de rol mientras su token sigue vigente.
- Petición a un endpoint público (`/tracking`, `/health`) con token inválido: no debe fallar.
- Rate limit detrás de proxy: `request.client.host` puede ser la IP del proxy.

## 10. Impacto en datos y migraciones

- No requiere migración: `active` y `role` ya existen (`back-end/app/models/user.py`).
- No toca objetos "Awen".

## 11. Tests a crear

| Test | Requisito | Tipo |
| --- | --- | --- |
| `test_rol_sin_permiso_devuelve_403` | R2 | integración |
| `test_admin_puede_gestionar_usuarios` | R2 | integración |
| `test_matriz_permisos_centralizada` | R3 | unitario |
| `test_usuario_inactivo_no_puede_login` | R4 | integración |
| `test_token_de_usuario_inactivo_rechazado` | R4 | integración |
| `test_arranque_falla_con_secret_key_por_defecto` | R5 | unitario |

> R6 no tiene test en esta fase (pospuesto).

## 12. Riesgos

- Aplicar RBAC puede romper flujos que hoy funcionan para todos los roles (especialmente
  `Driver` y `Client` en `parcels`, `deliveries` y `logistics`).
- Endurecer el rate limit con almacenamiento compartido añade infraestructura (Redis) que hoy
  no existe; se pospone.

## 13. Preguntas abiertas

- [x] ¿Cuál es la matriz exacta de permisos por rol y endpoint? → **Resuelta** (sección 6).
- [x] ¿El cliente puede crear encomiendas o solo consultarlas? → **Sí, puede crear** (sección 6).
- [x] ¿El conductor puede ver todas las encomiendas o solo las de sus lotes? → **Solo sus lotes** (sección 6).
- [x] ¿Se necesita refresh token o basta con 60 minutos? → **Pospuesto a fase 2**.
- [x] ¿R5 puede romper el arranque en desarrollo? → **Sin excepción; falla siempre**.
- [x] ¿Se acepta añadir Redis para R6 o se pospone? → **Pospuesto**.

## 14. Plan de verificación manual

1. Login con cada rol y llamar a un endpoint prohibido: debe dar 403.
2. Desactivar un usuario y probar login: debe dar 403.
3. Probar `/api/v1/tracking/...` sin token: debe seguir siendo público.
4. Arrancar sin `AWEN_SECRET_KEY` o con `CHANGE_ME`: la app debe fallar al iniciar.