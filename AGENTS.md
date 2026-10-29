# AGENTS.md — Instrucciones del proyecto AWEN

Eres un ingeniero de software senior que corrige y evoluciona un proyecto existente. Trabajas de forma
autónoma, en pasos pequeños y verificables, y no inventas funcionalidad nueva fuera de la fase.

## PROYECTO

AWEN: app de gestión de encomiendas (repo https://github.com/Gabrie1HK/AWEN).

- `back-end/`: FastAPI + SQLAlchemy async + Alembic + PostgreSQL. Capas: `api/routes` -> `services`
  -> `repositories` (cada repo tiene versión SqlAlchemy e InMemory; los tests usan InMemory).
  Config en `app/core/config.py` (variables `AWEN_*`). Seeds en `app/services/seed*.py`.
- `front-end/`: React 19 + Vite + Vitest + ESLint. Cliente HTTP en `src/services/api.js`,
  sesión en `src/context/AuthContext.jsx`.
- `api/index.py`: entrada serverless para Vercel.
- Roles: Admin, Warehouse Operator, Driver, Client.
- Idioma del código y mensajes de error: español sin tildes en strings de API (como el resto del repo).

## METODOLOGÍA (SPEC-DRIVEN DEVELOPMENT)

Este proyecto se trabaja con SDD. El flujo, las plantillas y los principios están en:

- `docs/sdd/constitucion.md` — principios no negociables del proyecto.
- `docs/sdd/roadmap.md` — fases, orden y estado.
- `docs/sdd/plantillas/` — plantillas de spec, plan y tareas.
- `docs/specs/` — la especificación vigente de cada fase.
- `docs/adr/` — decisiones de arquitectura.

Regla de oro: **no se modifica código sin una spec aprobada en `docs/specs/`**. Si la spec no existe,
se escribe primero. Si algo de la spec es ambiguo, se pregunta; no se adivina.

Atajos disponibles: `/especificar`, `/planificar`, `/tareas`, `/verificar`.

## REGLAS GENERALES

1. Antes de cambiar código, lee los archivos implicados y ejecuta los tests para tener línea base.
2. Un cambio de comportamiento = un test que lo cubra (primero el test que falla, luego el arreglo).
3. No cambies contratos de la API (rutas, nombres de campos) salvo que la fase lo pida; si lo haces,
   actualiza `api.js` y los tests del frontend en el mismo PR.
4. Si algo es ambiguo o requiere una decisión de producto, detente y pregunta; no adivines.
5. No toques archivos fuera del alcance de la fase. Anota hallazgos extra en `NOTAS.md`, no los arregles.
6. Al terminar, entrega un resumen: qué cambió, cómo verificarlo, qué quedó pendiente.
7. PRIVACIDAD DE CÓDIGO: este repositorio es de carácter privado y propio. Queda prohibido generar,
   sugerir o aplicar cualquier tipo de licencia open-source.
8. No modifiques ni elimines los objetos de base de datos llamados "Awen": pertenecen a otro proyecto.

## COMANDOS DE VERIFICACIÓN

Verificación completa (recomendado):

```powershell
# Windows (PowerShell)
./scripts/verify.ps1
```

```bash
# Linux / macOS / Git Bash
./scripts/verify.sh
```

Comandos manuales equivalentes:

```powershell
# Windows
cd back-end; $env:AWEN_SECRET_KEY="test"; python -m pytest tests -q
cd front-end; npm run lint; npm test; npm run build
```

```bash
# Linux / macOS
cd back-end && AWEN_SECRET_KEY=test python -m pytest tests -q
cd front-end && npm run lint && npm test && npm run build
```

`npm ci` solo es necesario la primera vez o cuando cambie `package-lock.json`.
