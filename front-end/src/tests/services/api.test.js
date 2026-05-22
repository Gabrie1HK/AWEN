import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setAuthToken, getAuthToken, authApi, parcelsApi, branchesApi, usersApi, logisticsApi, deliveriesApi, dashboardApi, reportsApi, trackingApi, notificationsApi, requestForm } from '../../services/api'

const mockFetch = vi.fn()
global.fetch = mockFetch

function mockJsonResponse(body, status = 200) {
  return Promise.resolve({
    ok: status >= 200 && status < 300,
    status,
    headers: { get: () => 'application/json' },
    json: () => Promise.resolve(body),
    text: () => Promise.resolve(JSON.stringify(body)),
  })
}

function mockTextResponse(body, status = 200) {
  return Promise.resolve({
    ok: status >= 200 && status < 300,
    status,
    headers: { get: () => 'text/csv' },
    json: () => { throw new Error('not json') },
    text: () => Promise.resolve(body),
  })
}

describe('auth token', () => {
  it('stores and retrieves token', () => {
    setAuthToken('test-token')
    expect(getAuthToken()).toBe('test-token')
  })

  it('allows null token', () => {
    setAuthToken(null)
    expect(getAuthToken()).toBeNull()
  })
})

describe('authApi', () => {
  beforeEach(() => {
    mockFetch.mockReset()
    setAuthToken(null)
  })

  it('login sends POST with email and password', async () => {
    mockFetch.mockResolvedValue(mockJsonResponse({ access_token: 'abc', user: { id: 1 } }))
    const result = await authApi.login('admin@awen.com', '123456')
    expect(mockFetch).toHaveBeenCalledWith(
      '/api/v1/auth/login',
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({ email: 'admin@awen.com', password: '123456' }),
      })
    )
    expect(result.access_token).toBe('abc')
  })

  it('login throws on error', async () => {
    mockFetch.mockResolvedValue(mockJsonResponse({ message: 'Bad credentials' }, 401))
    await expect(authApi.login('bad@test.com', 'x')).rejects.toThrow()
  })

  it('me sends Authorization header when token set', async () => {
    setAuthToken('tok-123')
    mockFetch.mockResolvedValue(mockJsonResponse({ id: 1 }))
    await authApi.me()
    expect(mockFetch).toHaveBeenCalledWith(
      '/api/v1/auth/me',
      expect.objectContaining({
        headers: expect.objectContaining({ Authorization: 'Bearer tok-123' }),
      })
    )
  })
})

describe('parcelsApi', () => {
  beforeEach(() => { mockFetch.mockReset(); setAuthToken('t') })

  it('list builds query params', async () => {
    mockFetch.mockResolvedValue(mockJsonResponse({ data: [], total: 0 }))
    await parcelsApi.list({ page: 2, pageSize: 10, search: 'test', status: 'Delivered' })
    const url = mockFetch.mock.calls[0][0]
    expect(url).toContain('page=2')
    expect(url).toContain('pageSize=10')
    expect(url).toContain('search=test')
    expect(url).toContain('status=Delivered')
  })

  it('create sends POST', async () => {
    mockFetch.mockResolvedValue(mockJsonResponse({ id: 'ENV-001' }))
    const r = await parcelsApi.create({ sender: 'Test' })
    expect(mockFetch.mock.calls[0][1].method).toBe('POST')
    expect(r.id).toBe('ENV-001')
  })

  it('cancel sends POST', async () => {
    mockFetch.mockResolvedValue(mockJsonResponse({ status: 'Returned' }))
    const r = await parcelsApi.cancel('ENV-001')
    expect(mockFetch.mock.calls[0][1].method).toBe('POST')
    expect(r.status).toBe('Returned')
  })
})

describe('branchesApi', () => {
  beforeEach(() => { mockFetch.mockReset(); setAuthToken('t') })

  it('list with search param', async () => {
    mockFetch.mockResolvedValue(mockJsonResponse({ data: [] }))
    await branchesApi.list({ search: 'Central' })
    expect(mockFetch.mock.calls[0][0]).toContain('search=Central')
  })

  it('delete sends DELETE', async () => {
    mockFetch.mockResolvedValue(mockJsonResponse({ status: 'ok' }))
    await branchesApi.delete(1)
    expect(mockFetch.mock.calls[0][1].method).toBe('DELETE')
  })
})

describe('usersApi', () => {
  beforeEach(() => { mockFetch.mockReset(); setAuthToken('t') })

  it('list with role filter', async () => {
    mockFetch.mockResolvedValue(mockJsonResponse({ data: [] }))
    await usersApi.list({ role: 'Admin' })
    expect(mockFetch.mock.calls[0][0]).toContain('role=Admin')
  })

  it('me calls users/me', async () => {
    mockFetch.mockResolvedValue(mockJsonResponse({ id: 1 }))
    const r = await usersApi.me()
    expect(mockFetch.mock.calls[0][0]).toContain('/users/me')
    expect(r.id).toBe(1)
  })
})

describe('logisticsApi', () => {
  beforeEach(() => { mockFetch.mockReset(); setAuthToken('t') })

  it('listBatches builds URL', async () => {
    mockFetch.mockResolvedValue(mockJsonResponse({ data: [] }))
    await logisticsApi.listBatches({ page: 1 })
    expect(mockFetch.mock.calls[0][0]).toContain('/logistics/batches')
    expect(mockFetch.mock.calls[0][0]).toContain('page=1')
  })

  it('assignBatch sends POST', async () => {
    mockFetch.mockResolvedValue(mockJsonResponse({ status: 'Assigned' }))
    await logisticsApi.assignBatch('LOT-001', { driver: 'Pedro' })
    expect(mockFetch.mock.calls[0][1].method).toBe('POST')
  })
})

describe('deliveriesApi', () => {
  beforeEach(() => { mockFetch.mockReset(); setAuthToken('t') })

  it('addPod sends POST', async () => {
    mockFetch.mockResolvedValue(mockJsonResponse({ status: 'Completed' }))
    await deliveriesApi.addPod('D-1', { podType: 'Photo' })
    expect(mockFetch.mock.calls[0][1].method).toBe('POST')
  })

  it('uploadEvidence uses FormData', async () => {
    mockFetch.mockResolvedValue(mockJsonResponse({ url: '/uploads/test.jpg' }))
    const file = new File(['test'], 'test.jpg', { type: 'image/jpeg' })
    const r = await deliveriesApi.uploadEvidence('D-1', file)
    expect(mockFetch.mock.calls[0][0]).toContain('/deliveries/D-1/upload')
    expect(mockFetch.mock.calls[0][1].body).toBeInstanceOf(FormData)
    expect(r.url).toBe('/uploads/test.jpg')
  })
})

describe('dashboardApi', () => {
  beforeEach(() => { mockFetch.mockReset(); setAuthToken('t') })

  it('get fetches dashboard endpoint', async () => {
    mockFetch.mockResolvedValue(mockJsonResponse({ kpis: {} }))
    const r = await dashboardApi.get()
    expect(mockFetch.mock.calls[0][0]).toContain('/dashboard')
    expect(r.kpis).toBeDefined()
  })
})

describe('reportsApi', () => {
  beforeEach(() => { mockFetch.mockReset(); setAuthToken('t') })

  it('kpis with date params', async () => {
    mockFetch.mockResolvedValue(mockJsonResponse({}))
    await reportsApi.kpis({ dateFrom: '2026-01-01', dateTo: '2026-12-31' })
    const url = mockFetch.mock.calls[0][0]
    expect(url).toContain('date_from=2026-01-01')
    expect(url).toContain('date_to=2026-12-31')
  })

  it('exportCsv returns text', async () => {
    mockFetch.mockResolvedValue(mockTextResponse('route,volume\nCentral,10'))
    const r = await reportsApi.exportCsv()
    expect(typeof r).toBe('string')
    expect(r).toContain('Central')
  })
})

describe('trackingApi', () => {
  beforeEach(() => { mockFetch.mockReset() })

  it('publicTrack fetches without auth', async () => {
    mockFetch.mockResolvedValue(mockJsonResponse({ guide: 'AWEN-001' }))
    const r = await trackingApi.publicTrack('AWEN-001')
    expect(mockFetch.mock.calls[0][0]).toContain('/tracking/AWEN-001')
    expect(r.guide).toBe('AWEN-001')
  })
})

describe('requestForm', () => {
  beforeEach(() => { mockFetch.mockReset(); setAuthToken('t') })

  it('sends POST with FormData', async () => {
    mockFetch.mockResolvedValue(mockJsonResponse({ url: '/uploads/test.pdf' }))
    const fd = new FormData()
    fd.append('file', 'test')
    const result = await deliveriesApi.uploadEvidence('DEL-001', fd.get('file'))
    expect(mockFetch.mock.calls[0][1].method).toBe('POST')
    expect(mockFetch.mock.calls[0][0]).toContain('/deliveries/DEL-001/upload')
  })

  it('throws on HTML response', async () => {
    mockFetch.mockResolvedValue({
      ok: true,
      status: 200,
      headers: { get: () => 'text/html' },
      json: () => Promise.resolve({}),
      text: () => Promise.resolve('<html>Vercel SPA</html>'),
    })
    const fd = new FormData()
    fd.append('file', 'test')
    await expect(deliveriesApi.uploadEvidence('DEL-001', fd.get('file'))).rejects.toThrow('Respuesta inesperada del servidor')
  })

  it('throws on network error', async () => {
    mockFetch.mockRejectedValue(new Error('Network error'))
    const fd = new FormData()
    fd.append('file', 'test')
    await expect(deliveriesApi.uploadEvidence('DEL-001', fd.get('file'))).rejects.toThrow()
  })
})

describe('notificationsApi', () => {
  beforeEach(() => { mockFetch.mockReset(); setAuthToken('t') })

  it('list fetches notifications', async () => {
    mockFetch.mockResolvedValue(mockJsonResponse({ data: [] }))
    await notificationsApi.list()
    expect(mockFetch.mock.calls[0][0]).toContain('/notifications')
  })

  it('markRead sends PATCH', async () => {
    mockFetch.mockResolvedValue(mockJsonResponse({ ok: true }))
    await notificationsApi.markRead('n1')
    expect(mockFetch.mock.calls[0][1].method).toBe('PATCH')
    expect(mockFetch.mock.calls[0][0]).toContain('/notifications/n1/read')
  })
})
