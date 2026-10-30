---
fase: 5
nombre: limpieza-deuda-tecnica
estado: aprobada
rama: feat/fase-5-limpieza-deuda-tecnica
autor:
fecha: 2026-10-30
---

# Fase 5 — Limpieza de deuda técnica y decisiones pendientes

## 1. Contexto y problema

El CI del repositorio lleva fallando desde antes de la Fase 3 por tres causas independientes que bloquean la calidad y la entrega continua:

1. **Dependencia `boto3` ausente** en `requirements.txt` (introducida en Fase 2 para Vercel Blob).
2. **18 errores de lint** en páginas de producción del frontend (fuera del alcance de Fase 4).
3. **6 tests de backend preexistentes** en rojo que no se arreglaron en Fase 1.
4. **Licencia MIT** en `LICENSE` — proyecto educativo, se mantiene MIT + `NOTICE`.
5. **`start_backend.bat`** con ruta absoluta hardcodeada.
6. Rama `develop` sin branch protection ni CI obligatorio (Fase 6).

Esta fase agrupa la limpieza para dejar el repo en verde y listo para Fase 6 (CI/CD y protección de ramas).

## 2. Alcance

### Dentro del alcance

- **Backend**: Añadir `boto3` y `botocore` a `requirements.txt`.
- **Backend**: Arreglar 6 tests fallidos:
  - `test_delete_branch_soft` / `test_delete_user_soft`: soft delete con columna `active`.
  - `test_update_status_skip_not_allowed`: validación de salto de estado (state machine).
  - `test_reports_activity`: endpoint devuelve lista vacía (seed en tests).
  - `test_public_tracking_found` / `test_full_lifecycle`: PostgreSQL en CI via Docker.
- **Frontend**: Corregir 18 errores de ESLint en código de producción (no tests).
- **Docs/Repo**: `LICENSE` MIT + `NOTICE` con copyright autor (uso educativo).
- **Scripts**: `start_backend.bat`, `start_backend.sh`, `start_backend.ps1` con ruta relativa.
- **CI**: Contenedor PostgreSQL 16 en GitHub Actions; cache `boto3`.

### Fuera del alcance (no-goals)

- Tests E2E (Cypress/Playwright).
- Refactors arquitectónicos mayores.
- Cambios en la API pública (salvo soft delete y state machine).
- Branch protection de `develop` (Fase 6).

## 3. Comportamiento actual

| Área | Estado |
|------|--------|
| `requirements.txt` | Falta `boto3>=1.34.0` y `botocore>=1.34.0`. |
| `npm run lint` (frontend) | 18 errores, 11 warnings en 7 archivos. |
| `pytest` (backend) | 186/192 pasan; 6 fallos (4 failed + 2 error). |
| `LICENSE` | MIT (pública). |
| `start_backend.bat:2` | `cd C:\Users\espin\Desktop\AWEN\AWEN\back-end`. |
| `.github/workflows/ci.yml` | No instala `boto3`; sin PostgreSQL; sin branch protection. |

Archivos con errores de lint (frontend):
- `AuthContext.jsx` (3 `no-empty` en `catch`)
- `DriverDashboard.jsx` (`deliveryPhoto` no usada)
- `Reports.jsx` (`PARCEL_STATUS_LABELS` importado no usado)
- `BranchManagement.jsx`, `ClientProfile.jsx`, `ParcelManagement.jsx`, `Tracking.jsx`, `UserManagement.jsx` (`set-state-in-effect`, `rules-of-hooks`, `exhaustive-deps`)
- `Logistics.jsx` (`loadData` antes de declaración)
- `Dashboard.jsx` (`execute` falta en `useEffect` deps)

Tests fallidos (backend):
- `test_branches.py::TestBranches::test_delete_branch_soft` — KeyError `active` (API hace hard delete).
- `test_users.py::TestUsers::test_delete_user_soft` — KeyError `active` (API hace hard delete).
- `test_parcels.py::TestParcelStatus::test_update_status_skip_not_allowed` — espera 422, recibe 200.
- `test_reports.py::TestReports::test_activity` — `assert 0 > 0` (lista vacía).
- `test_parcels.py::TestPublicTracking::test_public_tracking_found` — OperationalError PostgreSQL.
- `test_workflows.py::TestParcelLifecycle::test_full_lifecycle` — OperationalError PostgreSQL.

## 4. Comportamiento deseado

- `npm run lint` → 0 errores (warnings tolerados).
- `pytest` → 192/192 pasan (2 tests requieren PG en CI, ya no `xfail`).
- `requirements.txt` incluye `boto3` y `botocore`.
- `LICENSE` MIT + `NOTICE` (copyright autor, uso educativo).
- `start_backend.bat/.sh/.ps1` usan ruta relativa.
- CI verde en PRs hacia `develop` con PostgreSQL 16 en contenedor.

## 5. Requisitos

| ID | Requisito | Prioridad |
|----|-----------|-----------|
| R1 | Añadir `boto3>=1.34.0` y `botocore>=1.34.0` a `requirements.txt` y actualizar lock. | must |
| R2 | Corregir 18 errores de ESLint en `front-end/src/pages/` y `front-end/src/context/`. | must |
| R3 | Soft delete en `branches` y `users`: migración Alembic (`active` boolean default true), filtro en repos, rutas devuelven 404 si `active=false`. | must |
| R4 | State machine de encomiendas: `ALLOWED_TRANSITIONS` en `app/schemas/parcel.py` + validación en `ParcelService.update_status`. | must |
| R5 | Seed de actividad en `conftest.py` para reports (parcelas con tracking/notificaciones). | should |
| R6 | PostgreSQL 16 en CI (`services.postgres`); quitar `xfail` a 2 tests. | must |
| R7 | `LICENSE` MIT + `NOTICE` con copyright y mención uso educativo. | must |
| R8 | 3 scripts de arranque multiplataforma con ruta relativa (`cd /d "%~dp0"` / `cd "$(dirname "$0")"`). | must |
| R9 | Workflow CI actualizado: cache `boto3`, servicio postgres, healthcheck. | must |

## 6. Criterios de aceptación

### R1
- **Dado** un entorno limpio
- **Cuando** se ejecuta `pip install -r requirements.txt`
- **Entonces** `import boto3` y `import botocore` funcionan sin error.

### R2
- **Dado** el frontend
- **Cuando** se ejecuta `npm run lint`
- **Entonces** exit code 0 y 0 errores reportados.

### R3
- **Dado** un branch o usuario
- **Cuando** se hace DELETE `/api/v1/branches/{id}` o `/api/v1/users/{id}`
- **Entonces** el objeto queda con `active: false` y GET posterior devuelve 404.
- **Y** los tests `test_delete_branch_soft` y `test_delete_user_soft` pasan.

### R4
- **Dado** una encomienda en estado `Registered`
- **Cuando** se intenta cambiar a `Delivered` saltando estados intermedios
- **Entonces** la API devuelve 422 con mensaje "Transicion de estado no permitida".
- **Y** `test_update_status_skip_not_allowed` pasa.

### R5
- **Dado** datos seed con actividad
- **Cuando** se consulta `GET /api/v1/reports/activity`
- **Entonces** devuelve lista no vacía.
- **Y** `test_reports_activity` pasa.

### R6
- **Dado** un PR hacia `develop`
- **Cuando** corre el workflow `ci.yml`
- **Entonces** el job `backend` levanta PostgreSQL 16, instala `boto3`, y los 192 tests pasan.

### R7
- **Dado** el repo
- **Cuando** se revisa `LICENSE` y `NOTICE`
- **Entonces** `LICENSE` es MIT estándar; `NOTICE` contiene copyright del autor y mención "Proyecto educativo".

### R8
- **Dado** Windows / Linux / macOS
- **Cuando** se ejecuta `start_backend.bat` / `.sh` / `.ps1`
- **Entonces** arranca el backend desde cualquier directorio.

### R9
- **Dado** el workflow `ci.yml`
- **Cuando** se ejecuta en PR
- **Entonces** cachea pip con `boto3`, levanta `postgres:16-alpine` con healthcheck, y `pytest` pasa.

## 7. Contratos de API

### Endpoints afectados

| Método | Ruta | Cambia | Notas |
|--------|------|--------|-------|
| DELETE | `/api/v1/branches/{id}` | sí | Soft delete: `active=false` en lugar de hard delete. |
| DELETE | `/api/v1/users/{id}` | sí | Soft delete: `active=false` en lugar de hard delete. |
| POST | `/api/v1/parcels/{id}/status` | sí | Validar transiciones permitidas (state machine). |
| GET | `/api/v1/reports/activity` | no | Asegurar seed en tests. |

### Errores exactos

| Código | Mensaje (sin tildes) | Cuándo |
|--------|----------------------|--------|
| 422 | `Transicion de estado no permitida` | Salto de estado inválido en `/parcels/{id}/status`. |
| 404 | `Sucursal no encontrada` | GET branch tras soft delete. |
| 404 | `Usuario no encontrado` | GET user tras soft delete. |

## 8. Casos de borde

- Soft delete en cascada: si se borra una sucursal con usuarios, los usuarios quedan huérfanos (no se borran en cascada).
- Validación de transiciones: matriz `Registered → Picked Up → In Transit → At Destination Branch → Out for Delivery → Delivered`; `Returned` solo desde `Out for Delivery` o `At Destination Branch`.
- Tests que requieren PostgreSQL: contenedor en CI elimina necesidad de `xfail`.

## 9. Impacto en datos y migraciones

- **Migración Alembic**: Sí, `alembic revision --autogenerate -m "add_active_to_branches_and_users"` para añadir columna `active` (boolean, default true) a `branches` y `users`.
- **Reversible**: Sí (`alembic downgrade -1`).
- **Objetos "Awen"**: No se tocan.

## 10. Tests a crear / modificar

| Test | Requisito | Tipo |
|------|-----------|------|
| `test_soft_delete_branch` | R3 | integración |
| `test_soft_delete_user` | R3 | integración |
| `test_status_transition_validation` | R4 | integración |
| `test_reports_activity_with_data` | R5 | integración |
| `test_public_tracking_found` | R6 | integración (ya existe, quitar xfail) |
| `test_full_lifecycle` | R6 | integración (ya existe, quitar xfail) |

## 11. Riesgos

- Soft delete puede afectar queries existentes que no filtran por `active` (mitigado: filtro en repositorio base).
- Validación de transiciones puede romper clientes que saltan estados (mitigado: error 422 claro).
- Contenedor PostgreSQL en CI añade ~15-20s al job backend.

## 12. Preguntas abiertas

- [x] **Licencia**: MIT + NOTICE (proyecto educativo).
- [x] **Soft delete**: Columna `active` en BD + filtro en repos.
- [x] **State machine**: Constante `ALLOWED_TRANSITIONS` en schema + validación en servicio.
- [x] **PostgreSQL en CI**: Contenedor `postgres:16-alpine` con healthcheck.
- [x] **Scripts arranque**: `.bat` (Windows), `.sh` (Linux/macOS), `.ps1` (PowerShell).

## 13. Plan de verificación manual

1. `cd back-end && pip install -r requirements.txt && python -c "import boto3, botocore; print('OK')"`
2. `cd back-end && $env:AWEN_SECRET_KEY="test"; python -m pytest tests -q` → 192 pasan.
3. `cd front-end && npm run lint` → 0 errores.
4. `cd front-end && npm test && npm run build` → OK.
5. Verificar `LICENSE`, `NOTICE` y `start_backend.*`.
6. Abrir PR a `develop` y confirmar CI verde con PostgreSQL.