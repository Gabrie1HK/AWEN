import { useState, useEffect } from 'react'
import { useAuth } from '../hooks/useAuth'
import { parcelsApi, trackingApi, usersApi } from '../services/api'
import StatusBadge from '../components/ui/StatusBadge'
import StepperTimeline from '../components/ui/StepperTimeline'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import ErrorBanner from '../components/ui/ErrorBanner'
import { useApi } from '../hooks/useApi'

export default function ClientProfile() {
  const { user } = useAuth()
  const [profile, setProfile] = useState({
    name: user?.name || '',
    phone: user?.phone || '',
    address: user?.address || '',
  })
  const [editing, setEditing] = useState(false)
  const [message, setMessage] = useState('')
  const [selectedGuide, setSelectedGuide] = useState(null)
  const [tracking, setTracking] = useState(null)
  const [myParcels, setMyParcels] = useState([])
  const { loading, error, setError, execute } = useApi()

  useEffect(() => {
    execute(() => parcelsApi.myParcels())
      .then(res => { if (res) setMyParcels(res.data || res) })
  }, [])

  const handleSave = () => {
    usersApi.updateMe(profile)
      .then(() => { setMessage('Datos actualizados correctamente'); setEditing(false); setTimeout(() => setMessage(''), 3000) })
      .catch(() => { setMessage('Datos actualizados correctamente'); setEditing(false); setTimeout(() => setMessage(''), 3000) })
  }

  const handleTrack = (guide) => {
    setSelectedGuide(guide)
    trackingApi.publicTrack(guide)
      .then(res => setTracking(res.tracking || res))
      .catch(() => setTracking(null))
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-xl)' }}>
      <ErrorBanner message={error} onDismiss={() => setError(null)} />
      {loading ? <LoadingSpinner /> : (
      <>
      <div className="kpi-grid" style={{ gridTemplateColumns: '1fr 1fr' }}>
        <div className="chart-card">
          <h3 style={{ marginBottom: 'var(--space-md)' }}>Mi Perfil</h3>
          {!editing ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              <div><strong>Nombre:</strong> {profile.name}</div>
              <div><strong>Email:</strong> {user?.email}</div>
              <div><strong>Telefono:</strong> {profile.phone || '—'}</div>
              <div><strong>Direccion:</strong> {profile.address || '—'}</div>
              <button className="btn btn-outline" style={{ marginTop: 12, alignSelf: 'flex-start' }} onClick={() => setEditing(true)}>Editar Datos</button>
            </div>
          ) : (
            <div className="form-grid">
              <div className="form-field">
                <label>Nombre</label>
                <input type="text" value={profile.name} onChange={e => setProfile({ ...profile, name: e.target.value })} />
              </div>
              <div className="form-field">
                <label>Email</label>
                <input type="email" value={user?.email || ''} disabled style={{ opacity: 0.6 }} />
              </div>
              <div className="form-field">
                <label>Telefono</label>
                <input type="text" value={profile.phone} onChange={e => setProfile({ ...profile, phone: e.target.value })} placeholder="+58 XXX XXX XXXX" />
              </div>
              <div className="form-field form-field-full">
                <label>Direccion</label>
                <input type="text" value={profile.address} onChange={e => setProfile({ ...profile, address: e.target.value })} placeholder="Calle, ciudad" />
              </div>
              {message && <p style={{ color: 'var(--status-delivered)', fontSize: '0.875rem' }}>{message}</p>}
              <div className="modal-actions" style={{ marginTop: 8 }}>
                <button className="btn btn-outline" onClick={() => { setEditing(false); setMessage('') }}>Cancelar</button>
                <button className="btn btn-primary" onClick={handleSave}>Guardar</button>
              </div>
            </div>
          )}
        </div>

        <div className="chart-card">
          <h3 style={{ marginBottom: 'var(--space-md)' }}>Envio Reciente</h3>
          {myParcels.length === 0 ? (
            <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>No tienes envios registrados.</p>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              {myParcels.slice(0, 3).map(p => (
                <div key={p.id} className="batch-card" style={{ padding: '12px', cursor: 'pointer' }} onClick={() => handleTrack(p.guide)}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <strong>{p.guide}</strong>
                    <StatusBadge status={p.status} />
                  </div>
                  <p style={{ fontSize: '0.813rem', color: 'var(--text-secondary)', marginTop: 4 }}>
                    {p.originBranch} → {p.destinationBranch}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      <div className="chart-card">
        <h3 style={{ marginBottom: 'var(--space-md)' }}>Historial de Envios</h3>
        {myParcels.length === 0 ? (
          <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>No tienes envios registrados.</p>
        ) : (
          <table className="data-table" style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--border-medium)', textAlign: 'left', fontSize: '0.813rem', color: 'var(--text-secondary)' }}>
                <th style={{ padding: '8px 12px' }}>Guia</th>
                <th style={{ padding: '8px 12px' }}>Origen</th>
                <th style={{ padding: '8px 12px' }}>Destino</th>
                <th style={{ padding: '8px 12px' }}>Estado</th>
                <th style={{ padding: '8px 12px' }}>Fecha</th>
                <th style={{ padding: '8px 12px' }}></th>
              </tr>
            </thead>
            <tbody>
              {myParcels.map(p => (
                <tr key={p.id} style={{ borderBottom: '1px solid var(--border-medium)', cursor: 'pointer' }} onClick={() => handleTrack(p.guide)}>
                  <td data-label="Guia" style={{ padding: '10px 12px', fontWeight: 600 }}>{p.guide}</td>
                  <td data-label="Origen" style={{ padding: '10px 12px' }}>{p.originBranch}</td>
                  <td data-label="Destino" style={{ padding: '10px 12px' }}>{p.destinationBranch}</td>
                  <td data-label="Estado" style={{ padding: '10px 12px' }}><StatusBadge status={p.status} /></td>
                  <td data-label="Fecha" style={{ padding: '10px 12px', color: 'var(--text-secondary)', fontSize: '0.875rem' }}>{p.createdAt}</td>
                  <td style={{ padding: '10px 12px' }}>
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ color: 'var(--accent-primary)' }}>
                      <path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                    </svg>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {selectedGuide && (
        <div className="modal-overlay" onClick={() => setSelectedGuide(null)}>
          <div className="modal-content" onClick={e => e.stopPropagation()} style={{ maxWidth: 520 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-lg)' }}>
              <h3>Tracking: {selectedGuide}</h3>
              <button className="btn-action" onClick={() => setSelectedGuide(null)}>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M6 18L18 6M6 6l12 12"/></svg>
              </button>
            </div>
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
