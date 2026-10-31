---
fase: N
nombre: nombre-corto
estado: borrador
rama: feat/fase-N-nombre-corto
autor:
fecha: AAAA-MM-DD
---

# Fase N — Nombre de la fase

## 1. Contexto y problema

Qué duele hoy y por qué merece una fase. Sin soluciones todavía.

## 2. Alcance

### Dentro del alcance

- ...

### Fuera del alcance (no-goals)

- ...

## 3. Comportamiento actual

Qué hace el sistema hoy, con referencias a archivos y endpoints concretos.
Si no existe, decirlo: "no implementado".

## 4. Comportamiento deseado

Descripción funcional, sin entrar en detalles de implementación.

## 5. Requisitos

| ID | Requisito | Prioridad |
| --- | --- | --- |
| R1 | ... | must |
| R2 | ... | should |

Prioridades: `must`, `should`, `could`.

## 6. Criterios de aceptación

Para cada requisito, en formato Given/When/Then.

### R1

- **Dado** ...
- **Cuando** ...
- **Entonces** ...

### R2

- **Dado** ...
- **Cuando** ...
- **Entonces** ...

## 7. Contratos de API

### Endpoints afectados

| Método | Ruta | Cambia | Notas |
| --- | --- | --- | --- |
| GET | `/api/v1/...` | no | — |

### Esquemas de entrada

```json
{}
```

### Esquemas de salida

```json
{}
```

### Errores exactos

| Código | Mensaje (sin tildes) | Cuándo |
| --- | --- | --- |
| 400 | `...` | ... |

## 8. Casos de borde

- ...

## 9. Impacto en datos y migraciones

- ¿Requiere migración de Alembic? Sí / No
- ¿Es reversible? Sí / No
- ¿Toca objetos "Awen"? **No** (prohibido)

## 10. Tests a crear

| Test | Requisito | Tipo |
| --- | --- | --- |
| `test_...` | R1 | unitario / integración |

Backend: `back-end/tests/`. Frontend: `front-end/tests/`.

## 11. Riesgos

- ...

## 12. Preguntas abiertas

- [ ] ...

> Una spec con preguntas abiertas no se aprueba.

## 13. Plan de verificación manual

Pasos concretos para que una persona compruebe la fase.
