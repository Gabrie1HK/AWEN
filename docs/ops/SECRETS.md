# Gestión de Secretos — AWEN

## Principios

1. **Nunca** commitear secretos al repositorio
2. **Rotar** secretos cada 90 días
3. **Principio de menor privilegio**: cada entorno tiene sus propios secretos
4. **Auditoría**: registrar cambios en `CHANGELOG_SECRETS.md`

---

## Inventario de Secretos

### Categorías

| Categoría | Secretos | Rotación | Almacenamiento |
|-----------|----------|----------|----------------|
| **Autenticación** | `AWEN_SECRET_KEY` | 90 días | GitHub Environments |
| **Base de Datos** | `AWEN_DATABASE_URL` | Al cambiar credenciales | Railway + GitHub |
| **Almacenamiento** | `AWEN_BLOB_READ_WRITE_TOKEN` | 90 días | Vercel + GitHub |
| **Configuración** | `AWEN_CORS_ORIGINS`, `AWEN_STORAGE_BUCKET` | Al cambiar dominio | GitHub + Vercel + Railway |

---

## Detalle por Secreto

### `AWEN_SECRET_KEY`

- **Descripción**: Clave para firmar/verificar JWT tokens
- **Formato**: String aleatorio ≥ 32 caracteres (base64 o hex)
- **Generación**: `openssl rand -base64 32`
- **Rotación**: Cada 90 días
- **Impacto rotación**: Invalida todos los tokens activos → usuarios deben relogear
- **Almacenamiento**: GitHub Environments (dev/staging/prod)
- **Uso**: `app.core.security.create_access_token()`, `get_current_user()`

### `AWEN_DATABASE_URL`

- **Descripción**: URL de conexión a PostgreSQL
- **Formato**: `postgresql+psycopg://user:pass@host:port/db`
- **Rotación**: Al cambiar contraseña BD o migrar proveedor
- **Impacto**: Requiere redeploy backend
- **Almacenamiento**: Railway (auto) + GitHub Environments
- **Uso**: `app.database.database.get_db()`

### `AWEN_BLOB_READ_WRITE_TOKEN`

- **Descripción**: Token de escritura/lectura en Vercel Blob
- **Formato**: Token Vercel (prefijo `vercel_blob_`)
- **Rotación**: Cada 90 días o si se compromete
- **Impacto**: Fallos subida/descarga archivos
- **Almacenamiento**: Vercel Dashboard + GitHub Environments
- **Uso**: `app.services.storage.StorageService`

### `AWEN_STORAGE_BUCKET`

- **Descripción**: Nombre del bucket en Vercel Blob
- **Formato**: String (ej. `awen-prod`)
- **Rotación**: Al crear nuevo bucket
- **Impacto**: Archivos nuevos en bucket nuevo
- **Almacenamiento**: GitHub + Vercel + Railway

### `AWEN_CORS_ORIGINS`

- **Descripción**: Orígenes permitidos para CORS
- **Formato**: JSON array o comma-separated
- **Ejemplo**: `["https://awen.app","https://staging.awen.app"]`
- **Rotación**: Al añadir/quitar dominios
- **Impacto**: Requests bloqueados si falta origen
- **Almacenamiento**: GitHub + Vercel + Railway

---

## Procedimiento de Rotación

### Rotación Programada (Cada 90 días)

1. **Planificar**: Crear issue "Rotación secretos QX-202X"
2. **Generar nuevos valores**:
   ```bash
   # Secret key
   openssl rand -base64 32
   
   # Database password (en Railway/PostgreSQL)
   # Blob token (en Vercel Dashboard)
   ```
2. **Actualizar en orden**:
   1. Vercel Blob token (efecto inmediato en frontend)
   2. GitHub Environments (staging → production)
   3. Railway variables (auto-deploy al cambiar)
   4. Vercel Environment Variables
2. **Verificar**:
   - CI pasa en staging
   - Healthcheck OK en staging
   - Login funciona en staging
   - Deploy a production
5. **Revocar antiguos**: Eliminar tokens/vars antiguos
6. **Documentar**: Actualizar `CHANGELOG_SECRETS.md`

### Rotación de Emergencia (Compromiso)

1. **Inmediato**: Generar nuevo secreto
2. **Actualizar** en orden inverso: production → staging → development
3. **Invalidar sesiones**: Cambiar `AWEN_SECRET_KEY` fuerza relogin
4. **Investigar**: Cómo se comprometió, mitigar vector
5. **Post-mortem**: Documentar en `INCIDENT_RESPONSE.md`

---

## Almacenamiento por Plataforma

### GitHub Environments

```
Settings → Environments → [development|staging|production]
  → Environment secrets
    AWEN_SECRET_KEY: ***
    AWEN_DATABASE_URL: ***
    AWEN_BLOB_READ_WRITE_TOKEN: ***
    AWEN_STORAGE_BUCKET: ***
    AWEN_CORS_ORIGINS: ***
```

**Protección**: Requerir reviewers para `production` environment.

### Railway

```bash
# Via CLI
railway variables set AWEN_SECRET_KEY=*** --environment production
railway variables set AWEN_BLOB_READ_WRITE_TOKEN=*** --environment production

# O Dashboard: Service → Variables → Add
```

### Vercel

```bash
# CLI
vercel env add AWEN_BLOB_READ_WRITE_TOKEN production

# Dashboard: Project → Settings → Environment Variables
```

---

## Checklist de Auditoría (Trimestral)

- [ ] Todos los secretos tienen dueño documentado
- [ ] Rotación realizada en últimos 90 días
- [ ] No hay secretos en código/commits (`git log --all --full-history -- "*secret*"`)
- [ ] Environments de GitHub tienen protection rules
- [ ] Railway/Vercel tienen 2FA habilitado
- [ ] `CHANGELOG_SECRETS.md` actualizado

---

## CHANGELOG_SECRETS.md (Template)

```markdown
# Changelog de Secretos

## 2026-Q4
- 2026-10-30: Rotación programada Q4
  - AWEN_SECRET_KEY rotado (dev/staging/prod)
  - AWEN_BLOB_READ_WRITE_TOKEN rotado
  - Responsable: @gabrie1hk
  - Verificado: staging OK, production OK

## 2026-Q3
- 2026-07-15: Rotación de emergencia - token Vercel expuesto en log
  - AWEN_BLOB_READ_WRITE_TOKEN rotado (emergencia)
  - Responsable: @gabrie1hk
  - Verificado: staging OK, production OK
```

---

## Referencias

- [GitHub Environments](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment)
- [Railway Variables](https://docs.railway.app/develop/variables)
- [Vercel Environment Variables](https://vercel.com/docs/concepts/projects/environment-variables)
- [12 Factor App - Config](https://12factor.net/config)