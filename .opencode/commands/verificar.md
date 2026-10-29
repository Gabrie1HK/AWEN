---
description: Ejecuta la auditoría completa del proyecto
---

Ejecuta la verificación completa del proyecto y reporta el resultado.

1. En Windows ejecuta `./scripts/verify.ps1`. En Linux/macOS ejecuta `./scripts/verify.sh`.
2. Si el script no existe o falla por entorno, ejecuta manualmente:
   - `cd back-end` con `AWEN_SECRET_KEY=test` y `python -m pytest tests -q`
   - `cd front-end` y `npm run lint`, `npm test`, `npm run build`
3. No corrijas nada todavía. Primero reporta:
   - comando ejecutado,
   - resultado (verde/rojo),
   - tests que fallan y por qué,
   - si el fallo es del cambio actual o preexistente.
4. Si hay fallos, propone el siguiente paso mínimo y espera confirmación si el arreglo sale del
   alcance de la fase.
