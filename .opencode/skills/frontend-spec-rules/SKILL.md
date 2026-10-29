---
name: Reglas Frontend AWEN
description: Reglas técnicas del frontend React 19 + Vite de AWEN. Úsalo al modificar componentes, páginas, servicios HTTP, contexto de sesión, estilos o tests del front-end.
---

# ESPECIFICACIONES TÉCNICAS FRONTEND (React 19 + Vite)

- Centralización HTTP: toda comunicación de red y llamadas a la API deben realizarse
  exclusivamente a través de `src/services/api.js`. Prohibido el uso de `fetch` o `axios`
  directamente dentro de los componentes.
- Gestión de sesión y estado: la lógica de autenticación, almacenamiento del token y verificación
  de roles (Admin, Warehouse Operator, Driver, Client) está encapsulada en
  `src/context/AuthContext.jsx`. Todo componente que requiera conocer el usuario activo debe
  consumir este contexto.
- Reflejo de contratos: si una fase exige modificar una respuesta o endpoint del backend, es
  obligatorio actualizar el contrato paralelo en `api.js` dentro del mismo Pull Request.
- Pruebas de cliente: toda modificación de interfaz o estado requiere validación. Ejecuta Vitest
  (`front-end/tests/`) antes del build.
- Linter y build: el código debe pasar limpio por ESLint (`npm run lint`) y compilar sin errores
  en Vite (`npm run build`). No dejar `console.log` residuales en los commits.
- Accesibilidad básica: todo control interactivo debe ser accesible por teclado y tener nombre
  accesible.
