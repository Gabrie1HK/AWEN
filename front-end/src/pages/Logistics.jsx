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
  const [vehicleSelections, setVehicleSelections] = useState({})
  const [assigning, setAssigning] = useState({})
  const [creating, setCreating] = useState(false)
  const [expandedBatch, setExpandedBatch] = useState(null)
  const [addParcelsBatch, setAddParcelsBatch] = useState(null)
  const [addParcelSelection, setAddParcelSelection] = useState([])
  const [targetBatch, setTargetBatch] = useState('')

  const allParcels = parcelList.filter(p => p.status === 'Registered' || p.status === 'At Destination Branch')
  const { loading, error, setError, execute } = useApi()

  useEffect(() => {
    loadData()
  }, [])

  function loadData() {
    execute(() => logisticsApi.listBatches())
      .then(res => { if (res) setBatches(res.data || res) })
    execute(() => logisticsApi.listVehicles())
      .then(res => { if (res) setVehicleList(res.data || res) })
    execute(() => parcelsApi.list({ pageSize: 100 }))
      .then(res => { if (res) setParcelList(res.data || res) })
  }

  const toggleParcel = (id) => {
    setSelectedParcels(prev =>
      prev.includes(id) ? prev.filter(p => p !== id) : [...prev, id]
    )
  }

  async function handleCreateLot() {
    if (selectedParcels.length === 0) return
    setCreating(true)
    try {
      const batch = await logisticsApi.createBatch({ parcels: selectedParcels })
      setBatches(prev => [...prev, batch])
      setSelectedParcels([])
    } catch {
      setError('No se pudo crear el lote')
    } finally {
      setCreating(false)
    }
  }

  async function handleAssign(batchId) {
    const vehicleId = vehicleSelections[batchId]
    if (!vehicleId) return
    const vehicle = vehicleList.find(v => v.id === vehicleId)
    if (!vehicle) return
    setAssigning(prev => ({ ...prev, [batchId]: true }))
    try {
      const updated = await logisticsApi.assignBatch(batchId, {
        vehicle: vehicle.plate,
        driver: vehicle.driver,
      })
      setBatches(prev => prev.map(b => b.id === batchId ? updated : b))
    } catch {
      setError('No se pudo asignar el lote')
    } finally {
      setAssigning(prev => ({ ...prev, [batchId]: false }))
    }
  }

  async function handleAddParcelsToBatch(batchId) {
    if (addParcelSelection.length === 0) return
    const batch = batches.find(b => b.id === batchId)
    if (!batch) return
    const merged = [...new Set([...batch.parcels, ...addParcelSelection])]
    try {
      const updated = await logisticsApi.updateBatch(batchId, { parcels: merged })
      setBatches(prev => prev.map(b => b.id === batchId ? updated : b))
      setAddParcelSelection([])
      setAddParcelsBatch(null)
    } catch {
      setError('No se pudieron agregar los envios al lote')
    }
  }

  async function handleAssignParcelsToBatch() {
    if (!targetBatch || selectedParcels.length === 0) return
    const batch = batches.find(b => b.id === targetBatch)
    if (!batch) return
    const merged = [...new Set([...batch.parcels, ...selectedParcels])]
    try {
      const updated = await logisticsApi.updateBatch(targetBatch, { parcels: merged })
      setBatches(prev => prev.map(b => b.id === targetBatch ? updated : b))
      setSelectedParcels([])
      setTargetBatch('')
    } catch {
      setError('No se pudieron agregar los envios al lote')
    }
  }

  const pendingBatches = batches.filter(b => b.status !== 'Completed')
  const unassignedVehicles = vehicleList.filter(v =>
    !batches.some(b => b.status === 'Assigned' && b.vehicle === v.plate)
  )
  const availableForAdd = allParcels.filter(p =>
    !addParcelsBatch || !batches.find(b => b.id === addParcelsBatch)?.parcels.includes(p.id)
  )

  return (
    <div className="logistics-layout">
      <ErrorBanner message={error} onDismiss={() => setError(null)} />
      {loading ? <LoadingSpinner /> : (
      <>
      <div className="logistics-panel">
        <h3>Lotes Pendientes</h3>
        {pendingBatches.length === 0 && (
          <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', marginTop: 'var(--space-md)' }}>
            No hay lotes pendientes
          </p>
        )}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-sm)', marginTop: 'var(--space-md)' }}>
          {pendingBatches.map(batch => {
            const isExpanded = expandedBatch === batch.id
            const isAdding = addParcelsBatch === batch.id
            return (
            <div key={batch.id} className={`batch-card ${isExpanded ? 'expanded' : ''}`}>
              <div
                style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8, cursor: 'pointer' }}
                onClick={() => setExpandedBatch(isExpanded ? null : batch.id)}
              >
                <strong>{batch.id}</strong>
                <StatusBadge status={batch.status} />
              </div>
              <p
                style={{ fontSize: '0.813rem', color: 'var(--text-secondary)', cursor: 'pointer' }}
                onClick={() => setExpandedBatch(isExpanded ? null : batch.id)}
              >
                {batch.parcelCount} encomienda{batch.parcelCount !== 1 ? 's' : ''}
                {batch.vehicle && ` — ${batch.vehicle}`}
              </p>

              {isExpanded && (
                <div style={{ marginTop: 12 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
                    <strong style={{ fontSize: '0.813rem' }}>Envíos del lote</strong>
                    <button
                      className="btn btn-outline"
                      style={{ fontSize: '0.75rem', padding: '4px 8px' }}
                      onClick={(e) => { e.stopPropagation(); setAddParcelsBatch(isAdding ? null : batch.id); setAddParcelSelection([]) }}
                    >
                      {isAdding ? 'Cancelar' : '+ Agregar Envíos'}
                    </button>
                  </div>
                  {batch.parcels.length === 0 ? (
                    <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Sin envíos asignados</p>
                  ) : (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                      {batch.parcels.map(pid => {
                        const p = parcelList.find(x => x.id === pid)
                        return p ? (
                          <div key={pid} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.75rem', padding: '4px 8px', background: 'var(--surface-base)', borderRadius: 'var(--radius-sm)' }}>
                            <span><strong>{p.guide}</strong> — {p.originBranch} → {p.destinationBranch}</span>
                            <StatusBadge status={p.status} />
                          </div>
                        ) : (
                          <div key={pid} style={{ fontSize: '0.75rem', color: 'var(--text-muted)', padding: '4px 8px' }}>
                            {pid}
                          </div>
                        )
                      })}
                    </div>
                  )}

                  {isAdding && (
                    <div style={{ marginTop: 8, padding: 8, background: 'var(--surface-base)', borderRadius: 'var(--radius-sm)' }}>
                      <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginBottom: 6 }}>Seleccionar envíos para agregar:</p>
                      {availableForAdd.length === 0 && (
                        <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>No hay envíos disponibles</p>
                      )}
                      <div style={{ display: 'flex', flexDirection: 'column', gap: 3, maxHeight: 200, overflowY: 'auto' }}>
                        {availableForAdd.map(p => (
                          <label key={p.id} className={`parcel-chip ${addParcelSelection.includes(p.id) ? 'selected' : ''}`} style={{ fontSize: '0.688rem' }}>
                            <input
                              type="checkbox"
                              checked={addParcelSelection.includes(p.id)}
                              onChange={() => setAddParcelSelection(prev =>
                                prev.includes(p.id) ? prev.filter(x => x !== p.id) : [...prev, p.id]
                              )}
                            />
                            {p.guide} — {p.destinationBranch}
                          </label>
                        ))}
                      </div>
                      {addParcelSelection.length > 0 && (
                        <button
                          className="btn btn-primary"
                          style={{ marginTop: 8, fontSize: '0.75rem', padding: '4px 10px' }}
                          onClick={() => handleAddParcelsToBatch(batch.id)}
                        >
                          Agregar ({addParcelSelection.length})
                        </button>
                      )}
                    </div>
                  )}
                </div>
              )}

              {batch.status === 'Pending Assignment' && (
                <div style={{ display: 'flex', gap: 8, alignItems: 'center', marginTop: 12, paddingTop: 12, borderTop: '1px solid var(--border-color)' }}>
                  <select
                    className="form-select"
                    style={{ flex: 1, fontSize: '0.813rem', padding: '6px 8px' }}
                    value={vehicleSelections[batch.id] || ''}
                    onChange={e => setVehicleSelections(prev => ({ ...prev, [batch.id]: Number(e.target.value) }))}
                  >
                    <option value="">Seleccionar vehículo...</option>
                    {unassignedVehicles.map(v => (
                      <option key={v.id} value={v.id}>{v.plate} — {v.driver}</option>
                    ))}
                  </select>
                  <button
                    className="btn btn-primary"
                    style={{ fontSize: '0.813rem', padding: '6px 12px', whiteSpace: 'nowrap' }}
                    disabled={!vehicleSelections[batch.id] || assigning[batch.id]}
                    onClick={() => handleAssign(batch.id)}
                  >
                    {assigning[batch.id] ? 'Asignando...' : 'Asignar'}
                  </button>
                </div>
              )}
            </div>
            )
          })}
        </div>

        <div className="batch-card" style={{ marginTop: 'var(--space-md)', background: 'var(--bg-tertiary)' }}>
          <h4>Paquetes Disponibles</h4>
          {allParcels.length === 0 && (
            <p style={{ fontSize: '0.813rem', color: 'var(--text-secondary)', marginTop: 8 }}>
              No hay paquetes disponibles
            </p>
          )}
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
          {selectedParcels.length > 0 && (
            <div style={{ display: 'flex', gap: 8, marginTop: 12, flexWrap: 'wrap' }}>
              <button
                className="btn btn-primary"
                style={{ fontSize: '0.813rem', padding: '6px 12px' }}
                disabled={creating}
                onClick={handleCreateLot}
              >
                {creating ? 'Creando...' : `Crear Lote (${selectedParcels.length})`}
              </button>
              <select
                className="form-select"
                style={{ fontSize: '0.813rem', padding: '6px 8px', minWidth: 180 }}
                value={targetBatch}
                onChange={e => setTargetBatch(e.target.value)}
              >
                <option value="">Agregar a lote...</option>
                {pendingBatches.filter(b => b.status === 'Pending Assignment').map(b => (
                  <option key={b.id} value={b.id}>{b.id}</option>
                ))}
              </select>
              {targetBatch && (
                <button
                  className="btn btn-outline"
                  style={{ fontSize: '0.813rem', padding: '6px 12px' }}
                  onClick={handleAssignParcelsToBatch}
                >
                  Agregar a {targetBatch}
                </button>
              )}
            </div>
          )}
        </div>
      </div>

      <div className="logistics-panel">
        <h3>Vehículos y Conductores</h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-md)', marginTop: 'var(--space-md)' }}>
          {vehicleList.map(v => {
            const assigned = batches.find(b => b.vehicle === v.plate && b.status !== 'Completed')
            return (
              <div key={v.id} className={`driver-card ${assigned ? '' : 'available'}`}>
                <div className="driver-avatar">
                  {v.driver.split(' ').pop()[0]}
                </div>
                <div className="driver-info">
                  <strong>{v.driver}</strong>
                  <span style={{ fontSize: '0.813rem', color: 'var(--text-secondary)' }}>
                    {v.plate} — {v.model}
                  </span>
                  <span style={{ fontSize: '0.75rem', color: assigned ? 'var(--status-returned)' : 'var(--status-delivered)' }}>
                    {assigned ? `Asignado a ${assigned.id}` : 'Disponible'}
                  </span>
                </div>
                <div className="driver-count">{v.capacity}</div>
              </div>
            )
          })}
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
