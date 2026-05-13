import { useState } from 'react'
import { deliveries } from '../data/mockData'
import StatusBadge from '../components/ui/StatusBadge'
import DataTable from '../components/ui/DataTable'

const columns = (onView) => [
  { key: 'guide', label: 'Guía #', sortable: true },
  { key: 'recipient', label: 'Destinatario', sortable: true },
  { key: 'driver', label: 'Conductor', sortable: true },
  { key: 'deliveryDate', label: 'Fecha Entrega', sortable: true, render: (r) => r.deliveryDate || <span style={{ color: 'var(--text-muted)' }}>—</span> },
  { key: 'podType', label: 'Tipo POD', sortable: true },
  { key: 'status', label: 'Estado', render: (r) => <StatusBadge status={r.status} /> },
  {
    key: 'actions', label: 'Acciones',
    render: (r) => <button className="btn btn-outline" style={{ fontSize: '0.75rem', padding: '4px 10px' }} onClick={() => onView(r)}>Ver POD</button>,
  },
]

export default function ProofOfDelivery() {
  const [selected, setSelected] = useState(null)

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-lg)' }}>
      <DataTable columns={columns(d => setSelected(d))} data={deliveries} />

      {selected && (
        <div className="modal-overlay" onClick={() => setSelected(null)}>
          <div className="modal-content modal-wide" onClick={e => e.stopPropagation()}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-lg)' }}>
              <h3>Comprobante de Entrega</h3>
              <button className="btn-action" onClick={() => setSelected(null)}>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M6 18L18 6M6 6l12 12"/></svg>
              </button>
            </div>
            <div className="pod-grid">
              <div className="pod-info">
                <div className="detail-section">
                  <h4>Información</h4>
                  <span className="detail-meta">Guía: {selected.guide}</span>
                  <span className="detail-meta">Destinatario: {selected.recipient}</span>
                  <span className="detail-meta">Conductor: {selected.driver}</span>
                  <span className="detail-meta">Fecha: {selected.deliveryDate || 'Pendiente'}</span>
                  <span className="detail-meta">Tipo: {selected.podType}</span>
                  <span className="detail-meta">GPS: {selected.gps}</span>
                  <div style={{ marginTop: 8 }}>
                    <StatusBadge status={selected.status} />
                  </div>
                </div>
              </div>
              <div className="pod-evidence">
                <h4>Evidencia</h4>
                {selected.podType === 'Signature' ? (
                  <div className="pod-placeholder signature-placeholder">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                      <path d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/>
                    </svg>
                    <p>Imagen de Firma Digital</p>
                    <span>Capturada en dispositivo móvil</span>
                  </div>
                ) : (
                  <div className="pod-placeholder photo-placeholder">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                      <rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/>
                    </svg>
                    <p>Foto de Entrega</p>
                    <span>Tomada en destino</span>
                  </div>
                )}
                <div style={{ marginTop: 'var(--space-md)', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                  Timestamp: {selected.deliveryDate ? `${selected.deliveryDate} 14:32` : '—'}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
