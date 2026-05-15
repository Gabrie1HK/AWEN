import { useState, useCallback } from 'react'
import { AuthContext } from './constants'
import { authApi, setAuthToken } from '../services/api'

const ROUTE_PERMISSIONS = {
  Admin: ['/app/dashboard', '/app/encomiendas', '/app/logistica', '/app/comprobantes', '/app/reportes', '/app/usuarios', '/app/sucursales'],
  'Warehouse Operator': ['/app/dashboard', '/app/encomiendas', '/app/logistica', '/app/comprobantes'],
  Driver: ['/app/dashboard', '/app/comprobantes'],
  Client: ['/tracking'],
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)

  const login = useCallback(async (email, password) => {
    try {
      const data = await authApi.login(email, password)
      setAuthToken(data.access_token)
      const userData = { ...data.user, avatar: null }
      setUser(userData)
      return userData
    } catch {
      return null
    }
  }, [])

  const logout = useCallback(() => {
    setAuthToken(null)
    setUser(null)
  }, [])

  const canAccess = useCallback((path) => {
    if (!user) return false
    const allowed = ROUTE_PERMISSIONS[user.role] || []
    return allowed.includes(path)
  }, [user])

  return (
    <AuthContext.Provider value={{ user, login, logout, canAccess }}>
      {children}
    </AuthContext.Provider>
  )
}


