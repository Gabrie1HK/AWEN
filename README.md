# AWEN

Aplicación de gestión de encomiendas. Backend FastAPI + PostgreSQL, frontend React + Vite.

Este proyecto se trabaja con **Spec-Driven Development (SDD)**: ningún cambio de comportamiento
se implementa sin una especificación aprobada.

## Empezar

1. Lee `docs/sdd/constitucion.md` (principios) y `docs/sdd/roadmap.md` (fases).
2. Elige la fase en estado `aprobada`.
3. Crea la rama desde `develop`:
   ```bash
   git switch develop
   git switch -c feat/fase-N-nombre
   ```
4. Usa los atajos de OpenCode: `/especificar`, `/planificar`, `/tareas`, `/verificar`.

## Estructura

| Ruta | Contenido |
| --- | --- |
| `back-end/` | FastAPI, SQLAlchemy, Alembic, tests con repos InMemory |
| `front-end/` | React 19, Vite, Vitest, ESLint |
| `api/index.py` | Entrada serverless para Vercel |
| `docs/sdd/` | Constitución, roadmap y plantillas |
| `docs/specs/` | Especificación de cada fase |
| `docs/adr/` | Decisiones de arquitectura |
| `.opencode/` | Skills y comandos del agente |
| `NOTAS.md` | Hallazgos fuera de alcance |

## Entorno de desarrollo

Requisitos: Python 3.12+, Node 22+ y PostgreSQL (solo para ejecutar la app, no para tests).

```powershell
# Backend
cd back-end
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r ..\requirements.txt
$env:AWEN_SECRET_KEY = "dev"
python -m uvicorn app.main:app --reload --port 8000
```

```powershell
# Frontend
cd front-end
npm ci
npm run dev
```

## Verificación

```powershell
./scripts/verify.ps1      # Windows
```

```bash
bash scripts/verify.sh    # Linux / macOS / Git Bash
```

Ejecuta pytest, ESLint, Vitest y el build de Vite. Es el mismo chequeo que corre CI.
