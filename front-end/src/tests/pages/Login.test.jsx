import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { AuthContext } from '../../context/constants'
import Login from '../../pages/Login'

function renderLogin({ user = null, login = vi.fn(), canAccess = () => true } = {}) {
  return render(
    <MemoryRouter>
      <AuthContext.Provider value={{ user, login, logout: vi.fn(), canAccess }}>
        <Login />
      </AuthContext.Provider>
    </MemoryRouter>
  )
}

describe('Login page', () => {
  it('renders form elements', () => {
    renderLogin()
    expect(screen.getByPlaceholderText('admin@awen.com')).toBeInTheDocument()
    expect(screen.getByText(/Iniciar Sesión/)).toBeInTheDocument()
    expect(screen.getByText('AWEN')).toBeInTheDocument()
  })

  it('shows error on failed login', async () => {
    const login = vi.fn().mockResolvedValue(null)
    renderLogin({ login })
    const inputs = screen.getAllByRole('textbox')
    fireEvent.change(inputs[0], { target: { value: 'bad@test.com' } })
    const passwords = document.querySelectorAll('input[type="password"]')
    fireEvent.change(passwords[0], { target: { value: 'wrong' } })
    fireEvent.click(screen.getByText(/Iniciar Sesión/))
    await waitFor(() => {
      expect(screen.getByText(/Credenciales inválidas/)).toBeInTheDocument()
    })
  })

  it('calls login with email and password', async () => {
    const login = vi.fn().mockResolvedValue({ id: 1, role: 'Admin', name: 'Admin' })
    renderLogin({ login })
    const inputs = screen.getAllByRole('textbox')
    fireEvent.change(inputs[0], { target: { value: 'admin@awen.com' } })
    const passwords = document.querySelectorAll('input[type="password"]')
    fireEvent.change(passwords[0], { target: { value: '123456' } })
    fireEvent.click(screen.getByText(/Iniciar Sesión/))
    await waitFor(() => {
      expect(login).toHaveBeenCalledWith('admin@awen.com', '123456')
    })
  })

  it('shows error message on thrown exception', async () => {
    const login = vi.fn().mockRejectedValue(new Error('Network error'))
    renderLogin({ login })
    const inputs = screen.getAllByRole('textbox')
    fireEvent.change(inputs[0], { target: { value: 'x@y.com' } })
    const passwords = document.querySelectorAll('input[type="password"]')
    fireEvent.change(passwords[0], { target: { value: 'pwd' } })
    fireEvent.click(screen.getByText(/Iniciar Sesión/))
    await waitFor(() => {
      expect(screen.getByText(/Error de conexión/)).toBeInTheDocument()
    })
  })

  it('shows back link to landing', () => {
    renderLogin()
    expect(screen.getByText('Volver al inicio')).toBeInTheDocument()
  })

  it('shows test credentials hint', () => {
    renderLogin()
    expect(screen.getByText(/Credenciales de prueba/)).toBeInTheDocument()
    expect(screen.getByText(/admin@awen.com \/ 123456/)).toBeInTheDocument()
  })
})
