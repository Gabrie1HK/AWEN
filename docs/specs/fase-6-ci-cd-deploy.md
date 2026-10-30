---
fase: 6
nombre: ci-cd-deploy
estado: aprobada
rama: feat/fase-6-ci-cd-deploy
autor:
fecha: 2026-10-30
---

# Fase 6 — CI/CD, Branch Protection y Despliegue

## 1. Contexto y problema

El repositorio tiene deuda de infraestructura que impide la entrega continua segura:

1. **Rama `develop` sin protección**: cualquiera puede hacer push directo o merge sin CI verde.
2. **CI incompleto**: Phase 5 R6/R9 (PostgreSQL 16 en CI) quedó pendiente porque el token de GitHub no tiene scope `workflow`.
3. **Despliegue manual**: Frontend en Vercel (automático por push), pero backend no tiene pipeline de deploy.
4. **Variables de entorno**: `AWEN_SECRET_KEY`, `DATABASE_URL`, credenciales Vercel Blob, etc. sin gestión centralizada.
4. **Sin monitoreo/alertas**: no hay visibilidad de salud de la API en producción.

Esta fase establece branch protection, completa el CI con PostgreSQL, automatiza el despliegue y documenta la operativa.

## 2. Alcance

### Dentro del alcance

- **Branch protection**: `develop` requiere PR, CI verde, 1 aprobación, branches actualizados.
- **CI completo**: Job backend con PostgreSQL 16 (service container), cache pip, healthcheck.
- **Deploy frontend**: Vercel automático (ya configurado, validar y documentar).
- **Deploy backend**: Pipeline a Railway/Render/Fly.io (elegir uno) con healthcheck.
- **Secrets management**: GitHub Environments + secrets por entorno (dev/staging/prod).
- **Documentación operativa**: `DEPLOY.md`, `SECRETS.md`, `INCIDENT_RESPONSE.md`.
- **Healthcheck endpoint**: `GET /health` en backend (readiness + liveness).

### Fuera del alcance (no-goals)

- Tests E2E (Cypress/Playwright) — fase posterior.
- Monitoreo avanzado (Prometheus/Grafana/Datadog) — fase posterior.
- Blue/green o canary deployments — fase posterior.
- Migración a Kubernetes — fase posterior.
- Backups automáticos de BD — fase posterior.

## 3. Comportamiento actual

| Área | Estado |
|------|--------|
| Rama `develop` | Sin protection, push directo permitido. |
| Workflow CI (`.github/workflows/ci.yml`) | Backend sin PostgreSQL (R6/R9 pendientes). |
| Frontend deploy | Vercel automático por push a `main`/`develop`. |
| Backend deploy | Manual (uvicorn local o Docker manual). |
| Secrets | En repo (`.env` local) o Vercel dashboard. |
| Healthcheck | No existe endpoint `/health`. |
| Documentación deploy | Dispersa en README y issues. |

Archivos relevantes:
- `.github/workflows/ci.yml` — workflow actual.
- `vercel.json` — config Vercel (proyecto `awen`).
- `back-end/Dockerfile` — no existe (crear).
- `back-end/app/main.py` — añadir `/health`.

## 4. Comportamiento deseado

- `develop` protegida: solo merge via PR con CI verde + 1 review.
- CI en verde en todo PR a `develop`/`main` (backend + frontend).
- Push a `develop` → deploy automático a staging (Vercel preview + backend staging).
- Push a `main` → deploy automático a producción.
- Secrets rotables vía GitHub Environments (`development`, `staging`, `production`).
- Endpoint `GET /health` responde `{"status":"ok","checks":{"db":true}}` en < 200ms.
- Documentación operativa centralizada en `docs/ops/`.

## 5. Requisitos

| ID | Requisito | Prioridad |
|----|-----------|-----------|
| R1 | Branch protection en `develop`: required PR, CI passing, 1 approval, dismiss stale reviews, require up-to-date branch. | must |
| R2 | CI backend con PostgreSQL 16: service container `postgres:16-alpine`, healthcheck `pg_isready`, `AWEN_DATABASE_URL` inyectada. | must |
| R3 | Healthcheck endpoint `GET /health` en backend: verifica DB connectivity, responde en < 200ms. | must |
| R4 | Deploy backend automatizado: Dockerfile multi-stage, deploy a Railway/Render/Fly.io con healthcheck y rollback automático. | must |
| R5 | GitHub Environments + secrets: `development`, `staging`, `production` con `AWEN_SECRET_KEY`, `DATABASE_URL`, `BLOB_*`, etc. | must |
| R6 | Documentación operativa: `DEPLOY.md` (pasos), `SECRETS.md` (lista y rotación), `INCIDENT_RESPONSE.md` (runbooks). | should |
| R7 | Vercel: validar config `vercel.json`, alias `staging.awen.app` y `awen.app`, headers de seguridad. | should |
| R8 | Cache pip optimizado: `cache-dependency-path: requirements.txt` + `pip cache dir`. | could |

## 6. Criterios de aceptación

### R1
- **Dado** un PR hacia `develop`
- **Cuando** se intenta merge
- **Entonces** GitHub bloquea si: CI no pasa, 0 approvals, branch desactualizado, reviews desestimadas.

### R2
- **Dado** un PR hacia `develop`
- **Cuando** corre job `backend`
- **Entonces** levanta `postgres:16-alpine`, `pg_isready` pasa, tests corren contra esa BD.

### R3
- **Dado** backend corriendo
- **Cuando** `GET /health`
- **Entonces** `200 OK`, JSON `{"status":"ok","checks":{"db":true}}`, latency < 200ms.

### R4
- **Dado** push a `develop`
- **Cuando** CI pasa
- **Entonces** imagen Docker construida, deploy a Railway/Render staging, healthcheck pasa, URL accesible.

### R5
- **Dado** un secreto nuevo (ej. rotar `AWEN_SECRET_KEY`)
- **Cuando** se actualiza en GitHub Environment `staging`
- **Entonces** próximo deploy usa el nuevo valor sin cambiar código.

### R6
- **Dado** un incidente (ej. BD caída)
- **Cuando** se consulta `INCIDENT_RESPONSE.md`
- **Entonces** hay runbook con pasos: diagnóstico, mitigación, comunicación, post-mortem.

### R7
- **Dado** `vercel.json`
- **Cuando** push a `main`
- **Entonces** deploy a `awen.app` con headers `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`.

## 7. Contratos de API

### Endpoints nuevos

| Método | Ruta | Cambia | Notas |
|--------|------|--------|-------|
| GET | `/health` | nuevo | Liveness/readiness probe. Respuesta: `{"status":"ok","checks":{"db":true},"version":"x.y.z"}`. |

### Esquema de salida `/health`

```json
{
  "status": "ok",
  "checks": {
    "db": true
  },
  "version": "0.1.0",
  "timestamp": "2026-10-30T15:00:00Z"
}
```

## 8. Casos de borde

- Healthcheck DB timeout > 5s → `{"status":"degraded","checks":{"db":false}}` + 503.
- Deploy falla healthcheck 3 veces → rollback automático a imagen anterior.
- Secret rotado pero deploy en curso → deploy usa secreto anterior, próximo usa nuevo.
- PR de dependabot → CI corre, si pasa auto-merge opcional.

## 9. Impacto en datos y migraciones

- **Migración Alembic**: No (salvo que healthcheck requiera tabla `health_check` — no necesario).
- **Reversible**: N/A.
- **Objetos "Awen"**: No se tocan.

## 10. Tests a crear

| Test | Requisito | Tipo |
|------|-----------|------|
| `test_healthcheck_ok` | R3 | integración |
| `test_healthcheck_db_down` | R3 | integración (mock DB fail) |
| `test_branch_protection_enforced` | R1 | manual (no automatizable en CI) |
| `test_docker_build` | R4 | integración (CI) |

## 11. Riesgos

- **PostgreSQL en CI**: Añade ~20s al job backend. Mitigar: cache layers Docker, paralelizar jobs.
- **Deploy backend**: Railway/Render/Fly.io tienen límites gratis. Evaluar costos antes de elegir.
- **Secrets rotation**: Coordinar con equipo para no romper deploys en curso.
- **Branch protection**: Bloquea merges de emergencia si CI falla. Tener plan de override (admin bypass).

## 12. Preguntas abiertas

- [ ] **Backend deploy target**: Railway vs Render vs Fly.io vs AWS ECS? (Recomendado: Railway por simplicidad + PostgreSQL managed).
- [ ] **Staging environment**: ¿URL fija `staging.awen.app` o preview por PR? (Recomendado: preview por PR en Vercel, URL fija en Railway).
- [ ] **Secrets rotation frequency**: ¿Cada 90 días? ¿Automatizar con script?
- [ ] **Healthcheck DB**: ¿Consulta simple `SELECT 1` o query real? (Recomendado: `SELECT 1`).
- [ ] **Rollback strategy**: ¿Mantener 2 últimas imágenes Docker? ¿Tag `latest` vs `sha`?
- [ ] **Token GitHub workflow scope**: Se necesita para actualizar `.github/workflows/ci.yml` con PostgreSQL. ¿Crear PAT clásico o fine-grained?

## 13. Plan de verificación manual

1. Configurar token GitHub con `workflow` scope → actualizar `ci.yml` con PostgreSQL → push PR → CI verde.
2. Habilitar branch protection en `develop` via GitHub UI → probar merge sin CI → bloqueado.
3. Crear `Dockerfile` backend → build local → `docker run` → `curl localhost:8000/health` → OK.
4. Configurar Railway project → conectar repo → `RAILWAY_ENVIRONMENT=staging` → deploy automático en push a `develop`.
5. Configurar GitHub Environments `development`/`staging`/`production` → secrets → deploy funciona.
6. Verificar `GET /health` en staging → 200 OK, JSON correcto, latency < 200ms.
6. Documentar todo en `docs/ops/DEPLOY.md`, `SECRETS.md`, `INCIDENT_RESPONSE.md`.