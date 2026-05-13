export default function ConfirmModal({ open, title, message, confirmLabel = 'Confirmar', cancelLabel = 'Cancelar', variant = 'danger', onConfirm, onCancel }) {
  if (!open) return null

  return (
    <div className="modal-overlay" onClick={onCancel}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <h3>{title}</h3>
        <p>{message}</p>
        <div className="modal-actions">
          <button className="btn btn-outline" onClick={onCancel}>{cancelLabel}</button>
          <button
            className="btn"
            style={{
              backgroundColor: variant === 'danger' ? '#ef4444' : 'var(--accent-primary)',
              color: 'white',
            }}
            onClick={onConfirm}
          >
            {confirmLabel}
          </button>
        </div>
      </div>
    </div>
  )
}
