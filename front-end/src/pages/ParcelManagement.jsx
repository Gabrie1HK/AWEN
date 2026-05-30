import { useState, useEffect, useCallback, useRef } from 'react'
import { parcelsApi, branchesApi, mapsApi } from '../services/api'
import StatusBadge from '../components/ui/StatusBadge'
import DataTable from '../components/ui/DataTable'
import SearchBar from '../components/ui/SearchBar'
import ConfirmModal from '../components/ui/ConfirmModal'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import ErrorBanner from '../components/ui/ErrorBanner'
import { useApi } from '../hooks/useApi'

const statusOptions = [
  { value: 'Registered', label: 'Registrado' },
  { value: 'In Transit', label: 'En Transito' },
  { value: 'At Destination Branch', label: 'En Destino' },
  { value: 'Delivered', label: 'Entregado' },
  { value: 'Returned', label: 'Devuelto' },
]

const parcelsColumns = (onView, onEdit, onDelete) => [
  { key: 'guide', label: 'Guia #', sortable: true },
  { key: 'sender', label: 'Remitente', sortable: true },
  { key: 'recipient', label: 'Destinatario', sortable: true },
  { key: 'originBranch', label: 'Origen', sortable: true, render: (row) => row.originAddress || row.originBranch },
  { key: 'destinationBranch', label: 'Destino', sortable: true, render: (row) => row.destinationAddress || row.destinationBranch },
  { key: 'weight', label: 'Peso (kg)', sortable: true },
  {
    key: 'status',
    label: 'Estado',
    sortable: true,
    render: (row) => <StatusBadge status={row.status} />,
  },
  { key: 'createdAt', label: 'Creado', sortable: true },
  {
    key: 'actions',
    label: 'Acciones',
    render: (row) => (
      <div style={{ display: 'flex', gap: 6 }}>
        <button className="btn-action" title="Ver" onClick={() => onView(row)}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
        </button>
        <button className="btn-action" title="Editar" onClick={() => onEdit(row)}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
        </button>
        <button className="btn-action btn-action-danger" title="Eliminar" onClick={() => onDelete(row)}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
        </button>
      </div>
    ),
  },
]

const PAGE_SIZE = 10
export default function ParcelManagement() {
  const [search, setSearch] = useState('')
  const [statusFilter, setStatusFilter] = useState('')
  const [selectedParcel, setSelectedParcel] = useState(null)
  const [deleteTarget, setDeleteTarget] = useState(null)
  const [showForm, setShowForm] = useState(false)

  const [parcelList, setParcelList] = useState([])
  const [branchList, setBranchList] = useState([])
  const [totalParcels, setTotalParcels] = useState(0)
  const [page, setPage] = useState(1)
  const formRef = useRef(null)
  const [mapComponents, setMapComponents] = useState(null)
  const [originPoint, setOriginPoint] = useState(null)
  const [destinationPoint, setDestinationPoint] = useState(null)
  const [mapStep, setMapStep] = useState('origin')
  const [routeData, setRouteData] = useState(null)
  const [loadingRoute, setLoadingRoute] = useState(false)
  const { loading, error, setError, execute } = useApi()

  const defaultCenter = [10.1620, -68.0077]

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
      .catch(() => { if (active) setMapComponents(null) })
    return () => { active = false }
  }, [])

  const fetchParcels = useCallback((p, s, st) => {
    execute(() => parcelsApi.list({ page: p, pageSize: PAGE_SIZE, search: s, status: st || undefined }))
      .then(res => {
        if (res) {
          setParcelList(res.data || res)
          setTotalParcels(res.total || res.length || 0)
        }
      })
  }, [execute])

  useEffect(() => {
    fetchParcels(page, search, statusFilter)
  }, [page, fetchParcels])

  useEffect(() => {
    setPage(1)
    fetchParcels(1, search, statusFilter)
  }, [search, statusFilter, fetchParcels])

  useEffect(() => {
    execute(() => branchesApi.list({ pageSize: 50 }))
      .then(res => { if (res) setBranchList(res.data || res) })
  }, [])

  useEffect(() => {
    if (destinationPoint) {
      const el = formRef.current?.elements?.recipientAddress
      if (el) el.value = `${destinationPoint.lat.toFixed(5)}, ${destinationPoint.lng.toFixed(5)}`
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

  useEffect(() => {
    if (selectedParcel && showForm) {
      if (selectedParcel.originLat && selectedParcel.originLng) {
        setOriginPoint({ lat: selectedParcel.originLat, lng: selectedParcel.originLng })
        if (selectedParcel.destinationLat && selectedParcel.destinationLng) {
          setDestinationPoint({ lat: selectedParcel.destinationLat, lng: selectedParcel.destinationLng })
          setMapStep('destination')
        } else {
          setMapStep('destination')
        }
      } else {
        setOriginPoint(null)
        setDestinationPoint(null)
        setMapStep('origin')
      }
    }
  }, [selectedParcel, showForm])

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
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-lg)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 'var(--space-md)' }}>
        <SearchBar
          search={search} onSearchChange={setSearch}
          filters={[{ key: 'status', value: statusFilter, placeholder: 'Filtrar por estado', options: statusOptions }]}
          onFilterChange={(k, v) => setStatusFilter(v)}
        />
        <button className="btn btn-primary" onClick={() => { setSelectedParcel(null); setOriginPoint(null); setDestinationPoint(null); setMapStep('origin'); setShowForm(true) }}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 4v16m8-8H4"/></svg>
          Nueva Encomienda
        </button>
      </div>

      <ErrorBanner message={error} onDismiss={() => setError(null)} />
      {loading ? <LoadingSpinner /> : (
      <DataTable
        columns={parcelsColumns(
          p => setSelectedParcel(p),
          p => { setSelectedParcel(p); setShowForm(true) },
          p => setDeleteTarget(p)
        )}
        data={parcelList}
        pageSize={PAGE_SIZE}
        totalItems={totalParcels}
        currentPage={page}
        onPageChange={setPage}
      />
      )}

      {selectedParcel && !showForm && (
        <div className="modal-overlay" onClick={() => setSelectedParcel(null)}>
          <div className="modal-content modal-wide" onClick={e => e.stopPropagation()}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-lg)' }}>
              <h3>Encomienda {selectedParcel.guide}</h3>
              <button className="btn-action" onClick={() => setSelectedParcel(null)}>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M6 18L18 6M6 6l12 12"/></svg>
              </button>
            </div>
            <div className="detail-grid">
              <div className="detail-section">
                <h4>Remitente</h4>
                <p>{selectedParcel.sender}</p>
                <span className="detail-meta">ID: {selectedParcel.senderId}</span>
                <span className="detail-meta">Tel: {selectedParcel.senderPhone}</span>
              </div>
              <div className="detail-section">
                <h4>Destinatario</h4>
                <p>{selectedParcel.recipient}</p>
                <span className="detail-meta">ID: {selectedParcel.recipientId}</span>
                <span className="detail-meta">Tel: {selectedParcel.recipientPhone}</span>
                <span className="detail-meta">Dir: {selectedParcel.recipientAddress}</span>
              </div>
              <div className="detail-section">
                <h4>Paquete</h4>
                <span className="detail-meta">Peso: {selectedParcel.weight} kg</span>
                <span className="detail-meta">Dimensiones: {selectedParcel.dimensions}</span>
                <span className="detail-meta">Valor decl.: ${selectedParcel.declaredValue.toLocaleString()}</span>
                <span className="detail-meta">Desc: {selectedParcel.description}</span>
              </div>
              <div className="detail-section">
                <h4>Ruta</h4>
                <span className="detail-meta">{(selectedParcel.originAddress || selectedParcel.originBranch)} → {(selectedParcel.destinationAddress || selectedParcel.destinationBranch)}</span>
                <div style={{ marginTop: 12 }}>
                  <StatusBadge status={selectedParcel.status} />
                </div>
              </div>
              <div className="detail-section">
                <h4>Codigos</h4>
                <div className="barcode-placeholder">{selectedParcel.barcode}</div>
                <div className="qr-placeholder">
                  <svg width="64" height="64" viewBox="0 0 64 64" fill="none">
                    <rect x="2" y="2" width="28" height="28" rx="2" stroke="currentColor" strokeWidth="2" fill="none"/>
                    <rect x="34" y="2" width="28" height="12" rx="2" stroke="currentColor" strokeWidth="2" fill="none"/>
                    <rect x="34" y="18" width="28" height="12" rx="2" stroke="currentColor" strokeWidth="2" fill="none"/>
                    <rect x="2" y="34" width="12" height="28" rx="2" stroke="currentColor" strokeWidth="2" fill="none"/>
                    <rect x="18" y="34" width="12" height="28" rx="2" stroke="currentColor" strokeWidth="2" fill="none"/>
                    <rect x="34" y="34" width="12" height="12" rx="2" stroke="currentColor" strokeWidth="2" fill="none"/>
                    <rect x="50" y="34" width="12" height="12" rx="2" stroke="currentColor" strokeWidth="2" fill="none"/>
                    <rect x="34" y="50" width="28" height="12" rx="2" stroke="currentColor" strokeWidth="2" fill="none"/>
                  </svg>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {showForm && (
        <div className="modal-overlay" onClick={() => { setShowForm(false); setSelectedParcel(null); setOriginPoint(null); setDestinationPoint(null); setMapStep('origin') }}>
          <div className="modal-content modal-form" onClick={e => e.stopPropagation()}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-lg)' }}>
              <h3>{selectedParcel ? 'Editar Encomienda' : 'Nueva Encomienda'}</h3>
              <button className="btn-action" onClick={() => { setShowForm(false); setSelectedParcel(null); setOriginPoint(null); setDestinationPoint(null); setMapStep('origin') }}>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M6 18L18 6M6 6l12 12"/></svg>
              </button>
            </div>
            <form ref={formRef} className="form-grid">
              <div className="form-field">
                <label>Remitente</label>
                <input name="sender" type="text" placeholder="Nombre" defaultValue={selectedParcel?.sender} />
              </div>
              <div className="form-field">
                <label>RUT / ID Remitente</label>
                <input name="senderId" type="text" placeholder="XX.XXX.XXX-X" defaultValue={selectedParcel?.senderId} />
              </div>
              <div className="form-field">
                <label>Telefono Remitente</label>
                <input name="senderPhone" type="text" placeholder="+58 X XXXX XXXX" defaultValue={selectedParcel?.senderPhone} />
              </div>
              <div className="form-field">
                <label>Destinatario</label>
                <input name="recipient" type="text" placeholder="Nombre" defaultValue={selectedParcel?.recipient} />
              </div>
              <div className="form-field">
                <label>RUT / ID Destinatario</label>
                <input name="recipientId" type="text" placeholder="XX.XXX.XXX-X" defaultValue={selectedParcel?.recipientId} />
              </div>
              <div className="form-field">
                <label>Telefono Destinatario</label>
                <input name="recipientPhone" type="text" placeholder="+58 X XXXX XXXX" defaultValue={selectedParcel?.recipientPhone} />
              </div>
              <div className="form-field form-field-full">
                <label>Direccion Destinatario</label>
                <input name="recipientAddress" type="text" placeholder="Calle, numero, ciudad" defaultValue={selectedParcel?.recipientAddress} />
              </div>
              <div className="form-field">
                <label>Sucursal Origen</label>
                <select name="originBranch" defaultValue={selectedParcel?.originBranch || ''}>
                  <option value="">Seleccionar...</option>
                  {branchList.filter(b => b.active).map(b => <option key={b.id} value={b.name}>{b.name}</option>)}
                </select>
              </div>
              <div className="form-field">
                <label>Sucursal Destino</label>
                <select name="destinationBranch" defaultValue={selectedParcel?.destinationBranch || ''}>
                  <option value="">Seleccionar...</option>
                  {branchList.filter(b => b.active).map(b => <option key={b.id} value={b.name}>{b.name}</option>)}
                </select>
              </div>
              <div className="form-field">
                <label>Peso (kg)</label>
                <input name="weight" type="number" step="0.1" placeholder="0.0" defaultValue={selectedParcel?.weight} />
              </div>
              <div className="form-field">
                <label>Dimensiones</label>
                <input name="dimensions" type="text" placeholder="LxAxA cm" defaultValue={selectedParcel?.dimensions} />
              </div>
              <div className="form-field">
                <label>Valor Declarado ($)</label>
                <input name="declaredValue" type="number" placeholder="0" defaultValue={selectedParcel?.declaredValue} />
              </div>
              <div className="form-field form-field-full">
                <label>Descripcion</label>
                <textarea name="description" rows="2" placeholder="Contenido del paquete" defaultValue={selectedParcel?.description} />
              </div>
            </form>
            <div className="tracking-map-section" style={{ marginTop: 'var(--space-lg)' }}>
              <h4>Ubicacion en el mapa (opcional)</h4>
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
            <div className="modal-actions" style={{ marginTop: 'var(--space-lg)' }}>
              <button className="btn btn-outline" onClick={() => { setShowForm(false); setSelectedParcel(null); setOriginPoint(null); setDestinationPoint(null); setMapStep('origin') }}>Cancelar</button>
              <button className="btn btn-primary" onClick={() => {
                const f = formRef.current
                if (!f) return
                const get = (n) => { const el = f.elements[n]; return el ? el.value || '' : '' }
                const declaredValueRaw = get('declaredValue').replace(/\D/g, '')
                const data = {
                  sender: get('sender'), senderId: get('senderId'), senderPhone: get('senderPhone'),
                  recipient: get('recipient'), recipientId: get('recipientId'), recipientPhone: get('recipientPhone'),
                  recipientAddress: get('recipientAddress'), originBranch: get('originBranch'),
                  destinationBranch: get('destinationBranch'), weight: parseFloat(get('weight')) || 0,
                  dimensions: get('dimensions'), declaredValue: parseFloat(declaredValueRaw) || 0,
                  description: get('description'),
                  originLat: originPoint?.lat || null,
                  originLng: originPoint?.lng || null,
                  destinationLat: destinationPoint?.lat || null,
                  destinationLng: destinationPoint?.lng || null,
                }
                if (selectedParcel) {
                  data.originAddress = selectedParcel.originAddress || null
                  data.destinationAddress = selectedParcel.destinationAddress || null
                } else {
                  data.originAddress = null
                  data.destinationAddress = null
                }
                if (selectedParcel) {
                  parcelsApi.update(selectedParcel.id, data)
                    .then(r => { 
                      setParcelList(prev => prev.map(p => p.id === selectedParcel.id ? r : p)) 
                      setShowForm(false); setSelectedParcel(null); setOriginPoint(null); setDestinationPoint(null); setMapStep('origin')
                    })
                    .catch(err => setError(err.message || 'No se pudo actualizar la encomienda'))
                } else {
                  parcelsApi.create(data)
                    .then(r => {
                      setParcelList(prev => [r, ...prev.slice(0, PAGE_SIZE - 1)])
                      setTotalParcels(t => t + 1)
                      setShowForm(false); setSelectedParcel(null); setOriginPoint(null); setDestinationPoint(null); setMapStep('origin')
                    })
                    .catch(err => setError(err.message || 'No se pudo crear la encomienda'))
                }
              }}>
                {selectedParcel ? 'Guardar Cambios' : 'Crear Encomienda'}
              </button>
            </div>
          </div>
        </div>
      )}

      <ConfirmModal
        open={!!deleteTarget}
        title="Eliminar Encomienda"
        message={`Estas seguro de eliminar la encomienda ${deleteTarget?.guide}? Esta accion no se puede deshacer.`}
        confirmLabel="Si, Eliminar"
        onConfirm={() => {
          const target = deleteTarget
          parcelsApi.remove(target.id)
            .then(() => { setParcelList(prev => prev.filter(p => p.id !== target.id)); setTotalParcels(t => t - 1) })
            .catch(() => setError('No se pudo eliminar la encomienda'))
          setDeleteTarget(null)
        }}
        onCancel={() => setDeleteTarget(null)}
      />
    </div>
  )
}
