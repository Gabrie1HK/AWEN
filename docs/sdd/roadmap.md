# Roadmap de fases — AWEN

Este documento es la fuente de verdad del orden de trabajo. Una fase no empieza hasta que su
spec esté **aprobada**.

## Estados de una fase

| Estado | Significado |
| --- | --- |
| `borrador` | Spec escrita, pendiente de revisión y decisiones de producto. |
| `aprobada` | Spec revisada; se puede crear rama y escribir tests. |
| `en implementacion` | Rama activa, tests RED y luego GREEN. |
| `en revision` | PR abierto hacia `develop`; CI en verde. |
| `cerrada` | Mergeada en `develop`, spec actualizada y roadmap al día. |
| `bloqueada` | Depende de una decisión o de otra fase. |

## Fases

| Fase | Nombre | Estado | Spec | Rama |
| --- | --- | --- | --- | --- |
| 1 | Seguridad y autorización | `cerrada` | [fase-1-seguridad](../specs/fase-1-seguridad.md) | `fix/fase-1-seguridad` |
| 2 | Almacenamiento serverless | `aprobada` | [fase-2-storage-serverless](../specs/fase-2-storage.md) | `feat/fase-2-storage-serverless` |
| 3 | Por definir | — | — | — |

> Las fases 2 en adelante se añaden cuando exista una spec. No se planifican en el roadmap
> sin spec: el roadmap solo refleja trabajo real.

## Cómo se añade una fase

1. Copia `docs/sdd/plantillas/spec.md` a `docs/specs/fase-N-nombre.md`.
2. Rellena la spec. Marca lo ambiguo como **pregunta abierta**.
3. Revisa la spec con el usuario. Al aprobarla, cambia el estado a `aprobada`.
4. Añade la fila a la tabla de arriba.
5. Crea la rama desde `develop`: `feat/fase-N-nombre` o `fix/fase-N-nombre`.
6. Sigue el flujo: tests RED -> implementación GREEN -> `/verificar` -> PR.

## Definition of Done de una fase

- [ ] Spec en estado `cerrada` y sin preguntas abiertas.
- [ ] Todos los requisitos (`R*`) tienen test y pasan.
- [ ] `scripts/verify.ps1` / `verify.sh` en verde.
- [ ] CI en verde en el PR hacia `develop`.
- [ ] `api.js` actualizado si cambió el contrato.
- [ ] `NOTAS.md` con los hallazgos fuera de alcance.
- [ ] Roadmap actualizado.
- [ ] Sin `console.log` ni código muerto.

## Convención de numeración

- El número de fase es el mismo en la spec, la rama y el roadmap (`fase-N`).
- Los requisitos se numeran `R1`, `R2`, ... dentro de cada spec y no se renumeran al cerrar.
- Los tests citan el requisito que cubren: `# R3`.
