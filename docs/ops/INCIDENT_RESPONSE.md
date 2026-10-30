# Plan de Respuesta a Incidentes — AWEN

## Clasificación de Severidad

| Nivel | Nombre | Definición | SLA Respuesta | SLA Resolución |
|-------|--------|------------|---------------|----------------|
| **SEV-1** | Crítico | Servicio caído, pérdida datos, brecha seguridad | 15 min | 1 hora |
| **SEV-2** | Alto | Funcionalidad crítica degradada, performance severa | 30 min | 4 horas |
| **SEV-3** | Medio | Funcionalidad no crítica afectada, workaround existe | 2 horas | 24 horas |
| **SEV-4** | Bajo | Bug cosmético, mejora, documentación | Next sprint | Next release |

---

## Proceso de Respuesta

### 1. Detección y Reporte

**Canales**:
- Alertas automáticas (healthcheck, CI failures)
- Reporte usuario (GitHub Issues, email)
- Monitoreo manual (logs, métricas)

**Plantilla Reporte**:
```
**Severidad**: SEV-[1-4]
**Título**: [Breve descripción]
**Servicio afectado**: [Backend/Frontend/DB/Infra]
**Síntomas**: [Qué falla, logs, errores]
**Impacto usuarios**: [Cuántos, qué funcionalidad]
**Pasos reproducir**: [Si conocido]
**Workaround**: [Si existe]
**Reportado por**: @usuario / sistema
**Timestamp**: YYYY-MM-DDTHH:MM:SSZ
```

### 2. Triage (Primeros 15 min)

| Acción | Responsable | Tiempo |
|--------|-------------|--------|
| Confirmar severidad | On-call / Tech Lead | 5 min |
| Asignar Incident Commander | Tech Lead | 5 min |
| Comunicar a stakeholders | Incident Commander | 5 min |
| Crear issue GitHub `incident/YYYY-MM-DD-descripcion` | Incident Commander | 5 min |

### 3. Diagnóstico (Paralelo a mitigación)

| Paso | Acción | Herramientas |
|------|--------|--------------|
| 1 | Verificar healthchecks (`/health`) | `curl /health` |
| 2 | Revisar logs recientes | Railway logs, Vercel logs, GitHub Actions |
| 3 | Verificar métricas clave | Latency, error rate, throughput |
| 4 | Revisar cambios recientes | GitHub commits, deploys recientes |
| 5 | Reproducir en staging | Reproducir issue reportado |
| 6 | Identificar root cause | Análisis logs, diffs, métricas |

### 4. Mitigación (Contención)

| Severidad | Acciones Inmediatas |
|-----------|---------------------|
| **SEV-1** | Rollback deploy anterior, activar maintenance mode, notificar usuarios |
| **SEV-2** | Rollback si deploy reciente, activar feature flags, escalar recursos |
| **SEV-3** | Workaround documentado, programar fix en sprint actual |
| **SEV-4** | Documentar, programar en backlog |

**Rollback Rápido**:
```bash
# Backend (Railway)
railway rollback  # O dashboard: Deployments → Previous → Redeploy

# Frontend (Vercel)
vercel rollback [deployment-url]  # O dashboard: Promote previous
```

### 5. Resolución

1. **Fix definitivo**: Commit fix → CI → Deploy
2. **Verificación**: Healthchecks OK, smoke tests pasan
3. **Cierre**: Actualizar issue GitHub con root cause y fix
4. **Comunicar**: Notificar stakeholders "Resuelto"

### 5. Post-Mortem (SEV-1 y SEV-2 obligatorio)

**Plantilla Post-Mortem** (en `docs/ops/postmortems/YYYY-MM-DD-descripcion.md`):

```markdown
# Post-Mortem: [Título incidente]

**Fecha**: YYYY-MM-DD
**Severidad**: SEV-[1-2]
**Duración**: X horas Y minutos
**Incident Commander**: @usuario

## Resumen
[Qué pasó en 2-3 líneas]

## Timeline
| Timestamp | Evento |
|-----------|--------|
| YYYY-MM-DDTHH:MM:SSZ | Inicio incidente |
| YYYY-MM-DDTHH:MM:SSZ | Detección |
| YYYY-MM-DDTHH:MM:SSZ | Mitigación iniciada |
| YYYY-MM-DDTHH:MM:SSZ | Fix deployado |
| YYYY-MM-DDTHH:MM:SSZ | Resuelto |

## Root Cause
[Causa raíz técnica - 5 Whys]

## Impacto
- Usuarios afectados: X
- Funcionalidad: [qué falló]
- Datos: [pérdida/corrupción/ninguno]

## Qué funcionó bien
- [Detección rápida, rollback rápido, comunicación clara]

## Qué mejorar
- [Mejor monitoring, mejor tests, mejor docs]

## Action Items
| Acción | Responsable | Fecha límite | Issue GitHub |
|--------|-------------|--------------|--------------|
| Añadir alerta X | @usuario | YYYY-MM-DD | #123 |
| Test de regresión Y | @usuario | YYYY-MM-DD | #124 |
| Documentar runbook Z | @usuario | YYYY-MM-DD | #125 |

## Lecciones Aprendidas
[Reflexión del equipo]
```

---

## Runbooks Específicos

### Runbook: Base de Datos Caída (SEV-1)

**Síntomas**: `/health` → `{"status":"degraded","checks":{"db":false}}`, errores `connection refused` en logs

**Pasos**:
1. Verificar Railway PostgreSQL service: `railway status` / Dashboard
2. Si service down: `railway service restart postgresql` / Dashboard → Restart
3. Si connection pool agotado: Verificar `pool_size` en config, reiniciar backend
4. Si corrupción datos: Restaurar desde backup Railway (point-in-time recovery)
5. Verificar `/health` → OK

**Contactos**: Railway Support (si managed), @gabrie1hk

---

### Runbook: Deploy Fallido (SEV-2)

**Síntomas**: CI pasa pero deploy falla, healthcheck falla 3 veces

**Pasos**:
1. Verificar logs deploy en Railway/Vercel
2. Si healthcheck falla: Verificar `/health` localmente con misma imagen Docker
3. Si código: `git revert` último commit → Push → CI → Deploy
3. Si configuración: Revertir variables env → Redeploy
4. Verificar healthcheck staging → OK → Promote production

**Contactos**: @gabrie1hk, Railway Support

---

### Runbook: Brecha de Seguridad / Secreto Comprometido (SEV-1)

**Síntomas**: Alerta GitHub Secret Scanning, reporte externo, logs anómalos

**Pasos**:
1. **Inmediato**: Rotar secreto comprometido (ver `SECRETS.md` rotación emergencia)
2. Revocar tokens/sesiones afectadas (cambiar `AWEN_SECRET_KEY` → invalida JWTs)
3. Revisar logs acceso: `grep "secret" logs` / auditoría GitHub
3. Evaluar impacto: ¿Datos expuestos? ¿Acceso no autorizado?
4. Notificar si datos personales expuestos (GDPR/LOPD)
5. Post-mortem obligatorio en 48h

**Contactos**: @gabrie1hk, Legal (si datos personales)

---

### Runbook: Performance Degradada (SEV-2)

**Síntomas**: Latency P95 > 2s, error rate > 5%, timeouts

**Pasos**:
1. Verificar métricas: Railway metrics, DB query performance
2. Identificar query lenta: `EXPLAIN ANALYZE` en queries sospechosas
3. Verificar connection pool: `pool_size`, `max_overflow`
4. Mitigación temporal: Escalar Railway service (`railway up --scale`), añadir read replica
5. Fix definitivo: Optimizar query, añadir índice, cache

**Contactos**: @gabrie1hk

---

### Runbook: Vercel Build/Deploy Fallido (SEV-2)

**Síntomas**: `npm run build` falla, deploy Vercel error

**Pasos**:
1. Verificar logs build en Vercel Dashboard
2. Reproducir local: `npm run build` en frontend
3. Causas comunes:
   - TypeScript errors → Fix types
   - Dependencias faltantes → `npm ci` / actualizar `package-lock.json`
   - Memory limit → `NODE_OPTIONS="--max-old-space-size=4096"`
   - Env vars missing → Verificar Vercel Environment Variables
4. Fix → Push → Vercel redeploy automático

**Contactos**: @gabrie1hk

---

## Comunicación

### Canales

| Audiencia | Canal | Frecuencia |
|-----------|-------|------------|
| Equipo técnico | GitHub Issue + Discord/Slack | Tiempo real |
| Stakeholders | Email / GitHub Issue comments | Cada 30 min (SEV-1), 1h (SEV-2) |
| Usuarios finales | Banner en app / Email | Si impacto visible > 15 min |

### Plantillas Comunicación

**Iniciando investigación**:
> 🔴 **INCIDENTE SEV-[1-2]**: [Título]
> Iniciado: YYYY-MM-DD HH:MM UTC
> Impacto: [Descripción breve]
> Estado: Investigando
> Próxima actualización: HH:MM UTC

**Actualización**:
> 🟡 **ACTUALIZACIÓN**: [Título]
> Estado: [Investigando / Mitigando / Verificando fix]
> Próximos pasos: [Qué se hará]
> Próxima actualización: HH:MM UTC

**Resuelto**:
> 🟢 **RESUELTO**: [Título]
> Resuelto: YYYY-MM-DD HH:MM UTC
> Duración: Xh Ym
> Root cause: [Breve]
> Fix: [Qué se hizo]
> Post-mortem: [Link issue GitHub]

---

## Escalación

| Nivel | Contacto | Trigger |
|-------|----------|---------|
| Nivel 1 | On-call / Tech Lead (@gabrie1hk) | Inicio incidente |
| Nivel 2 | Engineering Lead / Arquitecto | > 30 min sin progreso (SEV-1), > 2h (SEV-2) |
| Nivel 3 | Dirección / Legal / Compliance | Brecha datos, downtime > 4h, impacto legal |

---

## Herramientas y Accesos

| Herramienta | Acceso | Uso en Incidente |
|-------------|--------|------------------|
| GitHub | Admin/Write | Issues, Actions, Deployments, Secrets |
| Railway | Owner/Admin | Logs, Metrics, Deploy, Rollback, DB |
| Vercel | Owner/Admin | Logs, Deploy, Rollback, Env Vars |
| GitHub Actions | Admin | CI logs, Re-run, Manual approvals |
| Docker Hub / ghcr.io | Read | Imágenes base, vulnerabilidades |

---

## Métricas de Salud (KPIs)

| Métrica | Objetivo | Alerta |
|---------|----------|--------|
| Uptime | 99.9% | < 99.5% → SEV-2 |
| Latency P95 | < 500ms | > 2s → SEV-2 |
| Error Rate | < 0.1% | > 1% → SEV-2 |
| Deploy Success Rate | 100% | < 95% → SEV-3 |
| MTTR (Mean Time To Recovery) | < 30 min (SEV-1) | > 1h → Review proceso |
| MTTA (Mean Time To Acknowledge) | < 15 min | > 30 min → Review on-call |

---

## Referencias

- [DEPLOY.md](./DEPLOY.md) - Proceso de despliegue
- [SECRETS.md](./SECRETS.md) - Gestión de secretos
- [Railway Docs](https://docs.railway.app)
- [Vercel Docs](https://vercel.com/docs)
- [GitHub Actions](https://docs.github.com/en/actions)