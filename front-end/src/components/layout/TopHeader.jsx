import { useAuth } from '../../hooks/useAuth'
import { useLocation } from 'react-router-dom'

const PAGE_TITLES = {
  '/app/dashboard': 'Dashboard',
  '/app/encomiendas': 'Encomiendas',
  '/app/logistica': 'Logística y Rutas',
  '/app/comprobantes': 'Comprobantes de Entrega',
  '/app/reportes': 'Reportes y Analítica',
  '/app/usuarios': 'Gestión de Usuarios',
  '/app/sucursales': 'Gestión de Sucursales',
  '/tracking': 'Tracking de Envíos',
}

export default function TopHeader({ onMenuToggle }) {
  const { user, logout } = useAuth()
  const location = useLocation()
  const title = PAGE_TITLES[location.pathname] || 'AWEN'

  const initials = user?.name?.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase() || '??'

  return (
    <header className="top-header">
      <div className="top-header-left">
        <button className="mobile-menu-btn notification-btn" onClick={onMenuToggle}>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
        <h1 className="top-header-page-title">{title}</h1>
      </div>
      <div className="top-header-right">
        <button className="notification-btn">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
          </svg>
          <span className="notification-badge">3</span>
        </button>
        <div className="user-menu">
          <div className="user-avatar">{initials}</div>
          <div className="user-info">
            <span className="user-name">{user?.name}</span>
            <span className="user-role">{user?.role}</span>
          </div>
        </div>
        <button className="user-logout" onClick={logout}>Salir</button>
      </div>
    </header>
  )
}
