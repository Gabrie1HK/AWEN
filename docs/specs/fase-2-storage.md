---
fase: 2
nombre: storage-serverless
estado: aprobada
rama: feat/fase-2-storage-serverless
autor: Gabriel Espinoza
fecha: 2026-10-29
---

# Fase 2 — Almacenamiento serverless para uploads/POD

## 1. Contexto y problema

Hoy los archivos subidos (evidencias de encomiendas, comprobantes de entrega/POD, fotos de firma) se guardan en el **filesystem local** del servidor (`settings.upload_dir`, por defecto `./uploads`) y se sirven vía `StaticFiles` en `/uploads/*`.

**Problema**: En entornos serverless (Vercel, AWS Lambda, Cloudflare Workers) el filesystem es **ephemeral**:
- Solo `/tmp` es escribible (y no persiste entre invocaciones)
- Los archivos se pierden al reiniciar/escalar la función
- No hay acceso compartido entre instancias

**Riesgo**: Comprobantes de entrega (POD) y evidencias fotográficas se pierden en producción.

## 2. Alcance

### Dentro del alcance
- Reemplazar almacenamiento local por **Vercel Blob** (S3-compatible) como proveedor por defecto; compatible con cualquier proveedor S3-compatible (AWS S3, Cloudflare R2, MinIO, Azure Blob) via config
- Subida directa del cliente al bucket (pre-signed PUT URLs) para archivos <10MB; streaming por backend para archivos mayores
- Servir archivos via URLs firmadas (pre-signed GET, expiración 1h default) — bucket privado
- Mantener compatibilidad con respuesta actual: `{"filename": "...", "url": "...", "size": N}`
- Configuración por variables de entorno `AWEN_STORAGE_*` (proveedor, bucket, región, credenciales, TTL, límite tamaño, tipos permitidos)
- Tests de integración con mock S3 (moto) en CI; MinIO opcional en local

### Fuera del alcance (no-goals)
- Migración de archivos existentes en `./uploads` (se pueden dejar o migrar manualmente)
- CDN propio / configuración de CloudFront / Cloudflare Workers
- Procesamiento de imágenes (resize, thumbnail, optimización)
- Eliminación automática de archivos huérfanos
- Versionado de buckets / lifecycle policies

## 3. Comportamiento actual

| Endpoint | Qué hace hoy |
|----------|--------------|
| `POST /api/v1/parcels/upload-evidence` | Guarda en `./uploads/ev_{uuid}.ext`, retorna `/uploads/ev_...` |
| `POST /api/v1/deliveries/{id}/upload` | Guarda en `./uploads/{delivery_id}_{uuid}.ext`, actualiza `photoUrl` en BD, retorna `/uploads/...` |
| `GET /uploads/*` | Sirve archivos estáticos desde `./uploads` (StaticFiles) |

Config en `app/core/config.py`:
```python
upload_dir: str = "uploads"  # AWEN_UPLOAD_DIR
```

## 4. Comportamiento deseado

1. **Subida**: El cliente (frontend) obtiene una **pre-signed URL** del backend y sube **directamente al bucket** (evita pasar por el backend, ahorra ancho de banda y timeout).
   - Alternativa aceptable: Backend recibe archivo y hace streaming al bucket (si pre-signed URLs no viable por CORS/políticas).

2. **Respuesta**: Igual que hoy: `{"filename": "...", "url": "https://bucket.../...", "size": N}`. La URL es una **pre-signed URL de descarga** (expiración configurable, ej. 1 hora) o URL pública si bucket público.

3. **Descarga/visualización**: El frontend usa la URL firmada para mostrar imagen/PDF. No más `/uploads/*` local.

4. **Configuración**: Variables de entorno para proveedor, bucket, región, credenciales, expiración URLs.

## 5. Requisitos

| ID | Requisito | Prioridad |
|----|-----------|-----------|
| R1 | Subida de evidencias (parcels) usa object storage (S3/R2/MinIO) | must |
| R2 | Subida de POD/firmas (deliveries) usa object storage | must |
| R3 | Respuesta API mantiene contrato: `{filename, url, size}` | must |
| R4 | URLs de descarga son pre-signed (expiración configurable, default 1h) | must |
| R5 | Configuración por `AWEN_STORAGE_*` (provider, bucket, region, credentials, public_base_url) | must |
| R6 | Funciona en local con MinIO (docker-compose) y en CI con moto (mock) | should |
| R7 | No rompe contrato frontend (`api.js` actualizado si cambia) | must |

## 6. Criterios de aceptación

### R1 - Parcels upload evidence
- **Dado** un cliente autenticado con rol permitido
- **Cuando** llama `POST /api/v1/parcels/upload-evidence` con un archivo
- **Entonces** recibe `200` con `{filename, url, size}` donde `url` es pre-signed URL válida al bucket

### R2 - Deliveries upload POD
- **Dado** un cliente autenticado con rol permitido
- **Cuando** llama `POST /api/v1/deliveries/{id}/upload` con archivo
- **Entonces** recibe `200` con `{filename, url, size}` y `delivery.photoUrl` actualizado en BD con la URL firmada

### R3 - Contrato API
- **Dado** cualquier endpoint de upload existente
- **Cuando** se usa tras la migración
- **Entonces** el JSON de respuesta tiene exactamente los mismos campos (`filename`, `url`, `size`)

### R4 - URLs pre-signed
- **Dado** una URL retornada en `url`
- **Cuando** se accede dentro del TTL (default 1h)
- **Entonces** devuelve el archivo (200)
- **Cuando** se accede tras expirar TTL
- **Entonces** devuelve 403/404 (según proveedor)

### R5 - Configuración
- **Dado** variables `AWEN_STORAGE_PROVIDER=vercel-blob`, `AWEN_STORAGE_BUCKET=awen-uploads`, `AWEN_STORAGE_REGION=auto`, `AWEN_BLOB_READ_WRITE_TOKEN=vercel_blob_rw_token...`, `AWEN_STORAGE_PRESIGNED_TTL=3600`, `AWEN_UPLOAD_MAX_SIZE=10485760`, `AWEN_UPLOAD_ALLOWED_TYPES=image/jpeg,image/png,image/webp,application/pdf`
- **Cuando** arranca la app
- **Entonces** conecta a Vercel Blob y funciona sin código hardcodeado (compatibilidad S3 genérica permite otros proveedores)

### R6 - Local/CI
- **Dado** CI sin MinIO
- **Cuando** corren tests
- **Entonces** usan `moto` (mock S3) y pasan
- **Opcional**: `docker-compose.yml` con MinIO para desarrollo local (`AWEN_STORAGE_PROVIDER=s3` + endpoint local)

## 7. Contratos de API

### Endpoints afectados

| Método | Ruta | Cambia | Notas |
|--------|------|--------|-------|
| POST | `/api/v1/parcels/upload-evidence` | **sí** (interno) | Respuesta igual, URL distinta |
| POST | `/api/v1/deliveries/{id}/upload` | **sí** (interno) | Respuesta igual, URL distinta, actualiza BD |
| GET | `/uploads/*` | **elimina** | Ya no se usa; archivos via pre-signed URLs |

### Esquema de entrada (sin cambios)
```json
// multipart/form-data con campo "file"
```

### Esquema de salida (sin cambios)
```json
{
  "filename": "ev_a1b2c3d4.jpg",
  "url": "https://bucket.s3.region.amazonaws.com/key?X-Amz-Signature=...",
  "size": 102400
}
```

### Errores exactos
| Código | Mensaje (sin tildes) | Cuándo |
|--------|----------------------|--------|
| 400 | `Archivo invalido` | File vacío o tipo no permitido |
| 413 | `Archivo demasiado grande` | Excede límite configurado |
| 500 | `Error al subir archivo` | Falla proveedor storage |
| 403 | `No tiene permisos para esta operacion` | Sin rol (existente) |

## 8. Casos de borde

- Archivo vacío (0 bytes)
- Nombre de archivo con caracteres especiales / unicode
- Archivo > límite configurado (ej. 10MB)
- Proveedor storage caído / credenciales inválidas
- Bucket no existe / permisos insuficientes
- Pre-signed URL expirada al intentar descargar
- Mismo archivo subido dos veces (colisión de keys - usar UUID)
- Subida simultánea de mismo archivo (idempotencia no requerida)

## 9. Impacto en datos y migraciones

- **Migración Alembic**: No requerida (no cambia esquema BD, solo `photoUrl` guarda URL distinta)
- **Reversible**: Sí (cambiar config a local vuelve a funcionar si se mantiene `./uploads`)
- **Objetos "Awen"**: **No** se tocan

## 10. Tests a crear

| Test | Requisito | Tipo |
|------|-----------|------|
| `test_upload_evidence_returns_presigned_url` | R1 | integración |
| `test_upload_pod_updates_delivery_photo_url` | R2 | integración |
| `test_response_contract_unchanged` | R3 | integración |
| `test_presigned_url_expires` | R4 | integración |
| `test_storage_config_from_env` | R5 | unitario |
| `test_upload_works_with_moto_mock` | R6 | integración (CI) |

## 11. Riesgos

- **CORS en pre-signed URLs**: El bucket debe permitir `PUT` desde origen frontend (configurar CORS en bucket)
- **Latencia**: Pre-signed URLs añaden round-trip; mitigable con CDN
- **Coste**: Object storage tiene coste por request/almacenamiento; estimar según volumen
- **Migración archivos existentes**: Los archivos en `./uploads` quedarán inaccesibles si no se migran manualmente
- **Seguridad**: URLs pre-firmadas exponen acceso temporal; TTL corto (1h) mitiga riesgo

## 12. Preguntas abiertas (RESUELTAS ✅)

- [x] **Proveedor por defecto**: **Vercel Blob** (S3-compatible, nativo en Vercel, sin egress fees)
- [x] **Subida directa (pre-signed PUT) vs streaming por backend**: **Pre-signed PUT** para <10MB (cliente → bucket directo); streaming por backend para >10MB
- [x] **Bucket público vs privado con pre-signed GET**: **Privado + pre-signed GET** (expiración 1h default, configurable `AWEN_STORAGE_PRESIGNED_TTL`)
- [x] **Estructura de keys en bucket**: `evidence/{type}/{uuid}.ext` (type = `parcels` | `deliveries`)
- [x] **Límite de tamaño archivo**: **10MB** default (`AWEN_UPLOAD_MAX_SIZE=10485760`)
- [x] **Tipos de archivo permitidos**: **Imágenes (jpeg, png, webp) + PDF** (`AWEN_UPLOAD_ALLOWED_TYPES=image/jpeg,image/png,image/webp,application/pdf`)

## 13. Plan de verificación manual

1. **Producción (Vercel)**: Configurar `AWEN_BLOB_READ_WRITE_TOKEN` en Vercel Project Settings → Deploy → probar upload
2. **Local (opcional MinIO)**: 
   - `docker-compose up -d minio` (si se quiere probar local con S3)
   - Configurar `.env` con `AWEN_STORAGE_PROVIDER=s3` + endpoint MinIO
3. **Arrancar backend**: `AWEN_STORAGE_PROVIDER=vercel-blob AWEN_BLOB_READ_WRITE_TOKEN=... python -m uvicorn app.main:app`
4. Login frontend → subir evidencia en Parcels → ver respuesta con URL `https://<blob>.vercel-storage.com/...`
5. Abrir URL en navegador → imagen se ve (dentro de TTL)
6. Subir POD en Delivery → ver `photoUrl` actualizado en BD con URL firmada
7. Esperar TTL (reducir a 60s para test via `AWEN_STORAGE_PRESIGNED_TTL=60`) → URL expira → 403
8. Correr tests: `pytest tests/ -k "upload"` → verdes (usan `moto` mock)