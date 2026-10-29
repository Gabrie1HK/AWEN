---
name: Spec-Driven Workflow
description: Protocolo SDD de AWEN. Úsalo antes de modificar cualquier código para escribir la spec de la fase, crear los tests RED, implementar GREEN, verificar y cerrar la fase.
---

# PROTOCOLO SPEC-DRIVEN DEVELOPMENT (SDD) — AWEN

Antes de iniciar cualquier modificación en el proyecto AWEN, sigue este flujo secuencial.
No te saltes pasos y no empieces por el código.

## 0. FASE ACTIVA

- Lee `docs/sdd/roadmap.md` y localiza la fase en estado `aprobada`.
- Si no hay fase aprobada, detente: hay que escribir y aprobar una spec primero.
- Confirma la rama: `feat/fase-N-nombre` o `fix/fase-N-nombre`, creada desde `develop`.

## 1. ESPECIFICACIÓN

- Crea o actualiza `docs/specs/fase-N-nombre.md` usando `docs/sdd/plantillas/spec.md`.
- Incluye obligatoriamente:
  * Contexto y problema.
  * Alcance y no-goals.
  * Comportamiento actual vs. comportamiento deseado.
  * Requisitos numerados (`R1`, `R2`, ...) con prioridad.
  * Criterios de aceptación en Given/When/Then.
  * Contratos de entrada y salida (endpoints, DTOs, errores exactos sin tildes).
  * Casos de borde.
  * Lista de tests a crear, cada uno ligado a un requisito.
  * Preguntas abiertas.
- Si hay preguntas abiertas, **pregunta al usuario**. No las resuelvas por tu cuenta.

## 2. PLAN (solo si la fase lo necesita)

- Para fases con varios archivos o cambios de contrato, crea `docs/specs/fase-N-nombre.plan.md`
  con `docs/sdd/plantillas/plan.md`.
- El plan no puede añadir requisitos que no estén en la spec.

## 3. TAREAS

- Desglosa en `docs/specs/fase-N-nombre.tasks.md` con `docs/sdd/plantillas/tasks.md`.
- Cada tarea debe caber en un commit y citar su requisito.

## 4. VERIFICACIÓN PREVIA (RED)

- Escribe las pruebas unitarias/integración de la spec.
- Ejecútalas y confirma que **fallan por la razón correcta** antes de tocar la implementación.
- Cada test cita el requisito que cubre (`# R3`).

## 5. IMPLEMENTACIÓN MÍNIMA (GREEN)

- Modifica únicamente los archivos estrictamente necesarios en `back-end` o `front-end`.
- Respeta las capas `api/routes -> services -> repositories`.
- No refactorices nada fuera del alcance: anótalo en `NOTAS.md`.

## 6. AUDITORÍA

- Ejecuta `./scripts/verify.ps1` (Windows) o `./scripts/verify.sh` (Linux/macOS).
- Backend: `pytest` en verde. Frontend: `lint`, `test` y `build` en verde.
- Si cambió el contrato, actualiza `api.js` y sus tests en el mismo PR.

## 7. CIERRE DE FASE

- Marca la spec como `cerrada` y resuelve todas las preguntas abiertas.
- Actualiza `docs/sdd/roadmap.md`.
- Abre el PR hacia `develop` con la plantilla del repo.
- Al mergear, informa: qué cambió, cómo verificarlo y qué quedó pendiente.

## REGLA DE PARADA

Si en cualquier paso encuentras una ambigüedad de producto, un contrato roto no previsto o una
restricción que afecte datos, **detente y pregunta**. Nunca adivines.
