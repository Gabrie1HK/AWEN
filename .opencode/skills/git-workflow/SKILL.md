---
name: Flujo Git AWEN
description: Reglas de ramas, commits y Pull Requests de AWEN basadas en Conventional Commits. Úsalo al crear ramas, escribir mensajes de commit, preparar un PR o resolver dudas de integración.
---

# ESPECIFICACIÓN Y REGLAS DE FLUJO DE TRABAJO CON GIT (AWEN)

Este documento define la especificación formal del flujo de ramas, integración continua y la
convención estricta de commits para el proyecto AWEN, basada en la especificación oficial
[Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).

---

## 1. ARQUITECTURA DE RAMAS

El repositorio maneja dos ramas principales permanentes y ramas temporales de trabajo.

### Ramas principales (permanentes)

- `main`: rama de producción y código estable.
  - NUNCA se realiza commit ni push directo sobre `main`.
  - Solo recibe fusiones desde `develop` cuando una versión/fase se considera estable.
- `develop`: rama principal de integración y desarrollo.
  - Base de pruebas de estabilidad antes de enviar cambios a `main`.
  - NUNCA se hace commit ni push directo a `develop`.
  - Todos los cambios entran a `develop` mediante Pull Requests aprobados desde ramas temporales.

### Ramas temporales (trabajo específico)

Se crean a partir de `develop` (si `develop` no existe, se crea a partir de `main`).

Nomenclatura obligatoria:

- `feat/fase-N-nombre-funcionalidad`
- `fix/fase-N-descripcion-error`
- `refactor/nombre-modulo`
- `docs/descripcion`
- `test/descripcion`

---

## 2. ESTRUCTURA FORMAL DE COMMIT (CONVENTIONAL COMMITS v1.0.0)

```text
<tipo>[alcance opcional][!]: <descripcion en minusculas y en espanol>

[cuerpo opcional]

[pie(s) de pagina opcional(es)]
```

---

## 3. ESPECIFICACIÓN DE TIPOS Y ELEMENTOS

### Tipos principales (estándar v1.0.0)

- `fix`: corrige un bug o error en el código (PATCH en SemVer).
- `feat`: introduce una nueva funcionalidad (MINOR en SemVer).

### Tipos adicionales (convención Angular)

- `build`: cambios en el sistema de compilación o dependencias (npm, pip).
- `ci`: cambios en archivos y scripts de CI/CD.
- `docs`: cambios exclusivamente en documentación.
- `perf`: mejora de rendimiento.
- `refactor`: cambio que no corrige un bug ni agrega funcionalidad.
- `style`: cambios que no afectan el significado del código (espacios, formato, punto y coma).
- `test`: añadir pruebas faltantes o corregir pruebas existentes.
- `chore`: tareas rutinarias que no tocan código de producción ni tests.

---

## 4. REGLAS DE SINTAXIS Y CAMBIOS ROMPIENTES

1. **Encabezado:**
   - El `<tipo>` y la `<descripcion>` son obligatorios.
   - El `<alcance>` es opcional, entre paréntesis inmediato al tipo, indicando la sección
     afectada (ej. `auth`, `routes`, `ui`, `services`).
   - La `<descripcion>` debe ser breve, en minúsculas y en español, sin tildes.

2. **Cambios rompientes (BREAKING CHANGE):**
   - Un cambio que rompe compatibilidad (MAJOR en SemVer) DEBE indicarse de dos formas:
     a) `!` inmediatamente antes de los dos puntos (ej. `feat(api)!: cambiar contrato de /pedidos`).
     b) `BREAKING CHANGE: <descripcion>` en la primera línea del pie de página.

3. **Cuerpo y pie de página:**
   - El cuerpo es opcional, separado del encabezado por una línea en blanco, y explica el motivo
     y el contraste con el comportamiento anterior.
   - El pie sigue el formato `<token>: <valor>` (ej. `Refs: #123`).

---

## 5. EJEMPLOS DE COMMITS VÁLIDOS

### Corrección simple

```bash
git commit -m "fix(auth): corregir tiempo de expiracion del token jwt"
```

### Funcionalidad con alcance

```bash
git commit -m "feat(parcels): agregar filtro por sucursal en el listado"
```

### Cambio rompiente

```bash
git commit -m "feat(api)!: unificar respuesta de errores de validacion" -m "BREAKING CHANGE: el campo detail ahora es un objeto con code y message."
```

### Documentación

```bash
git commit -m "docs(sdd): agregar plantilla de especificacion de fase"
```

---

## 6. PULL REQUESTS

- Título con el mismo formato que un commit.
- Un PR resuelve una fase (o una parte declarada de ella).
- Debe incluir: requisitos cubiertos (`R*`), cómo verificarlo y hallazgos fuera de alcance.
- No se mergea con CI en rojo ni con preguntas abiertas en la spec.
- El merge hacia `develop` es squash o merge commit; nunca rebase que reescriba historia compartida.
