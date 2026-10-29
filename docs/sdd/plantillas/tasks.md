---
fase: N
spec: ../specs/fase-N-nombre.md
plan: ./fase-N-nombre.plan.md
---

# Tareas — Fase N

Checklist ejecutable. Cada tarea debe caber en un commit y citar su requisito.

## Preparación

- [ ] Rama creada desde `develop`: `feat/fase-N-nombre`
- [ ] Línea base de tests ejecutada y anotada
- [ ] Spec aprobada (sin preguntas abiertas)

## Tests RED

- [ ] `test_...` para R1
- [ ] `test_...` para R2
- [ ] Confirmado que fallan por la razón correcta

## Implementación GREEN

- [ ] R1 — ...
- [ ] R2 — ...
- [ ] Actualizar `api.js` si cambió el contrato
- [ ] Actualizar tests de frontend

## Verificación

- [ ] `./scripts/verify.ps1` en verde
- [ ] CI en verde
- [ ] Revisión manual según la spec

## Cierre

- [ ] Spec marcada como `cerrada`
- [ ] `docs/sdd/roadmap.md` actualizado
- [ ] `NOTAS.md` con hallazgos fuera de alcance
- [ ] PR mergeado en `develop`
