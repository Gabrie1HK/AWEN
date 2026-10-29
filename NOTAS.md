# NOTAS — Hallazgos fuera de alcance

Registro de cosas detectadas que **no** se arreglan en la fase actual. Cada una debería
convertirse en una spec o en una decisión cuando le toque.

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