import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import { trackingApi } from '../services/api'
import StepperTimeline from '../components/ui/StepperTimeline'
import StatusBadge from '../components/ui/StatusBadge'

export default function Tracking() {
  const { user } = useAuth()
  const [guide, setGuide] = useState('')
  const [parcel, setParcel] = useState(null)
  const [history, setHistory] = useState(null)
  const [routePath, setRoutePath] = useState(null)
  const [publicNotes, setPublicNotes] = useState(null)
  const [notFound, setNotFound] = useState(false)
  const [mapState, setMapState] = useState({ status: 'idle', marker: null, route: null, message: '' })
  const [mapComponents, setMapComponents] = useState(null)
  const isInternal = user && user.role !== 'Client'

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
        })
      })
      .catch(() => {
        if (!active) return
        setMapComponents(null)
      })
    return () => { active = false }
  }, [])

  const completedSteps = useMemo(() => {
    if (!history) return []
    return history.filter(step => step.completed && step.lat && step.lng)
  }, [history])

  useEffect(() => {
    if (!parcel) {
      setMapState({ status: 'idle', marker: null, route: null, message: '' })
      return
    }

    if (!completedSteps.length && !routePath?.length) {
      setMapState({ status: 'empty', marker: null, route: null, message: 'Ubicacion no disponible' })
      return
    }

    const route = routePath?.length
      ? routePath.map(point => ({ lat: Number(point.lat), lng: Number(point.lng) }))
      : completedSteps.map(step => ({ lat: Number(step.lat), lng: Number(step.lng) }))
    const lastStep = route[route.length - 1]
    setMapState({ status: 'ready', marker: lastStep, route, message: '' })
  }, [completedSteps, parcel, routePath])

  const handleTrack = () => {
    if (!guide.trim()) return
    setNotFound(false)
    setParcel(null)
    setHistory(null)
    setRoutePath(null)
    setPublicNotes(null)
    trackingApi.publicTrack(guide.trim())
      .then(data => {
        if (data.parcel) {
          setParcel(data.parcel)
          setHistory(data.history || data.tracking || null)
          setRoutePath(data.route || null)
          setPublicNotes(data.public_notes || null)
          setNotFound(false)
        } else {
          setNotFound(true)
        }
      })
      .catch(() => {
        setNotFound(true)
      })
  }

  return (
    <div className="tracking-page">
      <div className="auth-back-row">
        <Link to="/" className="auth-back-link">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
            <path d="M19 12H5M12 19l-7-7 7-7" />
          </svg>
          Volver al inicio
        </Link>
      </div>
      <div className="tracking-hero">
        <div className="tracking-hero-icon">
          <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
            <path d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
          </svg>
        </div>
        <h2>Rastrea tu Envío</h2>
        <p>Ingresa el número de guía para conocer el estado de tu encomienda</p>
        <div className="tracking-search">
          <input
            type="text"
            placeholder="Ej: AWEN-2026-0001"
            value={guide}
            onChange={e => setGuide(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleTrack()}
          />
          <button className="btn btn-primary" onClick={handleTrack}>Rastrear</button>
        </div>
      </div>

      {parcel && (
        <div className="tracking-result">
          <div className="tracking-parcel-info">
            <div className="tracking-parcel-header">
              <div>
                <span className="tracking-guide-label">Guía</span>
                <h3>{parcel.guide}</h3>
              </div>
              <StatusBadge status={parcel.status} />
            </div>
            <div className="tracking-parcel-details">
              <div><span>Origen:</span> {parcel.originBranch}</div>
              <div><span>Destino:</span> {parcel.destinationBranch}</div>
              <div><span>Remitente:</span> {parcel.sender}</div>
              <div><span>Destinatario:</span> {parcel.recipient}</div>
              <div><span>Peso:</span> {parcel.weight} kg</div>
              {isInternal && parcel.declaredValue != null && <div><span>Valor:</span> ${parcel.declaredValue.toLocaleString()}</div>}
              {isInternal && parcel.description && <div><span>Descripción:</span> {parcel.description}</div>}
            </div>
          </div>

          <div className="tracking-timeline-section">
            <h4>Historial de Tracking</h4>
            {history ? (
              <StepperTimeline steps={history} />
            ) : (
              <p className="tracking-muted-note">Historial no disponible</p>
            )}
          </div>

          <div className="tracking-map-section">
            <h4>Ubicacion del Paquete</h4>
            {mapState.status === 'empty' && (
              <div className="tracking-map-placeholder">{mapState.message}</div>
            )}
            {mapState.status === 'ready' && mapState.marker && mapComponents?.MapContainer && (
              <div className="tracking-map">
                <mapComponents.MapContainer
                  center={[mapState.marker.lat, mapState.marker.lng]}
                  zoom={12}
                  scrollWheelZoom={false}
                  style={{ height: '100%', width: '100%' }}
                >
                  <mapComponents.TileLayer
                    attribution='&copy; OpenStreetMap contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                  />
                  <mapComponents.Marker position={[mapState.marker.lat, mapState.marker.lng]} />
                  {mapState.route?.length ? (
                    <mapComponents.Polyline positions={mapState.route.map(p => [p.lat, p.lng])} />
                  ) : null}
                </mapComponents.MapContainer>
              </div>
            )}
            {mapState.status === 'ready' && (!mapState.marker || !mapComponents?.MapContainer) && (
              <div className="tracking-map-placeholder">Ubicacion no disponible</div>
            )}
          </div>

          {publicNotes && publicNotes.length > 0 && (
            <div className="tracking-notes-section">
              <h4>Comentarios del Conductor</h4>
              {publicNotes.map((note, i) => (
                <div key={note.id || i} className="tracking-note-item">
                  <div className="tracking-note-icon">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/>
                    </svg>
                  </div>
                  <div className="tracking-note-body">
                    <p className="tracking-note-text">{note.text}</p>
                    <span className="tracking-note-meta">{note.created_by} &middot; {note.created_at}</span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {isInternal && (
            <div className="tracking-internal-panel">
              <h4>Acciones Internas</h4>
              <div className="tracking-internal-actions">
                <button className="btn btn-outline">Actualizar Estado</button>
                <button className="btn btn-outline">Agregar Nota</button>
                <button className="btn btn-outline">Reasignar</button>
              </div>
            </div>
          )}
        </div>
      )}

      {notFound && (
        <div className="tracking-not-found">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>
          </svg>
          <p>No se encontró ninguna encomienda con la guía <strong>{guide}</strong></p>
          <p className="tracking-muted-note">Verifica el número e intenta nuevamente</p>
        </div>
      )}
    </div>
  )
}
