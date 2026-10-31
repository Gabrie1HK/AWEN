# Guía de Despliegue — AWEN

## Resumen

Este documento describe el proceso de despliegue para los entornos:
- **Development** (local)
- **Staging** (Railway + Vercel Preview)
- **Production** (Railway + Vercel Production)

## Arquitectura de Despliegue

```
┌─────────────────┐     ┌─────────────────┐
│   Frontend      │     │   Backend       │
│   (Vercel)      │────▶│   (Railway)     │
└─────────────────┘     └─────────────────┘
                              │
                              ▼
                        ┌─────────────────┐
                        │   PostgreSQL    │
                        │   (Railway)     │
                        └─────────────────┘
```

## Requisitos Previos

- Cuenta en [GitHub](https://github.com)
- Cuenta en [Vercel](https://vercel.com)
- Cuenta en [Railway](https://railway.app)
- Docker instalado (para builds locales)
- Python 3.12+ y Node.js 22+

---

## 1. Configuración Inicial (Una sola vez)

### 1.1 Repositorio GitHub

1. Fork/clone del repositorio
2. Configurar branch protection en `develop` (ver sección Branch Protection)
3. Crear Environments en GitHub: `development`, `staging`, `production`

### 1.2 Vercel (Frontend)

1. Conectar repositorio en Vercel
2. Configurar:
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm ci`
3. Variables de entorno en Vercel:
   - `VITE_API_URL`: URL del backend (ej. `https://awen-production.up.railway.app`)

### 1.3 Railway (Backend + PostgreSQL)

1. Crear proyecto en Railway
2. Añadir servicio **PostgreSQL** (managed)
3. Añadir servicio **Web Service** (Dockerfile)
4. Conectar repositorio GitHub
4. Configurar variables de entorno (ver sección Secrets)

---

## 2. Variables de Entorno (Secrets)

### GitHub Environments

Crear 3 environments en GitHub: `development`, `staging`, `production`

| Variable | Development | Staging | Production | Descripción |
|----------|-------------|---------|------------|-------------|
| `AWEN_SECRET_KEY` | `dev-key-...` | `staging-key-...` | `prod-key-...` | JWT signing key (mín. 32 chars) |
| `AWEN_DATABASE_URL` | `postgresql://...` | `postgresql://...` | `postgresql://...` | URL conexión BD |
| `AWEN_BLOB_READ_WRITE_TOKEN` | `vercel_blob_...` | `vercel_blob_...` | `vercel_blob_...` | Token Vercel Blob |
| `AWEN_STORAGE_BUCKET` | `awen-dev` | `awen-staging` | `awen-prod` | Bucket almacenamiento |
| `AWEN_CORS_ORIGINS` | `http://localhost:5173` | `https://*.vercel.app` | `https://awen.app` | CORS origins |

### Vercel Environment Variables

| Variable | Valor |
|----------|-------|
| `VITE_API_URL` | URL del backend Railway |

### Railway Variables

| Variable | Valor |
|----------|-------|
| `AWEN_SECRET_KEY` | (desde GitHub secret) |
| `AWEN_DATABASE_URL` | `${{RAILWAY_POSTGRES_URL}}` (auto) |
| `AWEN_BLOB_READ_WRITE_TOKEN` | (desde GitHub secret) |
| `AWEN_STORAGE_BUCKET` | `awen-prod` |
| `AWEN_CORS_ORIGINS` | `https://awen.app,https://staging.awen.app` |

---

## 3. Despliegue Local (Development)

### Backend

```bash
cd back-end
cp .env.example .env  # Editar con valores locales
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd front-end
cp .env.example .env.local  # VITE_API_URL=http://localhost:8000
npm ci
npm run dev
```

### Base de Datos Local

```bash
docker run -d \
  --name awen-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=awen_dev \
  -p 5432:5432 \
  postgres:16-alpine
```

---

## 4. Pipeline CI/CD (GitHub Actions)

### Trigger

- Push a `develop` → Deploy a Staging
- Push a `main` → Deploy a Production
- Pull Request a `develop`/`main` → CI checks

### Jobs

1. **Backend Tests** (con PostgreSQL 16 service container)
2. **Frontend Lint + Tests + Build**
3. **Docker Build** (backend)
4. **Deploy Staging** (si push a `develop` y CI pasa)
5. **Deploy Production** (si push a `main` y CI pasa, requiere approval manual)

### Ver CI localmente

```bash
# Backend
cd back-end
AWEN_SECRET_KEY=test AWEN_DATABASE_URL=postgresql://postgres:postgres@localhost:5432/awen_test python -m pytest tests -q

# Frontend
cd front-end
npm run lint && npm test && npm run build
```

---

## 5. Despliegue a Staging

### Automático (Push a `develop`)

1. Push a rama `develop`
2. GitHub Actions ejecuta CI
3. Si CI pasa → Deploy automático a:
   - **Frontend**: Vercel Preview URL (ej. `awen-git-develop-gabrie1hk.vercel.app`)
   - **Backend**: Railway Staging environment

### Manual (si CI falla pero se necesita deploy)

```bash
# En Railway dashboard → Service → Deployments → Redeploy
# En Vercel dashboard → Deployments → Redeploy
```

---

## 6. Despliegue a Producción

### Requisitos

- CI passing en `main`
- Aprobación manual en GitHub Actions (required reviewer)
- Version tag opcional: `git tag v1.0.0 && git push origin v1.0.0`

### Proceso

1. Merge PR a `main` (o push directo si autorizado)
2. GitHub Actions ejecuta CI completo
3. Si CI pasa → Job `deploy-production` espera approval manual
4. Aprobar en GitHub Actions UI
3. Deploy a:
   - **Frontend**: `https://awen.app` (Vercel Production)
   - **Backend**: Railway Production environment

### Rollback Producción

```bash
# Railway
railway rollback  # O en dashboard: Deployments → Previous → Redeploy

# Vercel
vercel rollback [deployment-url]  # O en dashboard: Deployments → Previous → Promote to Production
```

---

## 7. Verificación Post-Deploy

### Healthcheck

```bash
# Backend
curl https://awen-production.up.railway.app/health
# Respuesta esperada: {"status":"ok","checks":{"db":true},"version":"x.y.z"}

# Frontend
curl -I https://awen.app
# Verificar headers de seguridad
```

### Smoke Tests

1. Login con usuario admin
2. Crear encomienda
3. Verificar tracking público
4. Verificar reportes

---

## 8. Rollback de Emergencia

### Backend (Railway)

```bash
# Opción 1: CLI
railway rollback

# Opción 2: Dashboard
# Services → awen-backend → Deployments → [previous] → Redeploy
```

### Frontend (Vercel)

```bash
# CLI
vercel rollback [deployment-url]

# Dashboard
# Project → Deployments → [previous] → Promote to Production
```

### Base de Datos

```bash
# Solo si migración falló
alembic downgrade -1  # En backend container
```

---

## 8. Troubleshooting

| Problema | Causa | Solución |
|----------|-------|----------|
| CI falla en backend | PostgreSQL no ready | Verificar healthcheck en workflow |
| Deploy Railway falla | Healthcheck falla | Verificar `/health` endpoint |
| Vercel build falla | Node version mismatch | Verificar `node-version` en workflow |
| CORS error | Origin no permitido | Actualizar `AWEN_CORS_ORIGINS` |
| JWT invalid | Secret mismatch | Verificar `AWEN_SECRET_KEY` en todos lados |
| DB connection refused | BD no iniciada | Verificar PostgreSQL service en CI/Railway |

---

## 9. Contactos y Escalación

| Rol | Contacto | Escala |
|-----|----------|--------|
| DevOps | @gabrie1hk | Infraestructura, CI/CD |
| Backend Lead | @gabrie1hk | API, BD, Performance |
| Frontend Lead | @gabrie1hk | Build, Deploy, UX |
| Security | @gabrie1hk | Secrets, Vulnerabilidades |

---

**Última actualización**: 2026-10-30  
**Versión**: 1.0  
**Próxima revisión**: Al añadir nuevo entorno o cambiar proveedor