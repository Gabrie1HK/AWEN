# ADR 0001 — Repositorios duales SqlAlchemy / InMemory

- Fecha: 2026-10-29
- Estado: aceptado

## Contexto

El backend necesita persistencia real en PostgreSQL, pero los tests deben ser rápidos,
deterministas y no depender de una base de datos levantada.

## Decisión

Cada repositorio tiene dos implementaciones: `SqlAlchemy*Repository` para producción e
`InMemory*Repository` para tests. Los servicios dependen de la interfaz del repositorio, no de
la implementación. Los tests se construyen en `back-end/tests/conftest.py` con las versiones
InMemory.

## Consecuencias

### Positivas

- Tests sin PostgreSQL, rápidos y aislados.
- La lógica de negocio se prueba sin infraestructura.
- Fuerza una separación real entre rutas, servicios y persistencia.

### Negativas / costos

- Toda funcionalidad nueva de persistencia debe implementarse dos veces.
- Las dos implementaciones pueden divergir si no hay tests de contrato.
- Algunas consultas SQL complejas no se pueden replicar fielmente en memoria.

### Mitigación

- Mantener la lógica de consulta en el repositorio, no en el servicio.
- Añadir tests de contrato compartidos cuando una operación sea crítica.
