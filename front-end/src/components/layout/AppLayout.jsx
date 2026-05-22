import { useState } from 'react'
import { Outlet, Navigate } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import ErrorBoundary from '../ui/ErrorBoundary'
import Sidebar from './Sidebar'
import TopHeader from './TopHeader'
import './layout.css'

function MinimalFallback({ label }) {
  return (
    <div style={{ padding: 12, fontSize: '0.75rem', color: 'var(--text-muted)', textAlign: 'center', borderBottom: '1px solid var(--border-medium)' }}>
      Error al cargar {label}
    </div>
  )
}

export default function AppLayout() {
  const { user } = useAuth()
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)

  if (!user) return <Navigate to="/login" replace />

  return (
    <div className="app-layout app-shell-light">
      <ErrorBoundary fallback={<MinimalFallback label="menu lateral" />}>
        <Sidebar
          collapsed={sidebarCollapsed}
          open={sidebarOpen}
          onToggle={() => setSidebarCollapsed(c => !c)}
          onClose={() => setSidebarOpen(false)}
        />
      </ErrorBoundary>
      <div className="main-area">
        <ErrorBoundary fallback={<MinimalFallback label="encabezado" />}>
          <TopHeader onMenuToggle={() => setSidebarOpen(true)} />
        </ErrorBoundary>
        <main className="page-content">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
