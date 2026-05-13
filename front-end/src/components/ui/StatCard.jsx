export default function StatCard({ icon, value, label, trend, color }) {
  return (
    <div className="stat-card">
      <div className="stat-card-icon" style={{ backgroundColor: color ? `${color}20` : 'var(--accent-muted)' }}>
        {icon}
      </div>
      <div className="stat-card-info">
        <span className="stat-card-value">{value}</span>
        <span className="stat-card-label">{label}</span>
        {trend && (
          <span className={`stat-card-trend ${trend > 0 ? 'up' : 'down'}`}>
            {trend > 0 ? '↑' : '↓'} {Math.abs(trend)}%
          </span>
        )}
      </div>
    </div>
  )
}
