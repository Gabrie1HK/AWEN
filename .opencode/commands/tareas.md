---
description: Desglosa una fase en tareas ejecutables
---

Vas a desglosar en tareas la fase: $ARGUMENTS

Pasos obligatorios:

1. Lee la spec y, si existe, el plan de la fase.
2. Usa `docs/sdd/plantillas/tasks.md`.
3. Crea `docs/specs/fase-N-nombre.tasks.md`.
4. Cada tarea debe:
   - caber en un commit,
   - citar el requisito que cubre (`R*`),
   - indicar si es test RED o implementación GREEN.
5. Ordena las tareas: preparación, tests RED, implementación, verificación, cierre.

No modifiques código en este paso.
