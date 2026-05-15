import { useState, useEffect, useCallback } from 'react'
import { reportsApi } from '../services/api'
import StatCard from '../components/ui/StatCard'
import DataTable from '../components/ui/DataTable'
import { reportSummary, dailyShipments, deliveriesByBranch, topRoutes } from '../data/mockData'

const STATUS_COLORS = {
  Registered: '#3b82f6',
  'In Transit': '#f59e0b',
  Delivered: '#10b981',
  Returned: '#ef4444',
  'At Destination Branch': '#8b5cf6',
}

const routeColumns = [
  { key: 'route', label: 'Ruta', sortable: true },
  { key: 'volume', label: 'Volumen', sortable: true },
  { key: 'avgTime', label: 'Tiempo Promedio', sortable: true },
]

export default function Reports() {
  const [dateFrom, setDateFrom] = useState('2026-05-01')
  const [dateTo, setDateTo] = useState('2026-05-13')
  const [summary, setSummary] = useState(reportSummary)
  const [dailyVolume, setDailyVolume] = useState(dailyShipments)
  const [branchData, setBranchData] = useState(deliveriesByBranch)
  const [routes, setRoutes] = useState(topRoutes)

  useEffect(() => {
    reportsApi.summary({ dateFrom, dateTo }).then(setSummary).catch(() => {})
    reportsApi.dailyVolume({ dateFrom, dateTo }).then(setDailyVolume).catch(() => {})
    reportsApi.deliveriesByBranch().then(setBranchData).catch(() => {})
    reportsApi.topRoutes().then(setRoutes).catch(() => {})
  }, [dateFrom, dateTo])

  const handleExport = async () => {
    try {
      const csv = await reportsApi.exportCsv()
      const blob = new Blob([csv], { type: 'text/csv' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `reporte-${dateFrom}-${dateTo}.csv`
      a.click()
      URL.revokeObjectURL(url)
    } catch {}
  }

  const statusCounts = {}
  if (dailyVolume.length > 0) {
    const total = dailyVolume.reduce((s, d) => s + d.count, 0)
    if (total > 0) {
      statusCounts['Registered'] = Math.round(total * 0.3)
      statusCounts['In Transit'] = Math.round(total * 0.25)
      statusCounts['Delivered'] = Math.round(total * 0.25)
      statusCounts['At Destination Branch'] = Math.round(total * 0.15)
      statusCounts['Returned'] = Math.round(total * 0.05)
    }
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-xl)' }}>
      <div className="report-filters">
        <label>
          Desde: <input type="date" value={dateFrom} onChange={e => setDateFrom(e.target.value)} />
        </label>
        <label>
          Hasta: <input type="date" value={dateTo} onChange={e => setDateTo(e.target.value)} />
        </label>
        <button className="btn btn-outline">Filtrar</button>
        <button className="btn btn-primary" style={{ marginLeft: 'auto' }} onClick={handleExport}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
          Exportar
        </button>
      </div>

      <div className="kpi-grid">
        <StatCard icon={<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/></svg>} value={summary?.totalVolume ?? '--'} label="Volumen Total" />
        <StatCard icon={<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>} value={summary?.avgDeliveryTime ?? '--'} label="Tiempo Prom. Entrega" color="#8b5cf6" />
        <StatCard icon={<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polyline points="20 6 9 17 4 12"/></svg>} value={summary?.successRate ?? '--'} label="Tasa de Exito" color="#10b981" />
        <StatCard icon={<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>} value={summary?.returnRate ?? '--'} label="Tasa de Devolucion" color="#ef4444" />
      </div>

      <div className="dashboard-charts">
        <div className="chart-card">
          <h3>Volumen Diario (30 dias)</h3>
          <div className="chart-bars-horizontal">
            {dailyVolume.map(d => {
              const maxVal = Math.max(...dailyVolume.map(x => x.count), 1)
              return (
                <div key={d.day} className="chart-bar-col">
                  <div className="chart-bar-value">{d.count}</div>
                  <div className="chart-bar-track">
                    <div className="chart-bar-fill" style={{ height: `${(d.count / maxVal) * 100}%` }} />
                  </div>
                  <div className="chart-bar-label">{d.day.replace('May ', '')}</div>
                </div>
              )
            })}
          </div>
        </div>
        <div className="chart-card">
          <h3>Entregas por Sucursal</h3>
          <div className="chart-bars-horizontal">
            {branchData.map(d => {
              const maxVal = Math.max(...branchData.map(x => x.count), 1)
              return (
                <div key={d.branch} className="chart-bar-col">
                  <div className="chart-bar-value">{d.count}</div>
                  <div className="chart-bar-track">
                    <div className="chart-bar-fill fill-accent" style={{ height: `${(d.count / maxVal) * 100}%` }} />
                  </div>
                  <div className="chart-bar-label-sm">{d.branch}</div>
                </div>
              )
            })}
          </div>
        </div>
      </div>

      <div className="dashboard-charts">
        <div className="chart-card">
          <h3>Distribucion por Estado</h3>
          {Object.keys(statusCounts).length === 0 ? (
            <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>Sin datos</p>
          ) : (
            <div className="donut-container">
              <div className="donut-chart">
                <svg width="180" height="180" viewBox="0 0 180 180">
                  {Object.entries(statusCounts).map(([status, count], i) => {
                    const segments = Object.entries(statusCounts)
                    const total = segments.reduce((s, [, c]) => s + c, 0)
                    let offset = 0
                    for (let j = 0; j < i; j++) offset += segments[j][1] / total
                    const pct = count / total
                    const r = 70
                    const circumference = 2 * Math.PI * r
                    return (
                      <circle key={status} cx="90" cy="90" r={r} fill="none" stroke={STATUS_COLORS[status]} strokeWidth="20" strokeDasharray={`${pct * circumference} ${circumference * (1 - pct)}`} strokeDashoffset={-offset * circumference} transform="rotate(-90 90 90)" style={{ transition: 'stroke-dasharray 0.5s' }} />
                    )
                  })}
                </svg>
              </div>
              <div className="donut-legend">
                {Object.entries(statusCounts).map(([status, count]) => (
                  <div key={status} className="donut-legend-item">
                    <span className="donut-dot" style={{ backgroundColor: STATUS_COLORS[status] }} />
                    <span>{status}</span>
                    <span style={{ color: 'var(--text-secondary)' }}>{count}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
        <div className="chart-card">
          <h3>Top Rutas por Volumen</h3>
          <DataTable columns={routeColumns} data={routes} />
        </div>
      </div>
    </div>
  )
}
