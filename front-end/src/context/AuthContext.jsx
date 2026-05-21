import { useState, useCallback, useEffect } from 'react'
import { AuthContext } from './constants'
import { authApi, setAuthToken, getAuthToken } from '../services/api'

const ROUTE_PERMISSIONS = {
  Admin: ['/app/dashboard', '/app/encomiendas', '/app/logistica', '/app/comprobantes', '/app/reportes', '/app/usuarios', '/app/sucursales'],
  'Warehouse Operator': ['/app/dashboard', '/app/encomiendas', '/app/logistica', '/app/comprobantes'],
  Driver: ['/app/dashboard', '/app/mis-entregas', '/app/comprobantes'],
  Client: ['/app/mis-encomiendas', '/app/perfil'],
}

const MOCK_USERS = {
  'admin@awen.com': { id: 1, name: 'Admin Principal', email: 'admin@awen.com', role: 'Admin', branch: 'Sucursal Central', phone: '+58 212 212 3456', address: 'Av. Libertador 1234, Caracas', avatar: null },
  'operador.carlos@awen.com': { id: 2, name: 'Operador Carlos', email: 'operador.carlos@awen.com', role: 'Warehouse Operator', branch: 'Sucursal Central', phone: '+58 412 123 4567', avatar: null },
  'conductor.pedro@awen.com': { id: 4, name: 'Conductor Pedro', email: 'conductor.pedro@awen.com', role: 'Driver', branch: 'Sucursal Central', phone: '+58 414 987 6543', avatar: null },
  'juan@email.com': { id: 6, name: 'Cliente Juan', email: 'juan@email.com', role: 'Client', branch: '-', phone: '+58 412 789 0123', address: 'Calle 60 123, Merida', avatar: null },
}

function loadSession() {
  try {
    const saved = localStorage.getItem('awen_session')
    if (saved) {
      const { user: savedUser, token } = JSON.parse(saved)
      if (savedUser && token) {
        setAuthToken(token)
        return savedUser
      }
    }
  } catch {}
  return null
}

function saveSession(user, token) {
  try {
    localStorage.setItem('awen_session', JSON.stringify({ user, token: token || getAuthToken() }))
  } catch {}
}

function clearSession() {
  try { localStorage.removeItem('awen_session') } catch {}
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(loadSession)

  const login = useCallback(async (email, password) => {
    try {
      const data = await authApi.login(email, password)
      setAuthToken(data.access_token)
      const userData = { ...data.user, avatar: null }
      setUser(userData)
      saveSession(userData, data.access_token)
      return userData
    } catch {
      const found = MOCK_USERS[email]
      if (found && password === '123456') {
        setAuthToken('mock-token')
        setUser(found)
        saveSession(found, 'mock-token')
        return found
      }
      return null
    }
  }, [])

  const logout = useCallback(() => {
    setAuthToken(null)
    setUser(null)
    clearSession()
  }, [])

  const canAccess = useCallback((path) => {
    if (!user) return false
    const allowed = ROUTE_PERMISSIONS[user.role] || []
    return allowed.includes(path)
  }, [user])

  useEffect(() => {
    if (user) {
      saveSession(user, null)
    } else {
      clearSession()
    }
  }, [user])

  return (
    <AuthContext.Provider value={{ user, login, logout, canAccess }}>
      {children}
    </AuthContext.Provider>
  )
}
