# NOTAS — Hallazgos fuera de alcance

Registro de cosas detectadas que **no** se arreglan en la fase actual. Cada una debería
convertirse en una spec o en una decisión cuando le toque.

<<<<<<< HEAD
## Fase 1 — Seguridad y autorización (COMPLETADA)

### ✅ Implementado en esta fase:
- **R2**: Autorización por rol (RBAC) - matriz centralizada en `app/core/permissions.py`
- **R3**: Matriz de permisos declarada en un único lugar y testeable
- **R4**: Usuario inactivo bloqueado - login y token rechazados con 403 "Usuario inactivo"
- **R5**: Arranque falla si `AWEN_SECRET_KEY=CHANGE_ME` o no definida
- **Fix SSE**: Mensaje "Not authenticated" → "No autenticado" en `notifications_stream.py`
- Tests nuevos: `TestRoleBasedAccess`, `TestRoleBasedAuthorization`, `TestPermissionMatrixCentralized`, `TestInactiveUser`, `TestSecretKeyValidation`

### Bugs pre-existentes NO arreglados (fuera de alcance Fase 1):

#### Backend:
1. **`test_branches.py::test_delete_branch_soft`** - Espera soft delete (active=False) pero API hace hard delete (404)
2. **`test_logistics.py::test_assign_batch`** - Error pydantic: `parcels=None` pero schema espera lista
3. **`test_dashboard.py::test_dashboard_empty_data`** - ERROR en test con datos vacíos

#### Frontend (lint - errores pre-existentes):
1. **AuthContext.jsx** - Empty block statements (try/catch vacíos)
2. **BranchManagement.jsx, ClientProfile.jsx, ParcelManagement.jsx, UserManagement.jsx, Tracking.jsx** - `setState` sincrónico en useEffect
3. **ClientProfile.jsx, ParcelManagement.jsx** - `useMapEvents` llamado condicionalmente + componentes creados en render (`MapClickHandler`)
4. **Logistics.jsx** - `loadData` accedida antes de declararse
4. **DriverDashboard.jsx** - Variable `deliveryPhoto` no usada
5. **Reports.jsx** - `PARCEL_STATUS_LABELS` definido pero no usado
6. **api.test.js** - `requestForm` importado pero no usado, `global` no definido, `result` asignado pero no usado
7. **setup.js** - `beforeEach` no definido

#### Frontend (tests - fallos pre-existentes):
1. **Login.test.jsx** - Tests esperan textos que no existen en UI ("Credenciales inválidas", "Error de conexión", "Credenciales de prueba")
2. Tests reciben errores de JS ("Cannot read properties of null (reading 'role')", "Network error") en lugar de mensajes de API

#### Otros:
1. **Licencia MIT** en `LICENSE` contradice regla de privacidad (AGENTS.md:7, constitucion.md:9)
2. **`start_backend.bat`** tiene ruta hardcodeada (`C:\Users\espin\Desktop\AWEN\AWEN\back-end`)
3. **Rama `develop`** no publicada en remoto
4. **Uploads en serverless (Vercel)** - FS local no persiste (`main.py:74` monta `uploads/`)
5. **Rate limit en memoria** - No distribuido (R6 pospuesto)
6. **Cobertura tests frontend baja** - Solo `api.test.js` para app con 12+ páginas

---

## Próximas fases sugeridas:

| Fase | Tema | Prioridad |
|------|------|-----------|
| 2 | Almacenamiento serverless (S3/R2/Blob) para uploads/POD | Alta |
| 3 | Filtro por sucursal (branch scoping) en services | Alta |
| 4 | Testing Frontend - Cobertura páginas críticas | Media |
| 5 | Decisión Licencia + fix start_backend.bat | Media |
| 6 | Publicar rama develop + CI/CD | Baja |
=======
## Decisiones pendientes

### 1. Licencia MIT contradice la regla de privacidad

- `LICENSE` contiene una licencia **MIT**.
- `AGENTS.md` (regla 7) y `docs/sdd/constitucion.md` (punto 9) prohíben aplicar licencias
  open-source.
- **Decisión requerida:** eliminar `LICENSE`, cambiarlo por uno privado, o corregir la regla.

## Hallazgos técnicos

### 2. No hay autorización por rol (RBAC)

- Todas las rutas protegidas solo verifican autenticación con `Depends(get_current_user)`.
- `ForbiddenError` existe en `back-end/app/core/errors.py:22` pero no se usa en rutas.
- `back-end/tests/test_authorization.py` solo prueba 401, no 403.
- **Tratado en:** `docs/specs/fase-1-seguridad.md` (R2, R3).

### 3. `start_backend.bat` tiene una ruta absoluta hardcodeada

- `back-end/start_backend.bat:2` apunta a `C:\Users\espin\Desktop\AWEN\AWEN\back-end`.
- No funciona en otra máquina. **Sugerencia:** usar `cd /d "%~dp0"`.

### 4. Mensaje de error en inglés

- `back-end/app/api/routes/notifications_stream.py:21` devuelve `"Not authenticated"`.
- Viola la convención de mensajes en español sin tildes.
- **Tratado en:** `docs/specs/fase-1-seguridad.md` (tabla de errores).

### 5. Rate limit en memoria por proceso

- `back-end/app/core/ratelimit.py:15` guarda el estado en un `dict` del proceso.
- Con varios workers o en serverless el límite no es global y se reinicia al arrancar.
- **Tratado en:** `docs/specs/fase-1-seguridad.md` (R6, marcado `could`).

### 6. Uploads en un entorno serverless

- `back-end/app/main.py:74` crea y monta `uploads/` en el sistema de archivos local.
- En Vercel el filesystem es de solo lectura salvo `/tmp` y no persiste entre invocaciones.
- **Riesgo:** los comprobantes de entrega (POD) podrían perderse en producción.

### 7. Cobertura de tests del frontend baja

- Solo 8 archivos de test en `front-end/tests/` para una app con dashboard, logística, mapas,
  notificaciones y reportes.
- **Sugerencia:** antes de la próxima fase de UI, medir cobertura y añadir tests de páginas
  críticas (parcels, deliveries, logistics).

### 8. `front-end/README.md` es la plantilla por defecto de Vite

- No describe el proyecto. **Sugerencia:** reemplazarlo por documentación real o eliminarlo.

### 9. El repo no tenía rama `develop`

- `git-workflow` la exige, pero solo existía `main`.
- **Hecho:** se creó `develop` local desde `main` (sin push). Falta configurar protección de
  rama y publicarla en el remoto.

### 10. Historial con commits directos a `main`

- El historial muestra trabajo integrado sin PR. No se puede arreglar retroactivamente; la regla
  aplica desde ahora.

## Entorno local

- En esta máquina no hay `python` en PATH, ni `node_modules` en `front-end/`, ni entorno virtual.
- La línea base de tests no se pudo ejecutar aquí. Antes de la primera fase hay que dejar el
  entorno reproducible (ver `README.md`).
>>>>>>> origin/develop
