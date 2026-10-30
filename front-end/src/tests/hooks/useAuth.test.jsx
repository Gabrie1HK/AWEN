import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { act, renderHook } from '@testing-library/react'
import { useAuth } from '../../hooks/useAuth'
import { AuthProvider } from '../../context/AuthContext'

const wrapper = ({ children }) => <AuthProvider>{children}</AuthProvider>

function jsonResponse(body, status = 200) {
  return {
    ok: status >= 200 && status < 300,
    status,
    headers: { get: () => 'application/json' },
    json: () => Promise.resolve(body),
    text: () => Promise.resolve(JSON.stringify(body)),
  }
}

function seedSession(user, token = 'saved-token') {
  localStorage.setItem('awen_session', JSON.stringify({ user, token }))
}

describe('useAuth', () => {
  beforeEach(() => {
    localStorage.clear()
    vi.unstubAllGlobals()
  })

  afterEach(() => {
    vi.unstubAllGlobals()
    localStorage.clear()
  })

  it('devuelve null fuera de AuthProvider', () => {
    const { result } = renderHook(() => useAuth())
    expect(result.current).toBeNull()
  })

  it('expone el usuario restaurado desde localStorage', () => {
    seedSession({ id: 2, name: 'Carlos', role: 'Warehouse Operator', branch: 'Sucursal Central' })

    const { result } = renderHook(() => useAuth(), { wrapper })

    expect(result.current).not.toBeNull()
    expect(result.current.user).toEqual(expect.objectContaining({
      id: 2,
      name: 'Carlos',
      role: 'Warehouse Operator',
    }))
    expect(typeof result.current.login).toBe('function')
    expect(typeof result.current.logout).toBe('function')
    expect(typeof result.current.canAccess).toBe('function')
  })

  it('login actualiza el usuario del contexto', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(jsonResponse({
      access_token: 'token-1',
      user: { id: 1, name: 'Admin', role: 'Admin', branch: 'Sucursal Central' },
    })))

    const { result } = renderHook(() => useAuth(), { wrapper })

    let logged
    await act(async () => {
      logged = await result.current.login('admin@awen.com', '123456')
    })

    expect(logged).toEqual(expect.objectContaining({ id: 1, role: 'Admin' }))
    expect(result.current.user).toEqual(expect.objectContaining({ id: 1, role: 'Admin' }))
  })

  it('logout limpia el usuario del contexto', () => {
    seedSession({ id: 2, name: 'Carlos', role: 'Warehouse Operator', branch: 'Sucursal Central' })

    const { result } = renderHook(() => useAuth(), { wrapper })
    expect(result.current.user).not.toBeNull()

    act(() => {
      result.current.logout()
    })

    expect(result.current.user).toBeNull()
  })

  it('canAccess refleja la matriz del rol', () => {
    seedSession({ id: 6, name: 'Juan', role: 'Client', branch: null })

    const { result } = renderHook(() => useAuth(), { wrapper })

    expect(result.current.canAccess('/app/mis-encomiendas')).toBe(true)
    expect(result.current.canAccess('/app/encomiendas')).toBe(false)
  })
})
