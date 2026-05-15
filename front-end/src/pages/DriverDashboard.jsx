import { useState, useEffect, useCallback } from 'react'
import { useAuth } from '../hooks/useAuth'
import { parcelsApi, deliveriesApi } from '../services/api'
import StatusBadge from '../components/ui/StatusBadge'
import StepperTimeline from '../components/ui/StepperTimeline'

const STATUS_OPTIONS = [
  { value: 'Picked Up', label: 'Recogido' },
  { value: 'In Transit', label: 'En Transito' },
  { value: 'At Destination Branch', label: 'En Destino' },
  { value: 'Out for Delivery', label: 'En Reparto' },
  { value: 'Delivered', label: 'Entregado' },
]

const MOCK_PARCELS = [
  { id: 'ENV-001', guide: 'AWEN-2026-0001', sender: 'TechStore CA', recipient: 'Roberto Garcia', originBranch: 'Sucursal Central', destinationBranch: 'Sucursal Norte', status: 'In Transit', description: 'Notebook y accesorios', createdAt: '2026-05-10', recipientAddress: 'Av. Universidad 742, Caracas' },
  { id: 'ENV-006', guide: 'AWEN-2026-0006', sender: 'Moda Urbana CA', recipient: 'Daniela Rojas', originBranch: 'Sucursal Central', destinationBranch: 'Sucursal Sur', status: 'In Transit', description: 'Ropa y accesorios', createdAt: '2026-05-11', recipientAddress: 'Av. Andres Bello 890, Barquisimeto' },
]

const MOCK_HISTORY = {
  'AWEN-2026-0001': [
    { step: 'Registered', date: '2026-05-10', time: '14:30', location: 'Sucursal Central', operator: 'Operador Carlos', completed: true },
    { step: 'Picked Up', date: '2026-05-10', time: '16:00', location: 'Sucursal Central', operator: 'Conductor Pedro', completed: true },
    { step: 'In Transit', date: '2026-05-11', time: '08:00', location: 'Autopista Regional del Centro', operator: 'Conductor Pedro', completed: true },
  ],
  'AWEN-2026-0006': [
    { step: 'Registered', date: '2026-05-11', time: '10:00', location: 'Sucursal Central', operator: 'Operador Carlos', completed: true },
    { step: 'Picked Up', date: '2026-05-12', time: '09:00', location: 'Sucursal Central', operator: 'Conductor Pedro', completed: true },
  ],
}

export default function DriverDashboard() {
  const { user } = useAuth()
  const [parcels, setParcels] = useState([])
  const [selected, setSelected] = useState(null)
  const [tracking, setTracking] = useState(null)
  const [newStatus, setNewStatus] = useState('')
  const [note, setNote] = useState('')
  const [notes, setNotes] = useState({})
  const [msg, setMsg] = useState('')

  useEffect(() => {
    parcelsApi.myParcels()
      .then(setParcels)
      .catch(() => setParcels(MOCK_PARCELS))
  }, [])

  const handleView = async (p) => {
    setSelected(p)
    setNewStatus('')
    setNote('')
    setMsg('')
    try {
      const data = await parcelsApi.tracking(p.guide)
      setTracking(data)
    } catch {
      setTracking(MOCK_HISTORY[p.guide] || [])
    }
  }

  const handleUpdateStatus = async () => {
    if (!newStatus) return
    try {
      await parcelsApi.updateStatus(selected.id, newStatus)
      parcelsApi.tracking(selected.guide).then(setTracking).catch(() => {})
      setParcels(prev => prev.map(p => p.id === selected.id ? { ...p, status: newStatus } : p))
      setSelected(prev => ({ ...prev, status: newStatus }))
      setMsg('Estado actualizado correctamente')
    } catch {
      setParcels(prev => prev.map(p => p.id === selected.id ? { ...p, status: newStatus } : p))
      const updated = [...(MOCK_HISTORY[selected.guide] || [])]
      updated.push({ step: newStatus, date: '2026-05-15', time: new Date().toLocaleTimeString('es-CL', { hour: '2-digit', minute: '2-digit' }), location: 'En ruta', operator: user?.name, completed: true })
      MOCK_HISTORY[selected.guide] = updated
      setTracking(updated)
      setParcels(prev => prev.map(p => p.id === selected.id ? { ...p, status: newStatus } : p))
      setSelected(prev => ({ ...prev, status: newStatus }))
      setMsg('Estado actualizado (sin conexion al servidor)')
    }
  }

  const handleAddNote = () => {
    if (!note.trim()) return
    const key = selected.guide
    const existing = notes[key] || []
    const updated = [...existing, { text: note, date: new Date().toLocaleDateString(), by: user?.name }]
    setNotes({ ...notes, [key]: updated })
    setNote('')
    setMsg('Notificacion agregada')
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-xl)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>Mis Entregas</h2>
        <span style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>Conductor: {user?.name}</span>
      </div>

      {!selected ? (
        <div className="chart-card">
          {parcels.length === 0 ? (
            <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>No tienes entregas asignadas.</p>
          ) : (
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid var(--border-color)', textAlign: 'left', fontSize: '0.813rem', color: 'var(--text-secondary)' }}>
                  <th style={{ padding: '8px 12px' }}>Guia</th>
                  <th style={{ padding: '8px 12px' }}>Destinatario</th>
                  <th style={{ padding: '8px 12px' }}>Ruta</th>
                  <th style={{ padding: '8px 12px' }}>Estado</th>
                  <th style={{ padding: '8px 12px' }}></th>
                </tr>
              </thead>
              <tbody>
                {parcels.map(p => (
                  <tr key={p.id} style={{ borderBottom: '1px solid var(--border-color)' }}>
                    <td style={{ padding: '10px 12px', fontWeight: 600 }}>{p.guide}</td>
                    <td style={{ padding: '10px 12px' }}>{p.recipient}</td>
                    <td style={{ padding: '10px 12px', fontSize: '0.875rem' }}>{p.originBranch} → {p.destinationBranch}</td>
                    <td style={{ padding: '10px 12px' }}><StatusBadge status={p.status} /></td>
                    <td style={{ padding: '10px 12px' }}>
                      <button className="btn btn-outline" style={{ fontSize: '0.75rem', padding: '4px 10px' }} onClick={() => handleView(p)}>Gestionar</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
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
                  {STATUS_OPTIONS.map(o => (
                    <option key={o.value} value={o.value}>{o.label}</option>
                  ))}
                </select>
                <button className="btn btn-primary" onClick={handleUpdateStatus} disabled={!newStatus}>Actualizar</button>
              </div>
              {msg && <p style={{ marginTop: 8, fontSize: '0.813rem', color: msg.includes('Error') ? 'var(--status-returned)' : 'var(--status-delivered)' }}>{msg}</p>}
            </div>
            <div className="chart-card">
              <h4 style={{ marginBottom: 12 }}>Agregar Notificacion</h4>
              <div style={{ display: 'flex', gap: 8 }}>
                <input type="text" value={note} onChange={e => setNote(e.target.value)} placeholder="Ej: Retraso de 30 min por trafico" style={{ flex: 1 }} onKeyDown={e => e.key === 'Enter' && handleAddNote()} />
                <button className="btn btn-primary" onClick={handleAddNote} disabled={!note.trim()}>Enviar</button>
              </div>
              {notes[selected.guide] && notes[selected.guide].length > 0 && (
                <div style={{ marginTop: 12 }}>
                  {notes[selected.guide].map((n, i) => (
                    <div key={i} style={{ padding: '8px 12px', background: 'var(--bg-tertiary)', borderRadius: 'var(--radius-md)', marginBottom: 4, fontSize: '0.813rem' }}>
                      <p>{n.text}</p>
                      <span style={{ fontSize: '0.688rem', color: 'var(--text-muted)' }}>{n.date} - {n.by}</span>
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
    </div>
  )
}
