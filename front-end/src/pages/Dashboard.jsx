import { dashboardKPIs, dailyShipments, deliveriesByBranch, recentActivity } from '../data/mockData'
import StatCard from '../components/ui/StatCard'
import DataTable from '../components/ui/DataTable'

const activityColumns = [
  { key: 'time', label: 'Hora' },
  { key: 'action', label: 'Actividad' },
  { key: 'user', label: 'Usuario' },
]

export default function Dashboard() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-xl)' }}>
      <div className="kpi-grid">
        <StatCard
          icon={<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/></svg>}
          value={dashboardKPIs.totalShipments}
          label="Envíos Totales Hoy"
          trend={12}
        />
        <StatCard
          icon={<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>}
          value={dashboardKPIs.inTransit}
          label="En Tránsito"
          color="#f59e0b"
        />
        <StatCard
          icon={<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polyline points="20 6 9 17 4 12"/></svg>}
          value={dashboardKPIs.delivered}
          label="Entregados Exitosamente"
          trend={8}
          color="#10b981"
        />
        <StatCard
          icon={<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>}
          value={dashboardKPIs.returned}
          label="Devueltos / Fallidos"
          trend={-5}
          color="#ef4444"
        />
      </div>

      <div className="dashboard-charts">
        <div className="chart-card">
          <h3>Envíos Últimos 7 Días</h3>
          <div className="chart-bars-horizontal">
            {dailyShipments.map(d => (
              <div key={d.day} className="chart-bar-col">
                <div className="chart-bar-value">{d.count}</div>
                <div className="chart-bar-track">
                  <div
                    className="chart-bar-fill"
                    style={{ height: `${(d.count / Math.max(...dailyShipments.map(x => x.count))) * 100}%` }}
                  />
                </div>
                <div className="chart-bar-label">{d.day.replace('May ', '')}</div>
              </div>
            ))}
          </div>
        </div>
        <div className="chart-card">
          <h3>Entregas por Sucursal</h3>
          <div className="chart-bars-horizontal">
            {deliveriesByBranch.map(d => {
              const maxVal = Math.max(...deliveriesByBranch.map(x => x.count))
              return (
                <div key={d.branch} className="chart-bar-col">
                  <div className="chart-bar-value">{d.count}</div>
                  <div className="chart-bar-track">
                    <div
                      className="chart-bar-fill fill-accent"
                      style={{ height: `${(d.count / maxVal) * 100}%` }}
                    />
                  </div>
                  <div className="chart-bar-label-sm">{d.branch}</div>
                </div>
              )
            })}
          </div>
        </div>
      </div>

      <div>
        <h3 style={{ marginBottom: 'var(--space-md)' }}>Actividad Reciente</h3>
        <DataTable columns={activityColumns} data={recentActivity} />
      </div>
    </div>
  )
}
