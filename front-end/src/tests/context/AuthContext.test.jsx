import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { act, renderHook } from '@testing-library/react'
import { AuthProvider } from '../../context/AuthContext'
import { useAuth } from '../../hooks/useAuth'

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

describe('AuthContext', () => {
  beforeEach(() => {
    localStorage.clear()
    vi.unstubAllGlobals()
  })

  afterEach(() => {
    vi.unstubAllGlobals()
    localStorage.clear()
  })

  describe('login', () => {
    it('guarda usuario y token en estado y localStorage', async () => {
      vi.stubGlobal('fetch', vi.fn().mockResolvedValue(jsonResponse({
        access_token: 'test-token-123',
        user: {
          id: 1,
          name: 'Carlos',
          last_name: 'Operador',
          email: 'operador.carlos@awen.com',
          role: 'Warehouse Operator',
          branch: 'Sucursal Central',
          active: true,
        },
      })))

      const { result } = renderHook(() => useAuth(), { wrapper })

      let user
      await act(async () => {
        user = await result.current.login('operador.carlos@awen.com', '123456')
      })

      expect(user).toEqual(expect.objectContaining({
        id: 1,
        name: 'Carlos',
        role: 'Warehouse Operator',
      }))
      expect(result.current.user).toEqual(expect.objectContaining({ id: 1 }))

      const saved = JSON.parse(localStorage.getItem('awen_session'))
      expect(saved.user.id).toBe(1)
      expect(saved.token).toBe('test-token-123')
    })

    it('propaga el error y mantiene la sesion vacia', async () => {
      vi.stubGlobal('fetch', vi.fn().mockResolvedValue(jsonResponse(
        { message: 'Credenciales invalidas' },
        401,
      )))

      const { result } = renderHook(() => useAuth(), { wrapper })

      await act(async () => {
        await expect(result.current.login('bad@test.com', 'wrong'))
          .rejects.toThrow('Credenciales invalidas')
      })

      expect(result.current.user).toBeNull()
      expect(localStorage.getItem('awen_session')).toBeNull()
    })
  })

  describe('logout', () => {
    it('limpia usuario, token y localStorage', async () => {
      vi.stubGlobal('fetch', vi.fn().mockResolvedValue(jsonResponse({
        access_token: 'test-token',
        user: { id: 1, name: 'Carlos', role: 'Warehouse Operator', branch: 'Sucursal Central' },
      })))

      const { result } = renderHook(() => useAuth(), { wrapper })

      await act(async () => {
        await result.current.login('operador.carlos@awen.com', '123456')
      })
      expect(result.current.user).not.toBeNull()

      act(() => {
        result.current.logout()
      })

      expect(result.current.user).toBeNull()
      expect(localStorage.getItem('awen_session')).toBeNull()
    })
  })

  describe('canAccess', () => {
    it('devuelve false sin usuario', () => {
      const { result } = renderHook(() => useAuth(), { wrapper })
      expect(result.current.canAccess('/app/encomiendas')).toBe(false)
    })

    it('permite a Admin todas las rutas del sistema', () => {
      seedSession({ id: 1, name: 'Admin', role: 'Admin', branch: 'Sucursal Central' })
      const { result } = renderHook(() => useAuth(), { wrapper })

      expect(result.current.canAccess('/app/dashboard')).toBe(true)
      expect(result.current.canAccess('/app/encomiendas')).toBe(true)
      expect(result.current.canAccess('/app/logistica')).toBe(true)
      expect(result.current.canAccess('/app/reportes')).toBe(true)
      expect(result.current.canAccess('/app/usuarios')).toBe(true)
      expect(result.current.canAccess('/app/sucursales')).toBe(true)
    })

    it('limita las rutas de Warehouse Operator', () => {
      seedSession({ id: 2, name: 'Carlos', role: 'Warehouse Operator', branch: 'Sucursal Central' })
      const { result } = renderHook(() => useAuth(), { wrapper })

      expect(result.current.canAccess('/app/encomiendas')).toBe(true)
      expect(result.current.canAccess('/app/logistica')).toBe(true)
      expect(result.current.canAccess('/app/comprobantes')).toBe(true)
      expect(result.current.canAccess('/app/usuarios')).toBe(false)
      expect(result.current.canAccess('/app/sucursales')).toBe(false)
      expect(result.current.canAccess('/app/reportes')).toBe(false)
    })

    it('limita las rutas de Driver', () => {
      seedSession({ id: 4, name: 'Pedro', role: 'Driver', branch: 'Sucursal Central' })
      const { result } = renderHook(() => useAuth(), { wrapper })

      expect(result.current.canAccess('/app/mis-entregas')).toBe(true)
      expect(result.current.canAccess('/app/comprobantes')).toBe(true)
      expect(result.current.canAccess('/app/dashboard')).toBe(true)
      expect(result.current.canAccess('/app/encomiendas')).toBe(false)
      expect(result.current.canAccess('/app/logistica')).toBe(false)
    })

    it('limita las rutas de Client', () => {
      seedSession({ id: 6, name: 'Juan', role: 'Client', branch: null })
      const { result } = renderHook(() => useAuth(), { wrapper })

      expect(result.current.canAccess('/app/mis-encomiendas')).toBe(true)
      expect(result.current.canAccess('/app/perfil')).toBe(true)
      expect(result.current.canAccess('/app/encomiendas')).toBe(false)
      expect(result.current.canAccess('/app/logistica')).toBe(false)
    })
  })

  describe('persistencia de sesion', () => {
    it('restaura la sesion guardada al montar', () => {
      seedSession({
        id: 1,
        name: 'Carlos',
        role: 'Warehouse Operator',
        branch: 'Sucursal Central',
        active: true,
      })

      const { result } = renderHook(() => useAuth(), { wrapper })

      expect(result.current.user).toEqual(expect.objectContaining({
        id: 1,
        name: 'Carlos',
        role: 'Warehouse Operator',
      }))
    })

    it('ignora una sesion con JSON invalido', () => {
      localStorage.setItem('awen_session', 'invalid-json')

      const { result } = renderHook(() => useAuth(), { wrapper })

      expect(result.current.user).toBeNull()
    })

    it('ignora una sesion sin token', () => {
      localStorage.setItem('awen_session', JSON.stringify({ user: { id: 1, name: 'Carlos' } }))

      const { result } = renderHook(() => useAuth(), { wrapper })

      expect(result.current.user).toBeNull()
    })
  })
})
