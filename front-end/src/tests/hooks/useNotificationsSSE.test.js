import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { act, renderHook } from '@testing-library/react'
import { useNotificationsSSE } from '../../hooks/useNotificationsSSE'
import { setAuthToken } from '../../services/api'

let instances = []

class MockEventSource {
  constructor(url) {
    this.url = url
    this.close = vi.fn()
    this.onmessage = null
    this.onerror = null
    instances.push(this)
  }
}

function emitMessage(instance, payload) {
  act(() => {
    instance.onmessage({ data: JSON.stringify(payload) })
  })
}

describe('useNotificationsSSE', () => {
  beforeEach(() => {
    instances = []
    setAuthToken(null)
    vi.useFakeTimers()
    vi.stubGlobal('EventSource', MockEventSource)
  })

  afterEach(() => {
    vi.useRealTimers()
    vi.unstubAllGlobals()
    setAuthToken(null)
  })

  it('inicializa sin notificaciones y sin conexion si no hay token', () => {
    const { result } = renderHook(() => useNotificationsSSE())

    expect(result.current.notifications).toEqual([])
    expect(result.current.unreadCount).toBe(0)
    expect(instances).toHaveLength(0)
  })

  it('conecta al endpoint SSE con el token cuando existe sesion', () => {
    setAuthToken('tok-123')

    renderHook(() => useNotificationsSSE())

    expect(instances).toHaveLength(1)
    expect(instances[0].url).toBe('/api/v1/notifications/stream?token=tok-123')
  })

  it('agrega una notificacion entrante y aumenta el contador', () => {
    setAuthToken('tok-123')
    const { result } = renderHook(() => useNotificationsSSE())

    emitMessage(instances[0], {
      type: 'notification',
      data: { id: '1', message: 'Nueva encomienda', created_at: '2026-05-13T10:00:00Z' },
    })

    expect(result.current.notifications).toHaveLength(1)
    expect(result.current.notifications[0]).toEqual(expect.objectContaining({
      id: '1',
      text: 'Nueva encomienda',
      time: '2026-05-13T10:00:00Z',
      read: false,
    }))
    expect(result.current.unreadCount).toBe(1)
  })

  it('ignora mensajes de tipo ping', () => {
    setAuthToken('tok-123')
    const { result } = renderHook(() => useNotificationsSSE())

    emitMessage(instances[0], { type: 'ping' })

    expect(result.current.notifications).toHaveLength(0)
    expect(result.current.unreadCount).toBe(0)
  })

  it('ignora mensajes con JSON invalido', () => {
    setAuthToken('tok-123')
    const { result } = renderHook(() => useNotificationsSSE())

    act(() => {
      instances[0].onmessage({ data: 'not-json' })
    })

    expect(result.current.notifications).toHaveLength(0)
    expect(result.current.unreadCount).toBe(0)
  })

  it('marca una notificacion como leida', () => {
    setAuthToken('tok-123')
    const { result } = renderHook(() => useNotificationsSSE())

    emitMessage(instances[0], {
      type: 'notification',
      data: { id: '1', message: 'Nueva encomienda' },
    })

    act(() => {
      result.current.markRead('1')
    })

    expect(result.current.notifications[0].read).toBe(true)
    expect(result.current.unreadCount).toBe(0)
  })

  it('marca todas las notificaciones como leidas', () => {
    setAuthToken('tok-123')
    const { result } = renderHook(() => useNotificationsSSE())

    emitMessage(instances[0], { type: 'notification', data: { id: '1', message: 'Uno' } })
    emitMessage(instances[0], { type: 'notification', data: { id: '2', message: 'Dos' } })
    expect(result.current.unreadCount).toBe(2)

    act(() => {
      result.current.markAllRead()
    })

    expect(result.current.notifications.every(n => n.read)).toBe(true)
    expect(result.current.unreadCount).toBe(0)
  })

  it('reconecta tras un error de conexion', () => {
    setAuthToken('tok-123')
    renderHook(() => useNotificationsSSE())

    const first = instances[0]
    act(() => {
      first.onerror()
    })
    expect(first.close).toHaveBeenCalled()

    act(() => {
      vi.advanceTimersByTime(1000)
    })

    expect(instances).toHaveLength(2)
  })

  it('cierra la conexion al desmontar', () => {
    setAuthToken('tok-123')
    const { unmount } = renderHook(() => useNotificationsSSE())
    const instance = instances[0]

    unmount()

    expect(instance.close).toHaveBeenCalled()
  })
})
