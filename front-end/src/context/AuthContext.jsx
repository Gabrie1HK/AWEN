import { useState, useCallback, useEffect } from 'react'
import { AuthContext } from './constants'
import { authApi, setAuthToken, getAuthToken } from '../services/api'

const ROUTE_PERMISSIONS = {
  Admin: ['/app/dashboard', '/app/encomiendas', '/app/logistica', '/app/comprobantes', '/app/reportes', '/app/usuarios', '/app/sucursales'],
  'Warehouse Operator': ['/app/dashboard', '/app/encomiendas', '/app/logistica', '/app/comprobantes'],
  Driver: ['/app/dashboard', '/app/mis-entregas', '/app/comprobantes'],
  Client: ['/app/mis-encomiendas', '/app/perfil'],
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
    const data = await authApi.login(email, password)
    setAuthToken(data.access_token)
    const userData = { ...data.user, avatar: null }
    setUser(userData)
    saveSession(userData, data.access_token)
    return userData
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
