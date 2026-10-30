---
fase: 5
nombre: limpieza-deuda-tecnica
estado: borrador
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
4. **Licencia MIT** en `LICENSE` contradice la regla de privacidad del proyecto.
5. **`start_backend.bat`** con ruta absoluta hardcodeada.
6. Rama `develop` sin branch protection ni CI obligatorio.

Esta fase agrupa la limpieza para dejar el repo en verde y listo para Fase 6 (CI/CD y protección de ramas).

## 2. Alcance

### Dentro del alcance

- **Backend**: Añadir `boto3` y `botocore` a `requirements.txt`.
- **Backend**: Arreglar o documentar 6 tests fallidos:
  - `test_delete_branch_soft` / `test_delete_user_soft`: soft delete vs hard delete.
  - `test_update_status_skip_not_allowed`: validación de salto de estado.
  - `test_reports_activity`: endpoint devuelve lista vacía.
  - `test_public_tracking_found` / `test_full_lifecycle`: requieren PostgreSQL local.
- **Frontend**: Corregir 18 errores de ESLint en código de producción (no tests).
- **Docs/Repo**: Decidir y aplicar licencia (eliminar `LICENSE` o cambiar a privativa).
- **Scripts**: Corregir `start_backend.bat` para usar ruta relativa.
- **CI**: Añadir `boto3` al cache de dependencias del workflow.

### Fuera del alcance (no-goals)

- Tests E2E (Cypress/Playwright).
- Refactors arquitectónicos mayores.
- Migración de base de datos (salvo que sea necesaria para tests).
- Cambios en la API pública.
- Branch protection de `develop` (Fase 6).

## 3. Comportamiento actual

| Área | Estado |
|------|--------|
| `requirements.txt` | Falta `boto3>=1.34.0` y `botocore>=1.34.0`. |
| `npm run lint` (frontend) | 18 errores, 11 warnings en 7 archivos. |
| `pytest` (backend) | 186/192 pasan; 6 fallos (4 failed + 2 error). |
| `LICENSE` | MIT (pública). |
| `start_backend.bat:2` | `cd C:\Users\espin\Desktop\AWEN\AWEN\back-end`. |
| `.github/workflows/ci.yml` | No instala `boto3`; no tiene branch protection. |

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
- `pytest` → 192/192 pasan (o fallos documentados y aceptados con `xfail`).
- `requirements.txt` incluye `boto3` y `botocore`.
- `LICENSE` eliminado o reemplazado por licencia privativa.
- `start_backend.bat` usa `cd /d "%~dp0"`.
- CI verde en PRs hacia `develop`.

## 5. Requisitos

| ID | Requisito | Prioridad |
|----|-----------|-----------|
| R1 | Añadir `boto3` y `botocore` a `requirements.txt` y actualizar lock. | must |
| R2 | Corregir 18 errores de ESLint en `front-end/src/pages/` y `front-end/src/context/`. | must |
| R3 | Resolver tests `test_delete_branch_soft` y `test_delete_user_soft` (soft delete o actualizar test). | should |
| R4 | Resolver `test_update_status_skip_not_allowed` (validar transiciones de estado). | should |
| R5 | Resolver `test_reports_activity` (seed de datos o ajustar aserción). | should |
| R6 | Marcar `test_public_tracking_found` y `test_full_lifecycle` como `xfail` (requieren PostgreSQL externo). | should |
| R7 | Eliminar `LICENSE` o reemplazar por licencia privativa. | must |
| R8 | Corregir `start_backend.bat` a ruta relativa. | must |
| R9 | Actualizar workflow CI para cachear `boto3`. | must |

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
- **Entonces** el objeto queda con `active: false` y GET posterior devuelve 404 (o 200 con `active: false`).
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
- **Dado** la suite de tests
- **Cuando** se ejecuta `pytest`
- **Entonces** `test_public_tracking_found` y `test_full_lifecycle` aparecen como `xfail` (no fallan el build).

### R7
- **Dado** el repo
- **Cuando** se revisa `LICENSE`
- **Entonces** no contiene licencia MIT/OSI; contiene aviso de código privado o archivo eliminado.

### R8
- **Dado** Windows
- **Cuando** se ejecuta `start_backend.bat`
- **Entonces** arranca el backend desde cualquier directorio.

### R9
- **Dado** un PR hacia `develop`
- **Cuando** corre el workflow `ci.yml`
- **Entonces** el job `backend` instala dependencias incluyendo `boto3` y pasa (salvo tests con `xfail`).

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

- Soft delete en cascada: si se borra una sucursal con usuarios, ¿qué pasa?
- Validación de transiciones: definir matriz de estados permitidos (ej. `Registered → Picked Up → In Transit → At Destination Branch → Out for Delivery → Delivered`).
- Tests que requieren PostgreSQL: decidir si montar contenedor en CI o mantener `xfail`.

## 9. Impacto en datos y migraciones

- **Migración Alembic**: Sí, para añadir columna `active` (boolean, default true) a `branches` y `users` si no existe.
- **Reversible**: Sí (drop column).
- **Objetos "Awen"**: No se tocan.

## 10. Tests a crear

| Test | Requisito | Tipo |
|------|-----------|------|
| `test_soft_delete_branch` | R3 | integración |
| `test_soft_delete_user` | R3 | integración |
| `test_status_transition_validation` | R4 | integración |
| `test_reports_activity_with_data` | R5 | integración |

Tests a marcar `xfail`:
- `test_public_tracking_found`
- `test_full_lifecycle`

## 11. Riesgos

- Soft delete puede afectar queries existentes que no filtran por `active`.
- Validación de transiciones puede romper clientes que saltan estados.
- Cambio de licencia requiere decisión de producto/legal.

## 12. Preguntas abiertas

- [ ] **Soft delete**: ¿Se implementa en BD (columna `active`) o solo en API? (Recomendado: BD + filtro en repos).
- [ ] **State machine**: ¿Dónde definir transiciones permitidas? (Schema, servicio, o constante compartida).
- [ ] **Licencia**: ¿Eliminar `LICENSE` o poner aviso "Private - All rights reserved"?
- [ ] **PostgreSQL en CI**: ¿Montar contenedor `postgres:16` en GitHub Actions para los 2 tests `xfail`?
- [ ] **`start_backend.bat`**: ¿Mantener `.bat` o migrar a script multiplataforma (`.sh` + `.ps1`)?

## 13. Plan de verificación manual

1. `cd back-end && pip install -r requirements.txt && python -c "import boto3, botocore; print('OK')"`
2. `cd back-end && $env:AWEN_SECRET_KEY="test"; python -m pytest tests -q` → 192 pasan (o 190 + 2 xfail).
3. `cd front-end && npm run lint` → 0 errores.
4. `cd front-end && npm test && npm run build` → OK.
5. Verificar `LICENSE` y `start_backend.bat`.
6. Abrir PR a `develop` y confirmar CI verde.