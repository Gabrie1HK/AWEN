import { useState, useEffect, useCallback } from 'react'
import { useAuth } from '../hooks/useAuth'
import { parcelsApi, usersApi } from '../services/api'
import StatusBadge from '../components/ui/StatusBadge'

export default function ClientProfile() {
  const { user } = useAuth()
  const [parcels, setParcels] = useState([])
  const [profile, setProfile] = useState({ name: '', phone: '', address: '' })
  const [editing, setEditing] = useState(false)
  const [saving, setSaving] = useState(false)
  const [message, setMessage] = useState('')

  const fetchParcels = useCallback(async () => {
    try {
      const data = await parcelsApi.myParcels()
      setParcels(data)
    } catch {
      setParcels([])
    }
  }, [])

  const fetchProfile = useCallback(async () => {
    try {
      const data = await usersApi.me()
      setProfile({ name: data.name, phone: data.phone || '', address: data.address || '' })
    } catch {
      if (user) setProfile({ name: user.name, phone: user.phone || '', address: user.address || '' })
    }
  }, [user])

  useEffect(() => { fetchParcels(); fetchProfile() }, [fetchParcels, fetchProfile])

  const handleSave = async () => {
    setSaving(true)
    setMessage('')
    try {
      await usersApi.updateMe({ name: profile.name, phone: profile.phone, address: profile.address })
      setMessage('Datos actualizados correctamente')
      setEditing(false)
    } catch {
      setMessage('Error al guardar. Intente de nuevo.')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-xl)' }}>
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
              {message && <p style={{ color: message.includes('Error') ? 'var(--status-returned)' : 'var(--status-delivered)', fontSize: '0.875rem' }}>{message}</p>}
              <div className="modal-actions" style={{ marginTop: 8 }}>
                <button className="btn btn-outline" onClick={() => { setEditing(false); setMessage('') }}>Cancelar</button>
                <button className="btn btn-primary" onClick={handleSave} disabled={saving}>{saving ? 'Guardando...' : 'Guardar'}</button>
              </div>
            </div>
          )}
        </div>

        <div className="chart-card">
          <h3 style={{ marginBottom: 'var(--space-md)' }}>Envio Reciente</h3>
          {parcels.length === 0 ? (
            <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>No tienes envios registrados.</p>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              {parcels.slice(0, 3).map(p => (
                <div key={p.id} className="batch-card" style={{ padding: '12px' }}>
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
        {parcels.length === 0 ? (
          <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>No tienes envios registrados.</p>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--border-color)', textAlign: 'left', fontSize: '0.813rem', color: 'var(--text-secondary)' }}>
                <th style={{ padding: '8px 12px' }}>Guia</th>
                <th style={{ padding: '8px 12px' }}>Origen</th>
                <th style={{ padding: '8px 12px' }}>Destino</th>
                <th style={{ padding: '8px 12px' }}>Estado</th>
                <th style={{ padding: '8px 12px' }}>Fecha</th>
              </tr>
            </thead>
            <tbody>
              {parcels.map(p => (
                <tr key={p.id} style={{ borderBottom: '1px solid var(--border-color)' }}>
                  <td style={{ padding: '10px 12px', fontWeight: 600 }}>{p.guide}</td>
                  <td style={{ padding: '10px 12px' }}>{p.originBranch}</td>
                  <td style={{ padding: '10px 12px' }}>{p.destinationBranch}</td>
                  <td style={{ padding: '10px 12px' }}><StatusBadge status={p.status} /></td>
                  <td style={{ padding: '10px 12px', color: 'var(--text-secondary)', fontSize: '0.875rem' }}>{p.createdAt}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}
