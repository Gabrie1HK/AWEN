import { useState, useEffect } from 'react'
import { logisticsApi, parcelsApi } from '../services/api'
import StatusBadge from '../components/ui/StatusBadge'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import ErrorBanner from '../components/ui/ErrorBanner'
import { useApi } from '../hooks/useApi'

export default function Logistics() {
  const [selectedParcels, setSelectedParcels] = useState([])
  const [batches, setBatches] = useState([])
  const [vehicleList, setVehicleList] = useState([])
  const [parcelList, setParcelList] = useState([])

  const allParcels = parcelList.filter(p => p.status === 'Registered' || p.status === 'At Destination Branch')
  const { loading, error, setError, execute } = useApi()

  useEffect(() => {
    execute(() => logisticsApi.listBatches())
      .then(res => { if (res) setBatches(res.data || res) })
    execute(() => logisticsApi.listVehicles())
      .then(res => { if (res) setVehicleList(res.data || res) })
    execute(() => parcelsApi.list({ pageSize: 100 }))
      .then(res => { if (res) setParcelList(res.data || res) })
  }, [])

  const toggleParcel = (id) => {
    setSelectedParcels(prev =>
      prev.includes(id) ? prev.filter(p => p !== id) : [...prev, id]
    )
  }

  return (
    <div className="logistics-layout">
      <ErrorBanner message={error} onDismiss={() => setError(null)} />
      {loading ? <LoadingSpinner /> : (
      <>
      <div className="logistics-panel">
        <h3>Lotes Pendientes</h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-sm)', marginTop: 'var(--space-md)' }}>
          {batches.filter(b => b.status !== 'Completed').map(batch => (
            <div key={batch.id} className="batch-card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
                <strong>{batch.id}</strong>
                <StatusBadge status={batch.status} />
              </div>
              <p style={{ fontSize: '0.813rem', color: 'var(--text-secondary)' }}>
                {batch.parcelCount} encomienda{batch.parcelCount !== 1 ? 's' : ''}
              </p>
              {batch.parcelCount > 0 && (
                <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap', marginTop: 8 }}>
                  {batch.parcels.map(pid => {
                    const p = parcelList.find(x => x.id === pid)
                    return p ? (
                      <label key={pid} className={`parcel-chip ${selectedParcels.includes(pid) ? 'selected' : ''}`}>
                        <input
                          type="checkbox"
                          checked={selectedParcels.includes(pid)}
                          onChange={() => toggleParcel(pid)}
                        />
                        {p.guide}
                      </label>
                    ) : null
                  })}
                </div>
              )}
            </div>
          ))}
        </div>
        <div className="batch-card" style={{ marginTop: 'var(--space-md)', background: 'var(--bg-tertiary)' }}>
          <h4>Paquetes Disponibles</h4>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 4, marginTop: 8 }}>
            {allParcels.map(p => (
              <label key={p.id} className={`parcel-chip ${selectedParcels.includes(p.id) ? 'selected' : ''}`}>
                <input
                  type="checkbox"
                  checked={selectedParcels.includes(p.id)}
                  onChange={() => toggleParcel(p.id)}
                />
                {p.guide} — {p.destinationBranch}
              </label>
            ))}
          </div>
        </div>
      </div>

      <div className="logistics-panel">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-md)' }}>
          <h3>Vehículos y Conductores</h3>
          {selectedParcels.length > 0 && (
            <button className="btn btn-primary" style={{ fontSize: '0.813rem', padding: '6px 12px' }} onClick={() => {
              const targetBatch = batches.find(b => b.status === 'Pending Assignment')
              if (targetBatch) {
                logisticsApi.assignBatch(targetBatch.id, { parcels: selectedParcels })
                  .then(() => setBatches(prev => prev.map(b => b.id === targetBatch.id ? { ...b, parcels: [...b.parcels, ...selectedParcels], parcelCount: b.parcelCount + selectedParcels.length } : b)))
                  .catch(() => setError('No se pudo asignar el lote'))
                setSelectedParcels([])
              }
            }}>
              Asignar ({selectedParcels.length})
            </button>
          )}
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-md)' }}>
          {vehicleList.map(v => (
            <div key={v.id} className="driver-card">
              <div className="driver-avatar">
                {v.driver.split(' ').pop()[0]}
              </div>
              <div className="driver-info">
                <strong>{v.driver}</strong>
                <span style={{ fontSize: '0.813rem', color: 'var(--text-secondary)' }}>
                  {v.plate} — {v.model}
                </span>
              </div>
              <div className="driver-count">{v.capacity}</div>
            </div>
          ))}
        </div>

        <div style={{ marginTop: 'var(--space-xl)' }}>
          <h3 style={{ marginBottom: 'var(--space-md)' }}>Mapa de Rutas</h3>
          <div className="map-placeholder">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <path d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"/>
            </svg>
            <p>Vista de Mapa</p>
            <span>Integración con Google Maps / Mapbox próximamente</span>
          </div>
        </div>
      </div>
      </>
      )}
    </div>
  )
}
