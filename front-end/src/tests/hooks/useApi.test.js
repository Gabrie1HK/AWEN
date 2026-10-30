import { describe, it, expect, vi, beforeEach } from 'vitest'
import { renderHook, act } from '@testing-library/react'
import { useApi } from '../../hooks/useApi'

globalThis.fetch = vi.fn()

describe('useApi', () => {
  beforeEach(() => {
    vi.resetAllMocks()
    globalThis.fetch = vi.fn()
  })

  describe('basic functionality', () => {
    it('should return initial data', () => {
      const { result } = renderHook(() => useApi('test-data'))
      expect(result.current).not.toBeNull()
      expect(result.current.data).toBe('test-data')
    })

    it('should allow setting data', () => {
      const { result } = renderHook(() => useApi())
      act(() => {
        result.current.setData('new data')
      })
      expect(result.current.data).toBe('new data')
    })

    it('should allow setting error', () => {
      const { result } = renderHook(() => useApi())
      act(() => {
        result.current.setError('test error')
      })
      expect(result.current.error).toBe('test error')
    })
  })

  describe('execute', () => {
    beforeEach(() => {
      vi.resetAllMocks()
      globalThis.fetch = vi.fn()
    })

    it('should make API call and return data', async () => {
      const mockData = { data: [{ id: 1, name: 'Test' }], total: 1 }
      globalThis.fetch.mockResolvedValue({
        ok: true,
        status: 200,
        headers: { get: () => 'application/json' },
        json: () => Promise.resolve(mockData),
        text: () => Promise.resolve(JSON.stringify(mockData))
      })

      const { result } = renderHook(() => useApi())
      
      let data
      await act(async () => {
        data = await result.current.execute(async () => {
          const res = await fetch('/api/v1/test')
          return res.json()
        })
      })

      expect(globalThis.fetch).toHaveBeenCalledWith('/api/v1/test')
      expect(data).toEqual(mockData)
    })

    it('should return parsed JSON even on 401 (fetch does not throw on HTTP errors)', async () => {
      globalThis.fetch.mockResolvedValue({
        ok: false,
        status: 401,
        headers: { get: () => 'application/json' },
        json: () => Promise.resolve({ message: 'No autenticado' }),
        text: () => Promise.resolve('{"message":"No autenticado"}')
      })

      const { result } = renderHook(() => useApi())
      
      const resultValue = await act(async () => {
        return await result.current.execute(async () => {
          const res = await fetch('/api/v1/test')
          return res.json()
        })
      })

      // fetch doesn't throw on HTTP errors, so execute returns the parsed response
      expect(resultValue).toEqual({ message: 'No autenticado' })
    })

    it('should handle 403 error', async () => {
      globalThis.fetch.mockResolvedValue({
        ok: false,
        status: 403,
        headers: { get: () => 'application/json' },
        json: () => Promise.resolve({ message: 'No tiene permisos para esta operacion' }),
        text: () => Promise.resolve('{"message":"No tiene permisos para esta operacion"}')
      })

      const { result } = renderHook(() => useApi())
      
      const resultValue = await act(async () => {
        return await result.current.execute(async () => {
          const res = await fetch('/api/v1/test')
          return res.json()
        })
      })

      expect(resultValue).toEqual({ message: 'No tiene permisos para esta operacion' })
    })

    it('should handle network error', async () => {
      globalThis.fetch.mockRejectedValue(new Error('Network error'))

      const { result } = renderHook(() => useApi())
      
      const resultValue = await act(async () => {
        return await result.current.execute(async () => {
          const res = await fetch('/api/v1/test')
          return res.json()
        })
      })

      // Network errors are caught by execute and return null
      expect(resultValue).toBeNull()
      expect(result.current.error).toBe('Network error')
    })

    it('should handle HTML response as error (request function throws)', async () => {
      globalThis.fetch.mockResolvedValue({
        ok: true,
        status: 200,
        headers: { get: () => 'text/html' },
        json: () => Promise.resolve({}),
        text: () => Promise.resolve('<html>Vercel SPA</html>')
      })

      const { result } = renderHook(() => useApi())
      
      // The actual api.js request function throws on HTML responses
      // We simulate that by having the apiCall throw
      const resultValue = await act(async () => {
        return await result.current.execute(async () => {
          const res = await fetch('/api/v1/test')
          const ct = res.headers.get('content-type') || ''
          if (ct.includes('text/html')) {
            throw new Error('Respuesta inesperada del servidor')
          }
          return res.json()
        })
      })

      expect(resultValue).toBeNull()
      expect(result.current.error).toBe('Respuesta inesperada del servidor')
    })
  })
})