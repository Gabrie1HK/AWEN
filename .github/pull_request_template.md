## Qué cambia

<!-- Resumen en 2-3 líneas. -->

## Fase y requisitos

- Fase: `fase-N-nombre`
- Spec: `docs/specs/fase-N-nombre.md`
- Requisitos cubiertos: `R1`, `R2`

## Tipo de cambio

- [ ] `feat` — nueva funcionalidad
- [ ] `fix` — corrección de bug
- [ ] `refactor` — sin cambio de comportamiento
- [ ] `docs` / `test` / `ci` / `chore`

## Cómo verificarlo

<!-- Pasos concretos para una persona. -->

1.
2.

## Checklist SDD

- [ ] La spec existe, está `aprobada` y sin preguntas abiertas.
- [ ] Escribí los tests antes de la implementación y los vi fallar.
- [ ] Cada requisito cubierto tiene al menos un test.
- [ ] `scripts/verify.ps1` / `verify.sh` en verde.
- [ ] Si cambió el contrato de API, actualicé `api.js` y sus tests.
- [ ] No hay `console.log` ni código muerto.
- [ ] No toqué archivos fuera del alcance de la fase.
- [ ] Anoté hallazgos extra en `NOTAS.md`.

## Cambios rompientes

- [ ] No
- [ ] Sí — descrito abajo con `BREAKING CHANGE`

## Pendiente / fuera de alcance

<!-- Qué queda para otra fase. -->
