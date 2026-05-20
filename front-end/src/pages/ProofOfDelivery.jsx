import { useState, useEffect, useRef, useCallback } from 'react'
import { deliveries as mockDeliveries } from '../data/mockData'
import { deliveriesApi } from '../services/api'
import StatusBadge from '../components/ui/StatusBadge'
import DataTable from '../components/ui/DataTable'

const columns = (onView) => [
  { key: 'guide', label: 'Guia #', sortable: true },
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

const PAGE_SIZE = 10

export default function ProofOfDelivery() {
  const [selected, setSelected] = useState(null)
  const [deliveryList, setDeliveryList] = useState(mockDeliveries)
  const [totalDeliveries, setTotalDeliveries] = useState(mockDeliveries.length)
  const [page, setPage] = useState(1)
  const [uploading, setUploading] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [photoUrl, setPhotoUrl] = useState('')
  const [gps, setGps] = useState('')
  const [msg, setMsg] = useState('')
  const [error, setError] = useState('')
  const fileRef = useRef(null)

  const fetchDeliveries = useCallback((p) => {
    deliveriesApi.list({ page: p, pageSize: PAGE_SIZE })
      .then(res => {
        setDeliveryList(res.data || res)
        setTotalDeliveries(res.total || res.length || 0)
      })
      .catch(() => {})
  }, [])

  useEffect(() => {
    fetchDeliveries(page)
  }, [page, fetchDeliveries])

  const handleFileUpload = async () => {
    const file = fileRef.current?.files?.[0]
    if (!file) return
    setUploading(true)
    setError('')
    try {
      const result = await deliveriesApi.uploadEvidence(selected.id, file)
      setPhotoUrl(result.url)
      setMsg('Archivo subido correctamente')
      setTimeout(() => setMsg(''), 3000)
    } catch {
      setError('Error al subir archivo. Intente de nuevo.')
    }
    setUploading(false)
  }

  const handleSubmitPod = async () => {
    setSubmitting(true)
    setError('')
    try {
      const data = {
        podType: selected.podType,
        photoUrl: photoUrl || selected.photoUrl || null,
        gps: gps || selected.gps || null,
        deliveryDate: new Date().toISOString().slice(0, 10),
      }
      await deliveriesApi.addPod(selected.id, data)
      setMsg('Comprobante registrado exitosamente')
      setDeliveryList(prev => prev.map(d =>
        d.id === selected.id
          ? { ...d, status: 'Completed', deliveryDate: data.deliveryDate, photoUrl: photoUrl, gps: gps }
          : d
      ))
      setSelected(prev => ({ ...prev, status: 'Completed', deliveryDate: data.deliveryDate, photoUrl: photoUrl, gps: gps }))
      setTimeout(() => setMsg(''), 3000)
    } catch {
      setError('Error al registrar comprobante. Intente de nuevo.')
    }
    setSubmitting(false)
  }

  const isPending = selected?.status === 'Pending'

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-lg)' }}>
      <DataTable
        columns={columns(d => { setSelected(d); setPhotoUrl(''); setGps(''); setMsg(''); setError('') })}
        data={deliveryList}
        pageSize={PAGE_SIZE}
        totalItems={totalDeliveries}
        currentPage={page}
        onPageChange={setPage}
      />

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
                  <h4>Informacion</h4>
                  <span className="detail-meta">Guia: {selected.guide}</span>
                  <span className="detail-meta">Destinatario: {selected.recipient}</span>
                  <span className="detail-meta">Conductor: {selected.driver}</span>
                  <span className="detail-meta">Fecha: {selected.deliveryDate || 'Pendiente'}</span>
                  <span className="detail-meta">Tipo: {selected.podType}</span>
                  <span className="detail-meta">GPS: {selected.gps || gps || '—'}</span>
                  <div style={{ marginTop: 8 }}>
                    <StatusBadge status={selected.status} />
                  </div>
                </div>
                {isPending && (
                  <div className="detail-section" style={{ marginTop: 'var(--space-md)' }}>
                    <h4>Registrar Entrega</h4>
                    <div className="form-field" style={{ marginBottom: 8 }}>
                      <label>GPS (opcional)</label>
                      <input type="text" value={gps} onChange={e => setGps(e.target.value)} placeholder="Ej: 10.4806, -66.9036" />
                    </div>
                    <input ref={fileRef} type="file" accept="image/*" style={{ display: 'none' }} onChange={handleFileUpload} />
                    <button className="btn btn-outline" style={{ width: '100%', marginBottom: 8 }} disabled={uploading} onClick={() => fileRef.current?.click()}>
                      {uploading ? 'Subiendo...' : (photoUrl ? 'Reemplazar Foto' : 'Subir Foto')}
                    </button>
                    {msg && <p style={{ color: 'var(--status-delivered)', fontSize: '0.813rem', marginBottom: 8 }}>{msg}</p>}
                    {error && <p style={{ color: 'var(--status-returned)', fontSize: '0.813rem', marginBottom: 8 }}>{error}</p>}
                    <button className="btn btn-primary" style={{ width: '100%' }} disabled={submitting || !photoUrl} onClick={handleSubmitPod}>
                      {submitting ? 'Registrando...' : 'Registrar Comprobante'}
                    </button>
                  </div>
                )}
              </div>
              <div className="pod-evidence">
                <h4>Evidencia</h4>
                {(photoUrl || selected.photoUrl) ? (
                  <div className="pod-image-wrapper">
                    <img src={photoUrl || selected.photoUrl} alt="Evidencia de entrega" className="pod-image" />
                  </div>
                ) : selected.podType === 'Signature' ? (
                  <div className="pod-placeholder signature-placeholder">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                      <path d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/>
                    </svg>
                    <p>Imagen de Firma Digital</p>
                    <span>Capturada en dispositivo movil</span>
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
                  Timestamp: {selected.deliveryDate ? `${selected.deliveryDate} 14:32` : (new Date().toISOString().slice(0, 10) + ' — pendiente')}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}