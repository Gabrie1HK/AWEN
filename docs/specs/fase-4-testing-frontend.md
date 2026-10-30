---
fase: 4
nombre: testing-frontend-cobertura
estado: borrador
rama: feat/fase-4-testing-frontend
autor: Gabriel Espinoza
fecha: 2026-10-29
---

# Fase 4 — Testing Frontend: Cobertura Crítica

## 1. Contexto y problema

El frontend tiene **cobertura de tests muy baja**: solo existe `api.test.js` (262 líneas) para probar el cliente HTTP. No hay tests para:
- Páginas críticas: `ParcelManagement`, `Logistics`, `ProofOfDelivery`, `Reports`, `Dashboard`, `ClientProfile`, `DriverDashboard`
- Hooks personalizados: `useApi`, `useAuth`, `useNotificationsSSE`
- Contexto: `AuthContext`
- Routing protegido y navegación por roles
- Componentes UI reutilizables

Esto impide detectar regresiones en la UI y dificulta el refactoring seguro.

## 2. Alcance

### Dentro del alcance
- **Tests de páginas críticas** (integración): `ParcelManagement`, `Logistics`, `ProofOfDelivery`, `Reports`, `Dashboard`, `ClientProfile`, `DriverDashboard`
- **Tests de hooks** (unitarios): `useApi`, `useAuth`, `useNotificationsSSE`
- **Tests de contexto**: `AuthContext` (login, logout, permisos, persistencia)
- **Tests de routing protegido**: navegación por roles, redirecciones, 403/401 handling
- **Tests de componentes UI críticos**: `DataTable`, `StatCard`, `LoadingSpinner`, `ErrorBanner`, `ConfirmModal`
- **Configuración de cobertura**: umbral ≥ 70% statements en páginas críticas
- **Mocking de API**: usar `msw` (Mock Service Worker) para simular backend

### Fuera del alcance (no-goals)
- Tests E2E completos (Cypress/Playwright) - fase posterior
- Tests de accesibilidad (a11y) - fase posterior
- Tests visuales/regression visual - fase posterior
- Tests de performance - fase posterior
- Cobertura 100% - objetivo irrealista para este alcance

## 3. Comportamiento actual

| Área | Tests existentes | Cobertura |
|------|-----------------|-----------|
| `api.js` (cliente HTTP) | `api.test.js` (262 líneas) | ~60% del archivo |
| Páginas (12+) | **Ninguno** | 0% |
| Hooks (`useApi`, `useAuth`, `useNotificationsSSE`) | **Ninguno** | 0% |
| `AuthContext` | **Ninguno** | 0% |
| Routing protegido | **Ninguno** | 0% |
| Componentes UI | **Ninguno** | 0% |

## 4. Comportamiento deseado

### Métricas de cobertura objetivo
| Métrica | Umbral |
|---------|--------|
| Statements (páginas críticas) | ≥ 70% |
| Branches (páginas críticas) | ≥ 50% |
| Functions (hooks/contexto) | ≥ 80% |
| Lines (hooks/contexto) | ≥ 70% |

### Páginas críticas (prioridad 1)
1. `ParcelManagement` - CRUD encomiendas, filtros, modal crear/editar
2. `Logistics` - lotes, vehículos, asignación, mapa
3. `ProofOfDelivery` - listado, POD, upload evidencia
4. `Reports` - KPIs, gráficos, export CSV
4. `Dashboard` - KPIs, charts, actividad reciente
5. `ClientProfile` - mis encomiendas, perfil
5. `DriverDashboard` - mis entregas, POD

### Hooks/contexto (prioridad 2)
- `useApi` - request, error handling, auth header
- `useAuth` - login, logout, sesión, persistencia
- `useNotificationsSSE` - conexión, reconexión, eventos
- `AuthContext` - login, logout, permisos, `canAccess()`

## 5. Requisitos

| ID | Requisito | Prioridad |
|----|-----------|-----------|
| R1 | Tests de integración para `ParcelManagement` (listar, crear, editar, cancelar, tracking) | must |
| R2 | Tests de integración para `Logistics` (lotes, vehículos, asignar, mapa) | must |
| R3 | Tests de integración para `ProofOfDelivery` (listar, POD, upload) | must |
| R4 | Tests de integración para `Reports` (KPIs, gráficos, export) | must |
| R5 | Tests de integración para `Dashboard` (KPIs, charts, actividad) | must |
| R6 | Tests de integración para `ClientProfile` (mis encomiendas, perfil) | should |
| R7 | Tests de integración para `DriverDashboard` (mis entregas, POD) | should |
| R8 | Tests unitarios para `useApi` (request, error handling, auth) | must |
| R9 | Tests unitarios para `useAuth` (login, logout, sesión) | must |
| R10 | Tests unitarios para `useNotificationsSSE` (conexión, eventos) | should |
| R11 | Tests unitarios para `AuthContext` (login, logout, permisos, `canAccess`) | must |
| R12 | Tests de routing protegido (redirecciones por rol, 403/401) | must |
| R13 | Tests de componentes UI críticos (`DataTable`, `StatCard`, `LoadingSpinner`, `ErrorBanner`, `ConfirmModal`) | should |
| R14 | Configuración de cobertura con umbrales (≥70% statements páginas críticas) | must |
| R15 | Mocking de API con `msw` para tests de integración | must |

## 6. Criterios de aceptación

### R1 - ParcelManagement
- **Dado** usuario autenticado con rol Operator
- **Cuando** accede a `/app/encomiendas`
- **Entonces** ve listado paginado, puede filtrar, crear nueva encomienda (modal), ver tracking, cancelar

### R8 - useApi
- **Dado** llamada a `api.get('/parcels')`
- **Cuando** respuesta 200
- **Entonces** retorna datos parseados
- **Y cuando** respuesta 401
- **Entonces** lanza error con mensaje "No autenticado"
- **Y cuando** respuesta 403
- **Entonces** lanza error con mensaje "No tiene permisos para esta operacion"

### R11 - AuthContext
- **Dado** login exitoso
- **Cuando** `AuthContext` recibe token y user
- **Entonces** `user` y `token` se guardan en estado y localStorage
- **Y** `canAccess('/app/encomiendas')` retorna true para Operator
- **Y cuando** logout
- **Entonces** estado y localStorage se limpian

### R12 - Routing protegido
- **Dado** usuario sin autenticar
- **Cuando** accede a `/app/encomiendas`
- **Entonces** redirige a `/login`
- **Dado** Operator autenticado
- **Cuando** accede a `/app/usuarios` (solo Admin)
- **Entonces** redirige a `/app/dashboard` (403 handling)

## 7. Contratos de API (existentes, sin cambios)

Los tests usarán los endpoints ya definidos en `api.js`:
- `parcelsApi.list`, `create`, `update`, `cancel`, `tracking`
- `logisticsApi.listBatches`, `createBatch`, `assignBatch`, `listVehicles`
- `deliveriesApi.list`, `addPod`, `uploadEvidence`
- `reportsApi.kpis`, `dailyVolume`, `exportCsv`
- `dashboardApi.get`
- `usersApi.list`, `me`, `updateMe`
- `notificationsApi.list`, `markRead`, `markAllRead`

## 8. Casos de borde

- Red lenta/timeout en requests (testing de timeouts en `useApi`)
- Token expirado durante request (auto-refresh o logout)
- SSE desconexión/reconexión en `useNotificationsSSE`
- Usuario sin permisos accediendo a rutas protegidas
- Datos vacíos en listados (empty states)
- Errores de red en upload de archivos

## 9. Impacto en datos y migraciones

- **Migración Alembic**: No requerida (solo tests)
- **Reversible**: Sí (eliminar tests no afecta código productivo)
- **Objetos "Awen"**: No se tocan

## 10. Tests a crear

| Archivo | Tests | Tipo |
|---------|-------|------|
| `src/tests/pages/ParcelManagement.test.jsx` | 15+ | integración |
| `src/tests/pages/Logistics.test.jsx` | 15+ | integración |
| `src/tests/pages/ProofOfDelivery.test.jsx` | 10+ | integración |
| `src/tests/pages/Reports.test.jsx` | 10+ | integración |
| `src/tests/pages/Dashboard.test.jsx` | 10+ | integración |
| `src/tests/pages/ClientProfile.test.jsx` | 8+ | integración |
| `src/tests/pages/DriverDashboard.test.jsx` | 8+ | integración |
| `src/tests/hooks/useApi.test.js` | 12+ | unitario |
| `src/tests/hooks/useAuth.test.js` | 8+ | unitario |
| `src/tests/hooks/useNotificationsSSE.test.js` | 8+ | unitario |
| `src/tests/context/AuthContext.test.jsx` | 10+ | unitario |
| `src/tests/routing/ProtectedRoutes.test.jsx` | 8+ | integración |
| `src/tests/components/ui/DataTable.test.jsx` | 8+ | unitario |
| `src/tests/components/ui/StatCard.test.jsx` | 5+ | unitario |
| `src/tests/components/ui/LoadingSpinner.test.jsx` | 3+ | unitario |
| `src/tests/components/ui/ErrorBanner.test.jsx` | 3+ | unitario |
| `src/tests/components/ui/ConfirmModal.test.jsx` | 5+ | unitario |
| `vitest.config.js` | config | config |

**Total estimado**: ~150+ tests nuevos

## 11. Riesgos

- **Tiempo**: ~150 tests requiere tiempo significativo
- **Mantenibilidad**: Tests de integración frágiles si UI cambia frecuentemente
- **Mocking**: `msw` requiere configuración cuidadosa de handlers
- **Flakiness**: Tests de UI pueden ser inestables (timers, animaciones)
- **Cobertura real**: 70% statements no garantiza ausencia de bugs

## 12. Preguntas abiertas

- [x] **Framework de testing**: `vitest` + `@testing-library/react` + `msw`. Resuelto: se mantiene el stack.
- [x] **Mocking de API**: handlers de `msw` centralizados en `src/tests/mocks/handlers.js`. Resuelto: MSW se usa en el test de integración de `Dashboard`; el resto mockea módulos o `fetch` con Vitest para evitar que MSW intercepte esos dobles.
- [x] **Datos de prueba**: fixtures centralizados en `src/tests/fixtures/`. Resuelto: se reutilizan usuarios en tests de contexto y páginas.
- [x] **Cobertura de ramas**: 50% branches como umbral inicial. Resuelto: configurado en `vitest.config.js`; la cobertura real de páginas supera el 60%.
- [x] **Tests de snapshot**: no se incluyen. Resuelto: prioridad baja, se posponen.
- [x] **CI/CD**: ejecutar tests en PR obligatorio. Resuelto: forma parte de la Definition of Done.

## 13. Plan de verificación manual

1. `npm run test:coverage` → verificar umbrales ≥70% statements en páginas críticas.
2. `npm test src/tests/pages/ParcelManagement.test.jsx` → todos pasan.
3. `npm test src/tests/hooks/useApi.test.js` → todos pasan.
4. `npm test src/tests/context/AuthContext.test.jsx` → todos pasan.
5. `npm test src/tests/routing/ProtectedRoute.test.jsx` → todos pasan.
6. Verificar reporte de cobertura HTML en `coverage/index.html`.

## 14. Resultado de la implementación

Fecha de cierre local: 2026-10-30. Integrada en `develop` mediante PR #13.

- **Suite**: 20 archivos, 165 tests, todos en verde.
- **Cobertura** (`npm run test:coverage`):
  - Global: 75.55% statements, 61.98% branches, 78.9% lines.
  - Páginas críticas: 72.18% statements, 60.77% branches, 75.6% lines.
  - Hooks: 100% statements/lines/functions.
  - Contexto: 100% statements/lines/functions.
- **MSW**: integración real en `Dashboard.test.jsx` con `src/tests/mocks/setup.js` y los handlers
  centralizados. No se activa globalmente porque interfiere con los tests que sustituyen `fetch`.
- **R12**: `src/tests/routing/ProtectedRoute.test.jsx` cubre redirección a login, acceso permitido y
  redirección al dashboard por rol.
- **R14**: umbrales configurados en `vitest.config.js` y script `test:coverage` en `package.json`.
- **Lint**: `npx eslint src/tests` pasa; `npm run lint` sigue fallando por deuda preexistente en
  páginas de producción, registrada en `NOTAS.md` para Fase 5.


---

> **Nota**: Esta fase se enfoca en **cobertura de código crítico**, no en tests E2E completos. Los E2E (Cypress/Playwright) se posponen a fase posterior.