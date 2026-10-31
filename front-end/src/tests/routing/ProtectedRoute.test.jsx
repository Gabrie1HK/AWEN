import { describe, it, expect, beforeEach, afterEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import { MemoryRouter, Routes, Route } from 'react-router-dom'
import { ProtectedRoute } from '../../App'
import { AuthProvider } from '../../context/AuthContext'
import { mockUsers } from '../fixtures/users'

function seedSession(user, token = 'session-token') {
  localStorage.setItem('awen_session', JSON.stringify({ user, token }))
}

function renderAt(path, user = null) {
  if (user) seedSession(user)

  return render(
    <MemoryRouter initialEntries={[path]}>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<div>Pantalla Login</div>} />
          <Route path="/app/dashboard" element={<div>Pantalla Dashboard</div>} />
          <Route
            path="/app/encomiendas"
            element={<ProtectedRoute path="/app/encomiendas"><div>Pantalla Encomiendas</div></ProtectedRoute>}
          />
          <Route
            path="/app/usuarios"
            element={<ProtectedRoute path="/app/usuarios"><div>Pantalla Usuarios</div></ProtectedRoute>}
          />
          <Route
            path="/app/mis-entregas"
            element={<ProtectedRoute path="/app/mis-entregas"><div>Pantalla Mis Entregas</div></ProtectedRoute>}
          />
        </Routes>
      </AuthProvider>
    </MemoryRouter>,
  )
}

describe('Routing protegido', () => {
  beforeEach(() => {
    localStorage.clear()
  })

  afterEach(() => {
    localStorage.clear()
  })

  it('redirige a login cuando no hay sesion', () => {
    renderAt('/app/encomiendas')

    expect(screen.getByText('Pantalla Login')).toBeInTheDocument()
    expect(screen.queryByText('Pantalla Encomiendas')).not.toBeInTheDocument()
  })

  it('permite a Warehouse Operator una ruta autorizada', () => {
    renderAt('/app/encomiendas', mockUsers.operator)

    expect(screen.getByText('Pantalla Encomiendas')).toBeInTheDocument()
    expect(screen.queryByText('Pantalla Login')).not.toBeInTheDocument()
  })

  it('redirige al dashboard si el rol no tiene permiso', () => {
    renderAt('/app/usuarios', mockUsers.operator)

    expect(screen.getByText('Pantalla Dashboard')).toBeInTheDocument()
    expect(screen.queryByText('Pantalla Usuarios')).not.toBeInTheDocument()
  })

  it('permite a Driver acceder a mis entregas', () => {
    renderAt('/app/mis-entregas', mockUsers.driver)

    expect(screen.getByText('Pantalla Mis Entregas')).toBeInTheDocument()
  })

  it('redirige a Admin fuera de una ruta inexistente para su rol', () => {
    renderAt('/app/mis-entregas', mockUsers.admin)

    expect(screen.getByText('Pantalla Dashboard')).toBeInTheDocument()
    expect(screen.queryByText('Pantalla Mis Entregas')).not.toBeInTheDocument()
  })
})
