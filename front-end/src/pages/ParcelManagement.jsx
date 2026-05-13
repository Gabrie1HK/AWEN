import { useState } from 'react'
import { parcels, branches } from '../data/mockData'
import StatusBadge from '../components/ui/StatusBadge'
import DataTable from '../components/ui/DataTable'
import SearchBar from '../components/ui/SearchBar'
import ConfirmModal from '../components/ui/ConfirmModal'

const statusOptions = [
  { value: 'Registered', label: 'Registrado' },
  { value: 'In Transit', label: 'En Tránsito' },
  { value: 'At Destination Branch', label: 'En Destino' },
  { value: 'Delivered', label: 'Entregado' },
  { value: 'Returned', label: 'Devuelto' },
]

const parcelsColumns = (onView, onEdit, onCancel) => [
  { key: 'guide', label: 'Guía #', sortable: true },
  { key: 'sender', label: 'Remitente', sortable: true },
  { key: 'recipient', label: 'Destinatario', sortable: true },
  { key: 'originBranch', label: 'Origen', sortable: true },
  { key: 'destinationBranch', label: 'Destino', sortable: true },
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
        <button className="btn-action btn-action-danger" title="Cancelar" onClick={() => onCancel(row)}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>
    ),
  },
]

export default function ParcelManagement() {
  const [search, setSearch] = useState('')
  const [statusFilter, setStatusFilter] = useState('')
  const [selectedParcel, setSelectedParcel] = useState(null)
  const [cancelTarget, setCancelTarget] = useState(null)
  const [showForm, setShowForm] = useState(false)

  const filtered = parcels.filter(p => {
    const matchesSearch = !search || p.guide.toLowerCase().includes(search.toLowerCase()) || p.sender.toLowerCase().includes(search.toLowerCase()) || p.recipient.toLowerCase().includes(search.toLowerCase())
    const matchesStatus = !statusFilter || p.status === statusFilter
    return matchesSearch && matchesStatus
  })

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-lg)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 'var(--space-md)' }}>
        <SearchBar
          search={search} onSearchChange={setSearch}
          filters={[{ key: 'status', value: statusFilter, placeholder: 'Filtrar por estado', options: statusOptions }]}
          onFilterChange={(k, v) => setStatusFilter(v)}
        />
        <button className="btn btn-primary" onClick={() => setShowForm(true)}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 4v16m8-8H4"/></svg>
          Nueva Encomienda
        </button>
      </div>

      <DataTable
        columns={parcelsColumns(
          p => setSelectedParcel(p),
          p => { setSelectedParcel(p); setShowForm(true) },
          p => setCancelTarget(p)
        )}
        data={filtered}
      />

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
                <span className="detail-meta">{selectedParcel.originBranch} → {selectedParcel.destinationBranch}</span>
                <div style={{ marginTop: 12 }}>
                  <StatusBadge status={selectedParcel.status} />
                </div>
              </div>
              <div className="detail-section">
                <h4>Códigos</h4>
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
        <div className="modal-overlay" onClick={() => setShowForm(false)}>
          <div className="modal-content modal-form" onClick={e => e.stopPropagation()}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-lg)' }}>
              <h3>{selectedParcel ? 'Editar Encomienda' : 'Nueva Encomienda'}</h3>
              <button className="btn-action" onClick={() => { setShowForm(false); setSelectedParcel(null) }}>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M6 18L18 6M6 6l12 12"/></svg>
              </button>
            </div>
            <div className="form-grid">
              <div className="form-field">
                <label>Remitente</label>
                <input type="text" placeholder="Nombre" defaultValue={selectedParcel?.sender} />
              </div>
              <div className="form-field">
                <label>RUT / ID Remitente</label>
                <input type="text" placeholder="XX.XXX.XXX-X" defaultValue={selectedParcel?.senderId} />
              </div>
              <div className="form-field">
                <label>Teléfono Remitente</label>
                <input type="text" placeholder="+56 9 XXXX XXXX" defaultValue={selectedParcel?.senderPhone} />
              </div>
              <div className="form-field">
                <label>Destinatario</label>
                <input type="text" placeholder="Nombre" defaultValue={selectedParcel?.recipient} />
              </div>
              <div className="form-field">
                <label>RUT / ID Destinatario</label>
                <input type="text" placeholder="XX.XXX.XXX-X" defaultValue={selectedParcel?.recipientId} />
              </div>
              <div className="form-field">
                <label>Teléfono Destinatario</label>
                <input type="text" placeholder="+56 9 XXXX XXXX" defaultValue={selectedParcel?.recipientPhone} />
              </div>
              <div className="form-field form-field-full">
                <label>Dirección Destinatario</label>
                <input type="text" placeholder="Calle, número, ciudad" defaultValue={selectedParcel?.recipientAddress} />
              </div>
              <div className="form-field">
                <label>Sucursal Origen</label>
                <select defaultValue={selectedParcel?.originBranch || ''}>
                  <option value="">Seleccionar...</option>
                  {branches.filter(b => b.active).map(b => <option key={b.id} value={b.name}>{b.name}</option>)}
                </select>
              </div>
              <div className="form-field">
                <label>Sucursal Destino</label>
                <select defaultValue={selectedParcel?.destinationBranch || ''}>
                  <option value="">Seleccionar...</option>
                  {branches.filter(b => b.active).map(b => <option key={b.id} value={b.name}>{b.name}</option>)}
                </select>
              </div>
              <div className="form-field">
                <label>Peso (kg)</label>
                <input type="number" step="0.1" placeholder="0.0" defaultValue={selectedParcel?.weight} />
              </div>
              <div className="form-field">
                <label>Dimensiones</label>
                <input type="text" placeholder="LxAxA cm" defaultValue={selectedParcel?.dimensions} />
              </div>
              <div className="form-field">
                <label>Valor Declarado ($)</label>
                <input type="number" placeholder="0" defaultValue={selectedParcel?.declaredValue} />
              </div>
              <div className="form-field form-field-full">
                <label>Descripción</label>
                <textarea rows="2" placeholder="Contenido del paquete" defaultValue={selectedParcel?.description} />
              </div>
            </div>
            <div className="modal-actions" style={{ marginTop: 'var(--space-lg)' }}>
              <button className="btn btn-outline" onClick={() => { setShowForm(false); setSelectedParcel(null) }}>Cancelar</button>
              <button className="btn btn-primary" onClick={() => { setShowForm(false); setSelectedParcel(null) }}>
                {selectedParcel ? 'Guardar Cambios' : 'Crear Encomienda'}
              </button>
            </div>
          </div>
        </div>
      )}

      <ConfirmModal
        open={!!cancelTarget}
        title="Cancelar Encomienda"
        message={`¿Estás seguro de cancelar la encomienda ${cancelTarget?.guide}? Esta acción no se puede deshacer.`}
        confirmLabel="Sí, Cancelar"
        onConfirm={() => { setCancelTarget(null) }}
        onCancel={() => setCancelTarget(null)}
      />
    </div>
  )
}
