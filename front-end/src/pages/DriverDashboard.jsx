import { useState, useEffect } from 'react'
import { useAuth } from '../hooks/useAuth'
import { parcelsApi } from '../services/api'
import StatusBadge from '../components/ui/StatusBadge'
import StepperTimeline from '../components/ui/StepperTimeline'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import ErrorBanner from '../components/ui/ErrorBanner'
import { useApi } from '../hooks/useApi'

const STATUS_OPTIONS = [
  { value: 'Picked Up', label: 'Recogido' },
  { value: 'In Transit', label: 'En Transito' },
  { value: 'At Destination Branch', label: 'En Destino' },
  { value: 'Out for Delivery', label: 'En Reparto' },
  { value: 'Delivered', label: 'Entregado' },
]

export default function DriverDashboard() {
  const { user } = useAuth()
  const [parcels, setParcels] = useState([])
  const [selected, setSelected] = useState(null)
  const [tracking, setTracking] = useState(null)
  const [newStatus, setNewStatus] = useState('')
  const [note, setNote] = useState('')
  const [noteIsPublic, setNoteIsPublic] = useState(false)
  const [drvNotes, setDrvNotes] = useState([])
  const [msg, setMsg] = useState('')
  const { loading, error, setError, execute } = useApi()

  useEffect(() => {
    execute(() => parcelsApi.list({ pageSize: 50 }))
      .then(res => {
        if (res) {
          const list = res.data || res
          if (list.length > 0) setParcels(list)
        }
      })
  }, [])

  const handleView = (p) => {
    setSelected(p)
    setNewStatus('')
    setNote('')
    setMsg('')
    setDrvNotes([])
    setTracking([])
    parcelsApi.tracking(p.guide)
      .then(res => setTracking(res || []))
      .catch(() => setTracking([]))
    parcelsApi.getNotes(p.guide)
      .then(res => setDrvNotes(res || []))
      .catch(() => {})
  }

  const handleUpdateStatus = () => {
    if (!newStatus || !selected) return
    parcelsApi.updateStatus(selected.id, newStatus)
      .then((updated) => {
        setParcels(prev => prev.map(p => p.id === selected.id ? updated : p))
        setSelected(updated)
        setMsg('Estado actualizado correctamente')
        return parcelsApi.tracking(updated.guide)
      })
      .then(res => setTracking(res || []))
      .catch((err) => {
        setMsg(err?.message || 'No se pudo actualizar el estado')
      })
  }

  const handleAddNote = () => {
    if (!note.trim()) return
    const text = note
    const isPublic = noteIsPublic
    setNote('')
    setNoteIsPublic(false)
    parcelsApi.addNote(selected.guide, text, isPublic)
      .then(() => {
        setMsg(isPublic ? 'Comentario publicado' : 'Notificacion agregada')
        return parcelsApi.getNotes(selected.guide)
      })
      .then(res => setDrvNotes(res || []))
      .catch((err) => setMsg(err?.message || 'Error al agregar notificacion'))
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-xl)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>Mis Entregas</h2>
        <span style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>Conductor: {user?.name}</span>
      </div>

      <ErrorBanner message={error} onDismiss={() => setError(null)} />
      {loading ? <LoadingSpinner /> : (
      <>
      {!selected ? (
        <div className="chart-card">
          <table className="data-table" style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--border-medium)', textAlign: 'left', fontSize: '0.813rem', color: 'var(--text-secondary)' }}>
                <th style={{ padding: '8px 12px' }}>Guia</th>
                <th style={{ padding: '8px 12px' }}>Destinatario</th>
                <th style={{ padding: '8px 12px' }}>Ruta</th>
                <th style={{ padding: '8px 12px' }}>Estado</th>
                <th style={{ padding: '8px 12px' }}></th>
              </tr>
            </thead>
            <tbody>
              {parcels.map(p => (
                <tr key={p.id} style={{ borderBottom: '1px solid var(--border-medium)' }}>
                  <td data-label="Guia" style={{ padding: '10px 12px', fontWeight: 600 }}>{p.guide}</td>
                  <td data-label="Destinatario" style={{ padding: '10px 12px' }}>{p.recipient}</td>
                  <td data-label="Ruta" style={{ padding: '10px 12px', fontSize: '0.875rem' }}>{p.originBranch} → {p.destinationBranch}</td>
                  <td data-label="Estado" style={{ padding: '10px 12px' }}><StatusBadge status={p.status} /></td>
                  <td style={{ padding: '10px 12px' }}>
                    <button className="btn btn-outline" style={{ fontSize: '0.75rem', padding: '4px 10px' }} onClick={() => handleView(p)}>Gestionar</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-lg)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h3>Encomienda {selected.guide}</h3>
            <button className="btn btn-outline" onClick={() => setSelected(null)}>Volver</button>
          </div>

          <div className="kpi-grid" style={{ gridTemplateColumns: '1fr 1fr 1fr' }}>
            <div className="chart-card">
              <h4 style={{ marginBottom: 8 }}>Destinatario</h4>
              <p style={{ fontSize: '0.875rem' }}>{selected.recipient}</p>
              <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{selected.recipientAddress || 'Direccion no disponible'}</p>
            </div>
            <div className="chart-card">
              <h4 style={{ marginBottom: 8 }}>Paquete</h4>
              <p style={{ fontSize: '0.875rem' }}>{selected.description || 'Sin descripcion'}</p>
              <StatusBadge status={selected.status} />
            </div>
            <div className="chart-card">
              <h4 style={{ marginBottom: 8 }}>Ruta</h4>
              <p style={{ fontSize: '0.875rem' }}>{selected.originBranch} → {selected.destinationBranch}</p>
              <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Creado: {selected.createdAt}</p>
            </div>
          </div>

          <div className="kpi-grid" style={{ gridTemplateColumns: '1fr 1fr' }}>
            <div className="chart-card">
              <h4 style={{ marginBottom: 12 }}>Actualizar Estado</h4>
              <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
                <select value={newStatus} onChange={e => setNewStatus(e.target.value)} style={{ flex: 1, minWidth: 150 }}>
                  <option value="">Seleccionar...</option>
                  {STATUS_OPTIONS.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
                </select>
                <button className="btn btn-primary" onClick={handleUpdateStatus} disabled={!newStatus}>Actualizar</button>
              </div>
              {msg && <p style={{ marginTop: 8, fontSize: '0.813rem', color: 'var(--status-delivered)' }}>{msg}</p>}
            </div>
            <div className="chart-card">
              <h4 style={{ marginBottom: 12 }}>Agregar Notificacion</h4>
              <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
                <input type="text" value={note} onChange={e => setNote(e.target.value)} placeholder="Ej: Retraso de 30 min por trafico" style={{ flex: 1, minWidth: 180 }} onKeyDown={e => e.key === 'Enter' && handleAddNote()} />
                <label style={{ display: 'flex', alignItems: 'center', gap: 4, fontSize: '0.813rem', cursor: 'pointer', whiteSpace: 'nowrap' }}>
                  <input type="checkbox" checked={noteIsPublic} onChange={e => setNoteIsPublic(e.target.checked)} />
                  Publico
                </label>
                <button className="btn btn-primary" onClick={handleAddNote} disabled={!note.trim()}>Enviar</button>
              </div>
              {drvNotes.length > 0 && (
                <div style={{ marginTop: 12 }}>
                  {drvNotes.map((n, i) => (
                    <div key={i} style={{ padding: '8px 12px', background: 'var(--bg-tertiary)', borderRadius: 'var(--radius-md)', marginBottom: 4, fontSize: '0.813rem' }}>
                      <p>{n.text}</p>
                      <span style={{ fontSize: '0.688rem', color: 'var(--text-muted)' }}>
                        {n.is_public ? '🔓 Publico' : '🔒 Interno'} &middot; {n.created_at} &middot; {n.created_by}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          <div className="chart-card">
            <h4 style={{ marginBottom: 12 }}>Historial de Tracking</h4>
            {tracking && tracking.length > 0 ? (
              <StepperTimeline steps={tracking} />
            ) : (
              <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>Historial no disponible.</p>
            )}
          </div>
        </div>
      )}
      </>
      )}
    </div>
  )
}
