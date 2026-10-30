# NOTAS — Hallazgos fuera de alcance

Registro de cosas detectadas que **no** se arreglan en la fase actual. Cada una debería
convertirse en una spec o en una decisión cuando le toque.

## Estado de fases

- **Fase 1** (Seguridad y autorización): cerrada y mergeada en `develop` (PR #9).
- **Fase 2** (Almacenamiento serverless): cerrada y mergeada en `develop` (PR #11).
- **Fase 3** (Branch scoping): implementada en `feat/fase-3-branch-scoping`; PR pendiente de crear.
- **Fase 4** (Testing Frontend): tests implementados en `feat/fase-4-testing-frontend`; PR pendiente de crear.

## Fase 1 — Seguridad y autorización (COMPLETADA)

### Implementado en esta fase
- **R2**: Autorización por rol (RBAC), matriz centralizada en `app/core/permissions.py`.
- **R3**: Matriz de permisos declarada en un único lugar y testeable.
- **R4**: Usuario inactivo bloqueado; login y token rechazados con 403 "Usuario inactivo".
- **R5**: El arranque falla si `AWEN_SECRET_KEY=CHANGE_ME` o no está definida.
- **Fix SSE**: Mensaje "Not authenticated" → "No autenticado" en `notifications_stream.py`.
- Tests nuevos: `TestRoleBasedAccess`, `TestRoleBasedAuthorization`, `TestPermissionMatrixCentralized`,
  `TestInactiveUser`, `TestSecretKeyValidation`.

### Bugs preexistentes NO arreglados (fuera de alcance Fase 1)

#### Backend
1. **`test_branches.py::test_delete_branch_soft`**: espera soft delete (`active=False`) pero la API
   hace hard delete (404).
2. **`test_logistics.py::test_assign_batch`**: error pydantic, `parcels=None` pero el schema espera lista.
3. **`test_dashboard.py::test_dashboard_empty_data`**: error en test con datos vacíos.

## Decisiones pendientes

### 1. Licencia MIT contradice la regla de privacidad

- `LICENSE` contiene una licencia **MIT**.
- `AGENTS.md` (regla 7) y `docs/sdd/constitucion.md` (punto 9) prohíben aplicar licencias
  open-source.
- **Decisión requerida:** eliminar `LICENSE`, cambiarlo por uno privado o corregir la regla.

### 2. `start_backend.bat` tiene una ruta absoluta hardcodeada

- `back-end/start_backend.bat:2` apunta a `C:\Users\espin\Desktop\AWEN\AWEN\back-end`.
- No funciona en otra máquina. **Sugerencia:** usar `cd /d "%~dp0"`.

### 3. Protección de la rama `develop`

- `develop` ya existe en el remoto, pero falta configurar branch protection y CI obligatorio.

### 4. `gh` CLI sin autenticar

- No se pueden crear Pull Requests desde el agente. Los PR de Fase 3 y Fase 4 deben abrirse
  manualmente desde GitHub.

## Hallazgos técnicos

### 5. Lint global del frontend sigue en rojo (preexistente)

`npx eslint src/tests` pasa sin errores. `npm run lint` falla por deuda previa en código de
producción, ajena al alcance de Fase 4:

- `AuthContext.jsx`: bloques `catch` vacíos (`no-empty`).
- `DriverDashboard.jsx`: variable `deliveryPhoto` sin usar.
- `Reports.jsx`: `PARCEL_STATUS_LABELS` importado sin usar.
- `BranchManagement.jsx`, `ClientProfile.jsx`, `ParcelManagement.jsx`, `Tracking.jsx`,
  `UserManagement.jsx`: `setState` sincrónico dentro de `useEffect` (`react-hooks/set-state-in-effect`).
- `ClientProfile.jsx`, `ParcelManagement.jsx`: `useMapEvents` llamado condicionalmente,
  `MapClickHandler` creado durante el render y hooks con dependencias incompletas.
- `Logistics.jsx`: `loadData` accedida antes de su declaración.
- `Dashboard.jsx`: dependencia `execute` ausente en `useEffect`.

**Tratado en:** Fase 5 (limpieza de lint frontend). No se tocó en Fase 4 para no mezclar
refactors de producción con la suite de tests.

### 6. Cobertura de tests del frontend

- Antes de Fase 4 solo existía `api.test.js` para una app con 12+ páginas.
- Fase 4 añade tests de páginas críticas, hooks, contexto, componentes y routing protegido.
- Cobertura actual con `npm run test:coverage`: 75.55% statements global, 72.18% statements en
  páginas críticas, 61.98% branches, 78.9% lines.
- `ClientProfile.jsx` sigue en 50.55% statements por los flujos de mapa/creación; es la mayor
  oportunidad de mejora en una fase posterior.

### 7. Estrategia de mocking

- `msw` se usa en `Dashboard.test.jsx` como test de integración real con los handlers
  centralizados de `src/tests/mocks/handlers.js`.
- El resto de tests mockea módulos de servicio o `fetch` con Vitest. Activar MSW globalmente
  interceptaba esos `fetch` y hacía fallar la suite; por eso no se importa en `src/tests/setup.js`.

### 8. Uploads en un entorno serverless

- `back-end/app/main.py:74` crea y monta `uploads/` en el sistema de archivos local.
- En Vercel el filesystem es de solo lectura salvo `/tmp` y no persiste entre invocaciones.
- **Tratado en:** `docs/specs/fase-2-storage.md` (Vercel Blob, pre-signed URLs).

### 9. Rate limit en memoria por proceso

- `back-end/app/core/ratelimit.py:15` guarda el estado en un `dict` del proceso.
- Con varios workers o en serverless el límite no es global y se reinicia al arrancar.
- **Tratado en:** `docs/specs/fase-1-seguridad.md` (R6, marcado `could`).

### 10. `front-end/README.md` es la plantilla por defecto de Vite

- No describe el proyecto. **Sugerencia:** reemplazarlo por documentación real o eliminarlo.

### 11. Historial con commits directos a `main`

- El historial muestra trabajo integrado sin PR. No se puede arreglar retroactivamente; la regla
  aplica desde ahora.
