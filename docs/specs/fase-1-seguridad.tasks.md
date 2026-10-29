---
fase: 1
spec: ../specs/fase-1-seguridad.md
plan: ./fase-1-seguridad.plan.md
---

# Tareas — Fase 1: Seguridad y autorización

Checklist ejecutable. Cada tarea debe caber en un commit y citar su requisito.

## Preparación

- [ ] Rama creada desde `develop`: `fix/fase-1-seguridad` (ya existe)
- [ ] Línea base de tests ejecutada y anotada (`./scripts/verify.ps1` o manual)
- [ ] Spec aprobada (sin preguntas abiertas) ✅

## Tests RED

- [ ] `test_rol_sin_permiso_devuelve_403` para R2 (integración)
- [ ] `test_admin_puede_gestionar_usuarios` para R2 (integración)
- [ ] `test_matriz_permisos_centralizada` para R3 (unitario)
- [ ] `test_usuario_inactivo_no_puede_login` para R4 (integración)
- [ ] `test_token_de_usuario_inactivo_rechazado` para R4 (integración)
- [ ] `test_arranque_falla_con_secret_key_por_defecto` para R5 (unitario)
- [ ] Confirmado que **todos fallan por la razón correcta** antes de tocar implementación

## Implementación GREEN

### R3 — Matriz centralizada (primero, la usan los demás)
- [ ] Crear `back-end/app/core/permissions.py` con:
    - Enum/constantes de roles
    - Dict `ENDPOINT_PERMISSIONS: dict[str, set[Role]]` con la matriz de la spec
    - Función `require_roles(*roles: Role)` que retorna `Depends` para rutas
- [ ] Tests unitarios de la matriz pasan

### R5 — Secret key obligatoria
- [ ] En `back-end/app/core/config.py` o `main.py`: validar al arrancar que `settings.secret_key != "CHANGE_ME"`; si lo es, `raise RuntimeError("AWEN_SECRET_KEY no configurada")`
- [ ] Test unitario pasa

### R4 — Usuario inactivo
- [ ] En `back-end/app/services/auth.py` `authenticate()`: verificar `user.active` antes de emitir token; si `False`, `raise ForbiddenError("Usuario inactivo")`
- [ ] En `get_current_user()` (dependencies): verificar `user.active` en cada request; si `False`, `raise ForbiddenError("Usuario inactivo")`
- [ ] Tests de integración pasan

### R2 — RBAC en rutas
- [ ] Importar `require_roles` en cada router (`auth.py`, `parcels.py`, `users.py`, `branches.py`, `deliveries.py`, `logistics.py`, `notifications.py`, `reports.py`, `dashboard.py`, `tracking.py`)
- [ ] Reemplazar `_user=Depends(get_current_user)` por `_user=Depends(require_roles(...))` con los roles de la matriz (sección 6 de la spec)
- [ ] Endpoint público `/tracking` **sin** dependencia de auth
- [ ] Tests de integración pasan

### R1 — Mantener 401 (sin cambios de código, solo tests)
- [ ] Verificar que tests existentes de 401 siguen pasando

## Verificación

- [ ] `./scripts/verify.ps1` en verde (Windows) o `bash scripts/verify.sh` (Linux/macOS)
- [ ] CI en verde en PR hacia `develop`
- [ ] Revisión manual según la spec (sección 14)

## Cierre

- [ ] Spec marcada como `cerrada` (cambiar `estado: cerrada` en frontmatter)
- [ ] `docs/sdd/roadmap.md` actualizado (fase 1 → `cerrada`, añadir fase 2 si hay spec)
- [ ] `NOTAS.md` actualizado con hallazgos fuera de alcance (si los hay)
- [ ] PR mergeado en `develop`
- [ ] Mensaje de commit siguiendo Conventional Commits:
  ```
  fix(seguridad): implementar RBAC, usuario inactivo y secret key obligatoria

  - R2: autorización por rol en todas las rutas protegidas
  - R3: matriz de permisos centralizada en app/core/permissions.py
  - R4: bloquear login y requests de usuarios inactivos
  - R5: fallar al arranque si AWEN_SECRET_KEY=CHANGE_ME
  - Tests de integración y unitarios para R2–R5

  Closes #fase-1-seguridad
  ```