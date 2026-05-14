import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import { parcels, trackingHistory } from '../data/mockData'
import StepperTimeline from '../components/ui/StepperTimeline'
import StatusBadge from '../components/ui/StatusBadge'

export default function Tracking() {
  const { user } = useAuth()
  const [guide, setGuide] = useState('')
  const [result, setResult] = useState(null)
  const [history, setHistory] = useState(null)
  const isInternal = user && user.role !== 'Client'

  const handleTrack = () => {
    if (!guide.trim()) return
    const parcel = parcels.find(p => p.guide === guide.trim())
    if (parcel) {
      setResult(parcel)
      setHistory(trackingHistory[parcel.guide] || null)
    } else {
      setResult(null)
      setHistory(null)
    }
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

      {result && (
        <div className="tracking-result">
          <div className="tracking-parcel-info">
            <div className="tracking-parcel-header">
              <div>
                <span className="tracking-guide-label">Guía</span>
                <h3>{result.guide}</h3>
              </div>
              <StatusBadge status={result.status} />
            </div>
            <div className="tracking-parcel-details">
              <div><span>Origen:</span> {result.originBranch}</div>
              <div><span>Destino:</span> {result.destinationBranch}</div>
              <div><span>Remitente:</span> {result.sender}</div>
              <div><span>Destinatario:</span> {result.recipient}</div>
              <div><span>Peso:</span> {result.weight} kg</div>
              {isInternal && <div><span>Valor:</span> ${result.declaredValue.toLocaleString()}</div>}
              {isInternal && <div><span>Descripción:</span> {result.description}</div>}
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

      {guide && !result && (
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
