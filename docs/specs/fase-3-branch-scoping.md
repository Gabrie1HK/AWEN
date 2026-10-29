---
fase: 3
nombre: branch-scoping
estado: borrador
rama: feat/fase-3-branch-scoping
autor: Gabriel Espinoza
fecha: 2026-10-29
---

# Fase 3 — Filtro por Sucursal (Branch Scoping)

## 1. Contexto y problema

La Fase 1 definió la matriz de permisos por rol (sección 6, regla): *"Warehouse Operator y Driver solo ven datos de su `branch`. Client solo ve sus propias encomiendas. Admin ve todo."*

**Problema actual**: Los endpoints devuelven **todo sin filtrar** por `user.branch`. Los usuarios ven datos de otras sucursales, violando el principio de menor privilegio y el aislamiento de datos por sucursal.

Ejemplos:
- `GET /api/v1/parcels` devuelve encomiendas de todas las sucursales
- `GET /api/v1/deliveries` devuelve entregas de todas las sucursales
- `GET /api/v1/logistics/batches` devuelve lotes de todas las sucursales
- `GET /api/v1/users` (Operator) devuelve usuarios de todas las sucursales
- Dashboard/Reports muestran datos globales sin filtrar

## 2. Alcance

### Dentro del alcance

- **Parcels**: Filtrar `list()` por branch del usuario (Operator/Driver ven su branch; Admin ve todo; Client ve solo propias)
- **Deliveries**: Filtrar `list()` por branch del driver/operador
- **Logistics**: Filtrar `list_batches()` y `list_vehicles()` por branch
- **Users**: Operadores solo listan users de su branch
- **Reports/Dashboard**: KPIs, daily-volume, deliveries-by-branch, activity, summary, top-routes filtrados por branch
- **Single resource GET**: `get_parcel()`, `get_delivery()`, `get_batch()`, `get_user()` - verificar ownership/branch

### Fuera del alcance (no-goals)

- Cambios en modelo de datos (branch ya existe en User)
- UI para asignar branch a usuarios (ya existe en UserManagement)
- Filtrado en tracking público (`/tracking/{guide}` - sigue público)
- Cambios en creación de recursos (validación de branch en create ya se hace en service)

## 3. Comportamiento actual

| Endpoint | Comportamiento actual |
|----------|----------------------|
| `GET /api/v1/parcels` | Devuelve todas las encomiendas (sin filtro) |
| `GET /api/v1/deliveries` | Devuelve todas las entregas (sin filtro) |
| `GET /api/v1/logistics/batches` | Devuelve todos los lotes (sin filtro) |
| `GET /api/v1/logistics/vehicles` | Devuelve todos los vehículos (sin filtro) |
| `GET /api/v1/users` (Operator) | Devuelve todos los usuarios (sin filtro) |
| `GET /api/v1/reports/kpis` | KPIs globales (sin filtro) |
| `GET /api/v1/dashboard` | Dashboard global (sin filtro) |

Todos usan `user` del token pero **no filtran por `user.branch`**.

## 4. Comportamiento deseado

### Reglas de filtrado por rol

| Rol | Parcels | Deliveries | Logistics | Users | Reports/Dashboard |
|-----|---------|------------|-----------|-------|-------------------|
| **Admin** | Todas | Todas | Todas | Todas | Globales (sin filtro) |
| **Warehouse Operator** | Solo su `branch` (origin/dest) | Solo su `branch` | Solo su `branch` | Solo su `branch` | Solo su `branch` |
| **Driver** | Solo su `branch` (origin/dest) | Solo asignadas a él (su branch) | Solo su `branch` | No acceso | Solo su `branch` |
| **Client** | Solo propias (ya en R1 Fase 1) | Solo propias | No acceso | Solo su perfil | No acceso |

### Detalles por endpoint

- **Parcels**: Filtrar donde `origin_branch == user.branch` OR `destination_branch == user.branch`
- **Deliveries**: Filtrar donde delivery está asignada a driver del mismo branch, o branch del operador
- **Logistics**: Filtrar batches/vehicles donde `branch == user.branch`
- **Users**: Operator ve solo `WHERE branch == user.branch`
- **Reports**: Todas las agregaciones filtradas por branch del usuario (excepto Admin)
- **Dashboard**: KPIs, daily-volume, deliveries-by-branch filtrados

## 5. Requisitos

| ID | Requisito | Prioridad |
|----|-----------|-----------|
| R1 | `GET /api/v1/parcels` filtrado por branch del usuario (Operator/Driver) | must |
| R2 | `GET /api/v1/deliveries` filtrado por branch del driver/operador | must |
| R3 | `GET /api/v1/logistics/batches` y `/vehicles` filtrado por branch | must |
| R4 | `GET /api/v1/users` (Operator) solo ve users de su branch | must |
| R5 | `GET /api/v1/reports/*` y `GET /api/v1/dashboard` filtrados por branch | must |
| R6 | Admin ve todo sin filtro (backward compatibility) | must |
| R7 | Single resource GET verifica ownership/branch (404 si no pertenece) | should |

## 6. Criterios de aceptación

### R1 - Parcels filtrados por branch
- **Dado** un Operator de "Sucursal Central"
- **Cuando** llama `GET /api/v1/parcels`
- **Entonces** solo ve encomiendas donde `origin_branch == "Sucursal Central"` **OR** `destination_branch == "Sucursal Central"`

### R2 - Deliveries filtrados por branch
- **Dado** un Driver de "Sucursal Norte"
- **Cuando** llama `GET /api/v1/deliveries`
- **Entonces** solo ve entregas donde el `driver` pertenece a "Sucursal Norte" (join Delivery.driver → User.branch)

### R3 - Logistics filtrado por branch
- **Dado** un Operator de "Sucursal Sur"
- **Cuando** llama `GET /api/v1/logistics/batches`
- **Entonces** solo ve lotes donde el `driver` del lote pertenece a "Sucursal Sur" (join Batch.driver → User.branch)
- **Y** `GET /api/v1/logistics/vehicles` solo ve vehículos donde el `driver` pertenece a "Sucursal Sur"

### R4 - Users list para Operator
- **Dado** un Operator de "Sucursal Central"
- **Cuando** llama `GET /api/v1/users`
- **Entonces** solo ve usuarios donde `branch == "Sucursal Central"`

### R5 - Reports/Dashboard filtrados
- **Dado** un Operator de "Sucursal Central"
- **Cuando** llama `GET /api/v1/reports/kpis` o `GET /api/v1/dashboard`
- **Entonces** KPIs, daily-volume, deliveries-by-branch reflejan solo datos de "Sucursal Central"

### R6 - Admin sin filtro
- **Dado** un Admin
- **Cuando** llama cualquier endpoint de listado
- **Entonces** ve todos los registros sin filtrar por branch

### R7 - Single resource ownership
- **Dado** un Driver de "Sucursal Norte"
- **Cuando** llama `GET /api/v1/parcels/ENV-001` (ni origin ni destination son "Sucursal Norte")
- **Entonces** recibe 404 (no encontrado en su scope)

## 7. Contratos de API

### Endpoints afectados

| Método | Ruta | Cambia | Notas |
|--------|------|--------|-------|
| GET | `/api/v1/parcels` | sí (filtro interno) | Respuesta igual, menos items |
| GET | `/api/v1/parcels/{id}` | sí (validación) | 404 si no pertenece a branch |
| GET | `/api/v1/deliveries` | sí (filtro interno) | Respuesta igual, menos items |
| GET | `/api/v1/deliveries/{id}` | sí (validación) | 404 si no pertenece |
| GET | `/api/v1/logistics/batches` | sí (filtro interno) | Respuesta igual, menos items |
| GET | `/api/v1/logistics/vehicles` | sí (filtro interno) | Respuesta igual, menos items |
| GET | `/api/v1/users` | sí (filtro Operator) | Respuesta igual, menos items |
| GET | `/api/v1/users/{id}` | sí (validación) | 404 si Operator y distinto branch |
| GET | `/api/v1/reports/*` | sí (filtro interno) | Respuesta igual, datos filtrados |
| GET | `/api/v1/dashboard` | sí (filtro interno) | Respuesta igual, datos filtrados |

### Esquemas de salida
Sin cambios (mismos schemas, menos items en arrays).

### Errores exactos
| Código | Mensaje (sin tildes) | Cuándo |
|--------|----------------------|--------|
| 404 | `Encomienda no encontrada` | GET parcel/delivery/batch no pertenece a branch |
| 404 | `Usuario no encontrado` | GET user no pertenece a branch (Operator) |

## 8. Casos de borde

- Usuario sin branch asignado (`branch == null`): **Client** ve solo sus encomiendas (`/my-parcels`); **Operator/Driver/Admin** sin branch → lista vacía (no deberían existir sin branch)
- Branch inexistente en datos: lista vacía
- Cambio de branch de usuario mientras tiene token vigente: próximo request usa nuevo branch
- Admin creando recurso para otro branch: permitido (Admin no tiene restricción)
- Driver creando parcela: validar que `origin_branch` sea su branch

## 9. Impacto en datos y migraciones

- **Migración Alembic**: No requerida (campo `branch` ya existe en User, Parcels; Deliveries/Batches/Vehicles usan `driver` → join User)
- **Reversible**: Sí (quitar filtro en service vuelve a comportamiento anterior)
- **Objetos "Awen"**: **No** se tocan

## 10. Tests a crear

| Test | Requisito | Tipo |
|------|-----------|------|
| `test_parcels_list_filtered_by_operator_branch` | R1 | integración |
| `test_parcels_list_filtered_by_driver_branch` | R1 | integración |
| `test_parcels_get_returns_404_for_other_branch` | R7 | integración |
| `test_deliveries_list_filtered_by_driver_branch` | R2 | integración |
| `test_deliveries_list_filtered_by_operator_branch` | R2 | integración |
| `test_logistics_batches_filtered_by_branch` | R3 | integración |
| `test_logistics_vehicles_filtered_by_branch` | R3 | integración |
| `test_users_list_operator_sees_own_branch` | R4 | integración |
| `test_reports_kpis_filtered_by_branch` | R5 | integración |
| `test_dashboard_filtered_by_branch` | R5 | integración |
| `test_admin_sees_all_without_filter` | R6 | integración |

## 11. Riesgos

- **Performance**: Filtros `WHERE branch IN (...)` en queries grandes → agregar índices si necesario
- **Datos existentes**: Parcels/Deliveries sin branch poblado → decidir default (null = global?)
- **Tests existentes**: Algunos tests esperan datos globales → actualizar fixtures/assertions
- **Driver parcels**: Fase 1 permite Driver ver parcels (su branch) → validar que filtro coincide

## 12. Preguntas abiertas (RESUELTAS ✅)

- [x] **Branch en Parcels**: **OR (origin_branch O destination_branch)** — Parcel tiene ambos campos requeridos. Operador en origen ve lo que envía; en destino ve lo que recibe.
- [x] **Deliveries ownership**: **Branch del driver** — Delivery tiene `driver` (string). Join Delivery.driver → User.name → User.branch. Seeds: DEL-001 driver="Conductor Ana", DEL-002 driver="Conductor Pedro".
- [x] **Vehicles/Batches**: **Por driver's branch** — Vehicle y Batch tienen `driver` (string). No tienen campo branch propio. Filtro: Vehicle.driver / Batch.driver → User.name → User.branch.
- [x] **Branch null (Clients)**: Ya cubierto Fase 1 — Clients tienen `branch=None`. Solo ven sus encomiendas via `/my-parcels` (Fase 1 R1).
- [x] **Índices DB**: **Sí, agregar compuestos** — Performance: `parcels(origin_branch, destination_branch, status)`, `users(branch, role)`. Para deliveries/batches/vehicles: índices en `driver` para joins.

> Todas resueltas. Spec lista para aprobar.

## 13. Plan de verificación manual

1. Login como Operator "Sucursal Central" → `GET /parcels` → solo ve Central
2. Login como Driver "Sucursal Norte" → `GET /parcels` → solo ve Norte
3. Login como Admin → `GET /parcels` → ve todas
4. Operator "Central" → `GET /users` → solo ve users de Central
5. Driver "Norte" → `GET /deliveries` → solo ve entregas de Norte
6. Admin → `GET /reports/kpis` → ve KPIs globales
7. Operator "Central" → `GET /dashboard` → KPIs solo de Central
8. Driver "Norte" → `GET /parcels/ENV-XXX` (de Sur) → 404