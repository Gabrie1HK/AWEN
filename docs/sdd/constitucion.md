# Constitución del proyecto AWEN

Principios no negociables. Cualquier spec, plan o PR que los contradiga debe justificarlo
explícitamente o rechazarse.

## 1. La especificación manda

- Ningún cambio de comportamiento se implementa sin una spec en `docs/specs/`.
- La spec describe **qué** y **por qué**; el plan describe **cómo**.
- Si el código y la spec discrepan, gana la spec o se corrige la spec. Nunca se "ajusta" el
  comportamiento en silencio.

## 2. Test primero (RED -> GREEN)

- Todo requisito de la spec tiene al menos un test que lo verifica.
- El test se escribe y se ve fallar antes de tocar la implementación.
- Un bug corregido sin test de regresión no está corregido.

## 3. Arquitectura por capas (backend)

- Flujo obligatorio: `api/routes` -> `services` -> `repositories`.
- Ninguna ruta accede a la base de datos directamente.
- Todo repositorio tiene implementación SqlAlchemy e InMemory. Los tests usan InMemory.
- Configuración solo por variables de entorno `AWEN_*` en `app/core/config.py`.

## 4. Contrato único (frontend)

- Toda llamada HTTP pasa por `src/services/api.js`. Prohibido `fetch`/`axios` en componentes.
- La sesión y los roles viven en `src/context/AuthContext.jsx`.
- Si cambia un endpoint o un campo, `api.js` y sus tests se actualizan en el mismo PR.

## 5. Convenciones de la API

- Rutas versionadas bajo `/api/v1`.
- Mensajes de error en español **sin tildes** en los payloads JSON.
- No se rompen contratos sin marcarlo como `BREAKING CHANGE` en el commit y en la spec.

## 6. Seguridad y datos

- Prohibido tocar, migrar o eliminar los objetos de base de datos llamados "Awen": son de otro proyecto.
- Secretos solo por entorno. Nunca en el repositorio ni en el código.
- Las migraciones de Alembic son reversibles y no destructivas por defecto.

## 7. Alcance controlado

- Un PR resuelve una fase (o una parte declarada de ella). Nada de refactors colaterales.
- Los hallazgos fuera de alcance se anotan en `NOTAS.md`.

## 8. Verificación obligatoria

Un cambio está terminado solo si pasan:

- Backend: `pytest` en verde.
- Frontend: `lint`, `test` y `build` en verde.
- CI en verde en el PR hacia `develop`.

## 9. Licencias

Este repositorio es privado y propio. No se añaden licencias open-source ni se relicencia el código.
