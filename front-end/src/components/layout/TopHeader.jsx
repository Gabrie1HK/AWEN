import { useState, useRef, useEffect, useCallback } from 'react'
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
  '/app/mis-encomiendas': 'Mis Encomiendas',
  '/app/mis-entregas': 'Mis Entregas',
  '/app/perfil': 'Mi Perfil',
  '/tracking': 'Tracking de Envíos',
}

const MOCK_NOTIFICATIONS = [
  { id: 1, text: 'Encomienda AWEN-2026-0002 entregada con exito', time: 'Hace 5 min', read: false },
  { id: 2, text: 'Nueva encomienda registrada AWEN-2026-0007', time: 'Hace 30 min', read: false },
  { id: 3, text: 'Lote LOT-003 asignado a Conductor Ana', time: 'Hace 2 hs', read: false },
]

export default function TopHeader({ onMenuToggle }) {
  const { user, logout } = useAuth()
  const location = useLocation()
  const title = PAGE_TITLES[location.pathname] || 'AWEN'
  const [open, setOpen] = useState(false)
  const [notifications, setNotifications] = useState(MOCK_NOTIFICATIONS)
  const ref = useRef(null)

  const unread = notifications.filter(n => !n.read).length

  const handleClickOutside = useCallback((e) => {
    if (ref.current && !ref.current.contains(e.target)) setOpen(false)
  }, [])

  useEffect(() => {
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [handleClickOutside])

  const markAsRead = (id) => {
    setNotifications(prev => prev.map(n => n.id === id ? { ...n, read: true } : n))
  }

  const markAllRead = () => {
    setNotifications(prev => prev.map(n => ({ ...n, read: true })))
  }

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
        <div className="notification-wrapper" ref={ref}>
          <button className="notification-btn" onClick={() => setOpen(!open)}>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
            {unread > 0 && <span className="notification-badge">{unread}</span>}
          </button>
          {open && (
            <div className="notification-dropdown">
              <div className="notification-dropdown-header">
                <span>Notificaciones</span>
                {unread > 0 && <button className="notification-mark-all" onClick={markAllRead}>Marcar todo leido</button>}
              </div>
              <div className="notification-list">
                {notifications.length === 0 ? (
                  <div className="notification-empty">No hay notificaciones</div>
                ) : (
                  notifications.map(n => (
                    <div key={n.id} className={`notification-item ${n.read ? '' : 'unread'}`} onClick={() => markAsRead(n.id)}>
                      <div className="notification-dot" />
                      <div className="notification-content">
                        <p>{n.text}</p>
                        <span>{n.time}</span>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}
        </div>
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
