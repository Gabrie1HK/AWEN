const ROLE_COLORS = {
  Admin: { bg: 'rgba(239, 68, 68, 0.15)', color: '#ef4444' },
  'Warehouse Operator': { bg: 'rgba(59, 130, 246, 0.15)', color: '#3b82f6' },
  Driver: { bg: 'rgba(16, 185, 129, 0.15)', color: '#10b981' },
  Client: { bg: 'rgba(139, 92, 246, 0.15)', color: '#8b5cf6' },
}

export default function RoleBadge({ role }) {
  const colors = ROLE_COLORS[role] || { bg: 'rgba(156, 163, 175, 0.15)', color: '#9ca3af' }
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
      {role}
    </span>
  )
}
