---
fase: N
spec: ../specs/fase-N-nombre.md
---

# Plan técnico — Fase N

El plan responde **cómo** se cumple la spec. No añade requisitos nuevos.

## 1. Resumen de la solución

Dos o tres frases.

## 2. Archivos afectados

| Archivo | Cambio | Motivo |
| --- | --- | --- |
| `back-end/app/...` | nuevo / modificar | ... |
| `front-end/src/...` | nuevo / modificar | ... |

## 3. Diseño por capas (backend)

- **Routes**: ...
- **Services**: ...
- **Repositories** (SqlAlchemy + InMemory): ...
- **Schemas**: ...

## 4. Diseño de frontend

- **`src/services/api.js`**: ...
- **Componentes**: ...
- **`AuthContext`**: ...

## 5. Orden de implementación

1. Tests RED de R1.
2. Implementación mínima de R1.
3. Tests RED de R2...
4. ...

## 6. Migraciones

- Revisión / creación: ...
- Downgrade probado: sí / no

## 7. Alternativas descartadas

- ...

## 8. Riesgos técnicos

- ...

## 9. Estimación

| Requisito | Esfuerzo |
| --- | --- |
| R1 | S / M / L |
