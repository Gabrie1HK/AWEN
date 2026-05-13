import { useState } from 'react'
import { AuthContext } from './constants'

const ROUTE_PERMISSIONS = {
  Admin: ['/app/dashboard', '/app/encomiendas', '/app/logistica', '/app/comprobantes', '/app/reportes', '/app/usuarios', '/app/sucursales'],
  'Warehouse Operator': ['/app/dashboard', '/app/encomiendas', '/app/logistica', '/app/comprobantes'],
  Driver: ['/app/dashboard', '/app/comprobantes'],
  Client: ['/tracking'],
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)

  const login = (email, password) => {
    const mockUser = {
      'admin@awen.cl': { id: 1, name: 'Admin Principal', email: 'admin@awen.cl', role: 'Admin', branch: 'Sucursal Central', avatar: null },
      'operador.carlos@awen.cl': { id: 2, name: 'Operador Carlos', email: 'operador.carlos@awen.cl', role: 'Warehouse Operator', branch: 'Sucursal Central', avatar: null },
      'conductor.pedro@awen.cl': { id: 4, name: 'Conductor Pedro', email: 'conductor.pedro@awen.cl', role: 'Driver', branch: 'Sucursal Central', avatar: null },
      'juan@email.com': { id: 6, name: 'Cliente Juan', email: 'juan@email.com', role: 'Client', branch: '-', avatar: null },
    }
    const found = mockUser[email]
    if (found && password === '123456') {
      setUser(found)
      return found
    }
    return null
  }

  const logout = () => setUser(null)

  const canAccess = (path) => {
    if (!user) return false
    const allowed = ROUTE_PERMISSIONS[user.role] || []
    return allowed.includes(path)
  }

  return (
    <AuthContext.Provider value={{ user, login, logout, canAccess }}>
      {children}
    </AuthContext.Provider>
  )
}


