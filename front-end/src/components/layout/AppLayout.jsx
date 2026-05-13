import { useState } from 'react'
import { Outlet, Navigate } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import Sidebar from './Sidebar'
import TopHeader from './TopHeader'
import './layout.css'

export default function AppLayout() {
  const { user } = useAuth()
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)

  if (!user) return <Navigate to="/login" replace />

  return (
    <div className="app-layout">
      <Sidebar
        collapsed={sidebarCollapsed}
        open={sidebarOpen}
        onToggle={() => setSidebarCollapsed(c => !c)}
        onClose={() => setSidebarOpen(false)}
      />
      <div className="main-area">
        <TopHeader onMenuToggle={() => setSidebarOpen(true)} />
        <main className="page-content">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
