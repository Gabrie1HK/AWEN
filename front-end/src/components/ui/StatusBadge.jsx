const STATUS_COLORS = {
  Registered: { bg: 'rgba(59, 130, 246, 0.15)', color: '#3b82f6' },
  'In Transit': { bg: 'rgba(245, 158, 11, 0.15)', color: '#f59e0b' },
  'At Destination Branch': { bg: 'rgba(139, 92, 246, 0.15)', color: '#8b5cf6' },
  'Out for Delivery': { bg: 'rgba(14, 165, 233, 0.15)', color: '#0ea5e9' },
  Delivered: { bg: 'rgba(16, 185, 129, 0.15)', color: '#10b981' },
  Returned: { bg: 'rgba(239, 68, 68, 0.15)', color: '#ef4444' },
}

export default function StatusBadge({ status }) {
  const colors = STATUS_COLORS[status] || { bg: 'rgba(156, 163, 175, 0.15)', color: '#9ca3af' }
  return (
    <span style={{
      display: 'inline-flex',
      alignItems: 'center',
      padding: '2px 10px',
      borderRadius: 9999,
      fontSize: '0.75rem',
      fontWeight: 600,
      backgroundColor: colors.bg,
      color: colors.color,
      whiteSpace: 'nowrap',
    }}>
      {status}
    </span>
  )
}
