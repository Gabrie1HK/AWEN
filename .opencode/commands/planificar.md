---
description: Crea el plan técnico de una fase aprobada
---

Vas a crear el plan técnico de la fase: $ARGUMENTS

Pasos obligatorios:

1. Lee la spec de la fase en `docs/specs/` y `docs/sdd/plantillas/plan.md`.
2. Verifica que la spec esté en estado `aprobada` y sin preguntas abiertas. Si no, detente y
   avisa al usuario.
3. Identifica los archivos exactos que hay que tocar en `back-end/` y `front-end/`.
4. Diseña el cambio respetando las capas `api/routes -> services -> repositories` y las reglas
   de `api.js` / `AuthContext`.
5. Crea `docs/specs/fase-N-nombre.plan.md` con la plantilla.
6. El plan no puede añadir requisitos nuevos. Si detectas uno, vuelve a la spec.

No modifiques código en este paso.
