# AWEN

Aplicación de gestión de encomiendas. Backend FastAPI + PostgreSQL, frontend React + Vite.

## 🚀 Quick Start Local (Recomendado: Docker Compose)

```bash
# 1. Clonar
git clone https://github.com/Gabrie1HK/AWEN.git
cd AWEN

# 2. Configurar variables de entorno
cp back-end/.env.example back-end/.env

# 3. Levantar todo (PostgreSQL + Backend + Frontend)
docker compose up -d --build

# 4. Verificar
curl http://localhost:8000/health
# {"status":"ok","checks":{"db":true},"version":"0.1.0",...}

# Acceder:
# Frontend:  http://localhost:5173
# Backend:   http://localhost:8000
# API Docs:  http://localhost:8000/docs
```

### Opción B: Desarrollo Híbrido (Docker solo para PostgreSQL)

```bash
# 1. Solo PostgreSQL en Docker
docker run -d --name awen-postgres \
  -e POSTGRES_USER=awen -e POSTGRES_PASSWORD=awen -e POSTGRES_DB=awen \
  -p 5432:5432 -v postgres_data:/var/lib/postgresql/data \
  postgres:16-alpine

# 2. Backend (terminal 1)
cd back-end
cp .env.example .env
python -m venv .venv && source .venv/bin/activate  # Win: .venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000

# 3. Frontend (terminal 2)
cd front-end
npm ci
npm run dev
```

---

## 📁 Estructura del Proyecto

| Ruta | Contenido |
|------|-----------|
| `back-end/` | FastAPI, SQLAlchemy, Alembic, tests con repos InMemory |
| `front-end/` | React 19, Vite, Vitest, ESLint |
| `api/index.py` | Entrada serverless para Vercel |
| `docs/sdd/` | Constitución, roadmap y plantillas |
| `docs/specs/` | Especificación de cada fase |
| `docs/adr/` | Decisiones de arquitectura |
| `docs/ops/` | Guías operativas (DEPLOY, SECRETS, INCIDENT_RESPONSE) |
| `.opencode/` | Skills y comandos del agente |
| `NOTAS.md` | Hallazgos fuera de alcance |
| `docker-compose.yml` | Orquesta PostgreSQL + Backend + Frontend |
| `docker-compose.yml` | Orquesta PostgreSQL + Backend + Frontend |

---

## 🧪 Verificación

```powershell
./scripts/verify.ps1      # Windows
```

```bash
bash scripts/verify.sh    # Linux / macOS / Git Bash
```

Ejecuta pytest, ESLint, Vitest y el build de Vite. Es el mismo chequeo que corre CI.

---

## 📚 Documentación de Desarrollo

- **Constitución**: `docs/sdd/constitucion.md` (principios innegociables)
- **Roadmap**: `docs/sdd/roadmap.md` (fases y estado)
- **Specs**: `docs/specs/` (especificación de cada fase)
- **ADR**: `docs/adr/` (decisiones de arquitectura)
- **Guías Operativas**: `docs/ops/` (DEPLOY.md, SECRETS.md, INCIDENT_RESPONSE.md)
- **Notas**: `NOTAS.md` (hallazgos fuera de alcance)

---

## 🔧 Comandos Útiles

```bash
# Ver logs
docker compose logs -f backend
docker compose logs -f frontend

# Resetear BD completamente
docker compose down -v && docker compose up -d --build

# Tests locales
cd back-end && AWEN_SECRET_KEY=test python -m pytest tests -q
cd front-end && npm test

# Reset total (incluye volúmenes)
docker compose down -v && docker system prune -f
```

---

## 📝 Nota sobre Despliegue

Este proyecto está configurado para **funcionar completamente en local** con `docker compose up`. 

El despliegue a producción (Vercel + Railway/VPS) está documentado en `docs/ops/DEPLOY.md` y requiere configuración manual de:
- GitHub Environments + Secrets
- Vercel (Frontend)
- Railway/VPS propio (Backend + PostgreSQL)
- Branch Protection en `develop`

Ver `docs/ops/DEPLOY.md` para la guía completa.