import { useEffect, useMemo, useState } from 'react'
import { useAuth } from '../hooks/useAuth'
import { parcelsApi, trackingApi, usersApi, mapsApi } from '../services/api'
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
  const [clientNotes, setClientNotes] = useState([])
  const [myParcels, setMyParcels] = useState([])
  const [showCreate, setShowCreate] = useState(false)
  const [mapComponents, setMapComponents] = useState(null)
  const [mapStep, setMapStep] = useState('origin')
  const [originPoint, setOriginPoint] = useState(null)
  const [destinationPoint, setDestinationPoint] = useState(null)
  const [routeData, setRouteData] = useState(null)
  const [loadingRoute, setLoadingRoute] = useState(false)
  const [creating, setCreating] = useState(false)
  const [createError, setCreateError] = useState('')
  const [formData, setFormData] = useState({
    sender: '',
    senderId: '',
    senderPhone: '',
    recipient: '',
    recipientId: '',
    recipientPhone: '',
    recipientAddress: '',
    weight: '',
    dimensions: '',
    declaredValue: '',
    description: '',
  })
  const { loading, error, setError, execute } = useApi()

  const defaultCenter = useMemo(() => [10.1620, -68.0077], [])

  useEffect(() => {
    let active = true
    import('react-leaflet')
      .then(mod => {
        if (!active) return
        setMapComponents({
          MapContainer: mod.MapContainer,
          TileLayer: mod.TileLayer,
          Marker: mod.Marker,
          Polyline: mod.Polyline,
          useMapEvents: mod.useMapEvents,
        })
      })
      .catch(() => {
        if (!active) return
        setMapComponents(null)
      })
    return () => { active = false }
  }, [])

  useEffect(() => {
    execute(() => parcelsApi.myParcels())
      .then(res => { if (res) setMyParcels(res.data || res) })
  }, [])

  useEffect(() => {
    if (destinationPoint) {
      setFormData(prev => ({
        ...prev,
        recipientAddress: prev.recipientAddress.trim()
          ? prev.recipientAddress
          : `${destinationPoint.lat.toFixed(5)}, ${destinationPoint.lng.toFixed(5)}`,
      }))
    }
  }, [destinationPoint])

  useEffect(() => {
    if (originPoint && destinationPoint) {
      setLoadingRoute(true)
      mapsApi.getRoute(originPoint.lat, originPoint.lng, destinationPoint.lat, destinationPoint.lng)
        .then(res => setRouteData(res))
        .catch(() => setRouteData(null))
        .finally(() => setLoadingRoute(false))
    } else {
      setRouteData(null)
    }
  }, [originPoint, destinationPoint])

  const handleSave = () => {
    usersApi.updateMe(profile)
      .then(() => { setMessage('Datos actualizados correctamente'); setEditing(false); setTimeout(() => setMessage(''), 3000) })
      .catch(() => { setMessage('Datos actualizados correctamente'); setEditing(false); setTimeout(() => setMessage(''), 3000) })
  }

  const handleTrack = (guide) => {
    setSelectedGuide(guide)
    setClientNotes([])
    parcelsApi.tracking(guide)
      .then(res => setTracking(res || []))
      .catch(() => {
        trackingApi.publicTrack(guide)
          .then(res => setTracking(res.history || res.tracking || res))
          .catch(() => setTracking(null))
      })
    parcelsApi.getNotes(guide)
      .then(res => setClientNotes(res || []))
      .catch(() => {})
  }

  useEffect(() => {
    if (!selectedGuide) return undefined
    const refresh = () => {
      parcelsApi.tracking(selectedGuide)
        .then(res => setTracking(res || []))
        .catch(() => {})
      parcelsApi.getNotes(selectedGuide)
        .then(res => setClientNotes(res || []))
        .catch(() => {})
    }
    const interval = setInterval(refresh, 10000)
    return () => clearInterval(interval)
  }, [selectedGuide])

  const updateField = (field) => (event) => {
    let value = event.target.value
    if (field === 'declaredValue') {
      value = value.replace(/\D/g, '')
    }
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  const resetCreate = () => {
    setShowCreate(false)
    setMapStep('origin')
    setOriginPoint(null)
    setDestinationPoint(null)
    setCreateError('')
    setFormData({
      sender: profile.name || user?.name || '',
      senderId: '',
      senderPhone: profile.phone || user?.phone || '',
      recipient: '',
      recipientId: '',
      recipientPhone: '',
      recipientAddress: '',
      weight: '',
      dimensions: '',
      declaredValue: '',
      description: '',
    })
  }

  const handleCreate = () => {
    setCreateError('')
    if (!originPoint || !destinationPoint) {
      setCreateError('Selecciona origen y destino en el mapa.')
      return
    }
    const requiredFields = [
      ['sender', 'Remitente'],
      ['senderId', 'ID Remitente'],
      ['senderPhone', 'Teléfono Remitente'],
      ['recipient', 'Destinatario'],
      ['recipientId', 'ID Destinatario'],
      ['recipientPhone', 'Teléfono Destinatario'],
      ['recipientAddress', 'Dirección Destinatario'],
    ]
    const missing = requiredFields
      .filter(([field]) => !formData[field]?.trim())
      .map(([, label]) => label)
    if (missing.length > 0) {
      setCreateError(`Faltan campos: ${missing.join(', ')}`)
      return
    }
    if (!Number(formData.weight) || Number(formData.weight) <= 0) {
      setCreateError('El peso debe ser mayor a 0')
      return
    }
    const payload = {
      sender: formData.sender,
      senderId: formData.senderId,
      senderPhone: formData.senderPhone,
      recipient: formData.recipient,
      recipientId: formData.recipientId,
      recipientPhone: formData.recipientPhone,
      recipientAddress: formData.recipientAddress,
      originAddress: null,
      originLat: originPoint.lat,
      originLng: originPoint.lng,
      destinationAddress: null,
      destinationLat: destinationPoint.lat,
      destinationLng: destinationPoint.lng,
      originBranch: null,
      destinationBranch: null,
      weight: Number(formData.weight || 0),
      dimensions: formData.dimensions || 'N/A',
      declaredValue: Number(formData.declaredValue || 0),
      description: formData.description || 'Sin descripción',
    }

    setCreating(true)
    parcelsApi.create(payload)
      .then((created) => {
        setMyParcels(prev => [created, ...prev])
        resetCreate()
      })
      .catch((err) => setCreateError(err.message || 'No se pudo crear la encomienda.'))
      .finally(() => setCreating(false))
  }

  const MapClickHandler = () => {
    if (!mapComponents?.useMapEvents) return null
    const { useMapEvents } = mapComponents
    useMapEvents({
      click: (event) => {
        const coords = { lat: event.latlng.lat, lng: event.latlng.lng }
        if (mapStep === 'origin') {
          setOriginPoint(coords)
          setMapStep('destination')
        } else {
          setDestinationPoint(coords)
        }
      },
    })
    return null
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
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-md)' }}>
            <h3>Envio Reciente</h3>
            <button className="btn btn-primary" onClick={() => {
              setFormData(prev => ({
                ...prev,
                sender: profile.name || user?.name || '',
                senderPhone: profile.phone || user?.phone || '',
              }))
              setShowCreate(true)
            }}>
              Nuevo Paquete
            </button>
          </div>
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
                    {p.originAddress || p.originBranch} → {p.destinationAddress || p.destinationBranch}
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
                  <td data-label="Origen" style={{ padding: '10px 12px' }}>{p.originAddress || p.originBranch}</td>
                  <td data-label="Destino" style={{ padding: '10px 12px' }}>{p.destinationAddress || p.destinationBranch}</td>
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
            {clientNotes.length > 0 && (
              <div style={{ marginTop: 'var(--space-lg)' }}>
                <h4 style={{ marginBottom: 8 }}>Notificaciones del Conductor</h4>
                {clientNotes.map((n, i) => (
                  <div key={i} style={{ padding: '10px 14px', background: 'var(--bg-tertiary)', borderRadius: 'var(--radius-md)', marginBottom: 6, fontSize: '0.813rem' }}>
                    <p>{n.text}</p>
                    <span style={{ fontSize: '0.688rem', color: 'var(--text-muted)' }}>{n.created_at} - {n.created_by}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
      {showCreate && (
        <div className="modal-overlay" onClick={resetCreate}>
          <div className="modal-content modal-form" onClick={e => e.stopPropagation()}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-lg)' }}>
              <h3>Nueva Encomienda</h3>
              <button className="btn-action" onClick={resetCreate}>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M6 18L18 6M6 6l12 12"/></svg>
              </button>
            </div>
            <div className="form-grid">
              <div className="form-field">
                <label>Remitente</label>
                <input value={formData.sender} onChange={updateField('sender')} />
              </div>
              <div className="form-field">
                <label>ID Remitente</label>
                <input value={formData.senderId} onChange={updateField('senderId')} />
              </div>
              <div className="form-field">
                <label>Telefono Remitente</label>
                <input value={formData.senderPhone} onChange={updateField('senderPhone')} />
              </div>
              <div className="form-field">
                <label>Destinatario *</label>
                <input value={formData.recipient} onChange={updateField('recipient')} />
              </div>
              <div className="form-field">
                <label>ID Destinatario *</label>
                <input value={formData.recipientId} onChange={updateField('recipientId')} />
              </div>
              <div className="form-field">
                <label>Telefono Destinatario *</label>
                <input value={formData.recipientPhone} onChange={updateField('recipientPhone')} />
              </div>
              <div className="form-field form-field-full">
                <label>Direccion Destinatario *</label>
                <input value={formData.recipientAddress} onChange={updateField('recipientAddress')} />
              </div>
              <div className="form-field">
                <label>Peso (kg) *</label>
                <input type="number" step="0.1" value={formData.weight} onChange={updateField('weight')} />
              </div>
              <div className="form-field">
                <label>Dimensiones</label>
                <input value={formData.dimensions} onChange={updateField('dimensions')} />
              </div>
              <div className="form-field">
                <label>Valor Declarado ($)</label>
                <input type="text" inputMode="numeric" value={formData.declaredValue} onChange={updateField('declaredValue')} />
              </div>
              <div className="form-field form-field-full">
                <label>Descripcion</label>
                <textarea rows="2" value={formData.description} onChange={updateField('description')} />
              </div>
            </div>
            <div className="tracking-map-section" style={{ marginTop: 'var(--space-lg)' }}>
              <h4>Selecciona Origen y Destino</h4>
              <p className="tracking-muted-note">Paso actual: {mapStep === 'origin' ? 'Origen' : 'Destino'}</p>
              <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginBottom: 12 }}>
                <button className="btn btn-outline" type="button" onClick={() => setMapStep('origin')}>Marcar Origen</button>
                <button className="btn btn-outline" type="button" onClick={() => setMapStep('destination')}>Marcar Destino</button>
                <button className="btn btn-outline" type="button" onClick={() => { setOriginPoint(null); setDestinationPoint(null); setMapStep('origin') }}>Limpiar</button>
              </div>
              <div className="tracking-map">
                {mapComponents?.MapContainer ? (
                  <mapComponents.MapContainer center={defaultCenter} zoom={11} scrollWheelZoom={false} style={{ height: '100%', width: '100%' }}>
                    <mapComponents.TileLayer
                      attribution='&copy; OpenStreetMap contributors'
                      url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    />
                    <MapClickHandler />
                    {originPoint && (
                      <mapComponents.Marker position={[originPoint.lat, originPoint.lng]} />
                    )}
                    {destinationPoint && (
                      <mapComponents.Marker position={[destinationPoint.lat, destinationPoint.lng]} />
                    )}
                    {routeData?.route?.length ? (
                      <mapComponents.Polyline positions={routeData.route.map(p => [p.lat, p.lng])} />
                    ) : originPoint && destinationPoint && (
                      <mapComponents.Polyline positions={[[originPoint.lat, originPoint.lng], [destinationPoint.lat, destinationPoint.lng]]} />
                    )}
                  </mapComponents.MapContainer>
                ) : (
                  <div className="tracking-map-placeholder">Mapa no disponible</div>
                )}
              </div>
              {loadingRoute && <p style={{ fontSize: '0.813rem', color: 'var(--text-muted)', marginTop: 4 }}>Calculando ruta...</p>}
              {routeData?.distance_km > 0 && (
                <p style={{ fontSize: '0.875rem', fontWeight: 600, marginTop: 4 }}>
                  Distancia: {routeData.distance_km} km
                </p>
              )}
            </div>
            {createError && <p style={{ color: 'var(--status-returned)', fontSize: '0.875rem', marginTop: 'var(--space-sm)' }}>{createError}</p>}
            <div className="modal-actions" style={{ marginTop: 'var(--space-lg)' }}>
              <button className="btn btn-outline" onClick={resetCreate}>Cancelar</button>
              <button className="btn btn-primary" onClick={handleCreate} disabled={creating}>
                {creating ? 'Guardando...' : 'Crear Encomienda'}
              </button>
            </div>
          </div>
        </div>
      )}
      </>
      )}
    </div>
  )
}
