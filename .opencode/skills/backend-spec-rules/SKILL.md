---
name: Reglas Backend AWEN
description: Reglas técnicas del backend FastAPI + SQLAlchemy de AWEN. Úsalo al escribir o modificar rutas, servicios, repositorios, schemas, configuración o migraciones del back-end.
---

# ESPECIFICACIONES TÉCNICAS BACKEND (FastAPI + SQLAlchemy)

- Capas obligatorias: `api/routes` -> `services` -> `repositories`. Ninguna ruta accede a la base
  de datos directamente.
- Todos los repositorios deben incluir implementación SqlAlchemy e InMemory.
- Pruebas unitarias: deben ejecutarse utilizando la versión InMemory (`back-end/tests/conftest.py`).
- Manejo de configuración: exclusivamente mediante variables de entorno `AWEN_*` en
  `app/core/config.py`.
- Formato de errores: cadenas de texto sin tildes en los payloads JSON de la API.
- Rutas versionadas bajo `/api/v1`.
- Migraciones Alembic: reversibles, no destructivas por defecto y con `downgrade` probado.
- RESTRICCIÓN ESTRICTA DE INFRAESTRUCTURA: existen dos objetos en la base de datos nombrados
  "Awen". Pertenecen a un proyecto aparte. Queda absolutamente prohibido tocarlos, modificarlos,
  alterarlos o eliminarlos mediante migraciones de Alembic o scripts administrativos.
- No añadas dependencias nuevas sin justificarlo en la spec o el plan.
