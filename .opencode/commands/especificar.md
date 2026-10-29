---
description: Crea o actualiza la especificación SDD de una fase
---

Vas a escribir la especificación de la fase: $ARGUMENTS

Pasos obligatorios:

1. Lee `AGENTS.md`, `docs/sdd/constitucion.md`, `docs/sdd/roadmap.md` y
   `docs/sdd/plantillas/spec.md`.
2. Revisa el código real implicado. El "comportamiento actual" debe citar archivos y líneas
   concretas, no suposiciones.
3. Crea o actualiza `docs/specs/fase-N-nombre.md` con la plantilla. Incluye requisitos numerados
   (`R1`, `R2`, ...), criterios de aceptación Given/When/Then, contratos de API, errores exactos
   sin tildes, casos de borde y tests a crear.
4. No inventes requisitos de producto. Lo que no se pueda deducir del código o de la petición
   va en **Preguntas abiertas**.
5. Añade o actualiza la fila de la fase en `docs/sdd/roadmap.md` con estado `borrador`.
6. No modifiques código en este paso.

Al terminar, muestra al usuario: resumen de la spec, decisiones que tomaste y la lista de
preguntas abiertas que necesitan respuesta antes de aprobarla.
