const BASE_URL = '/api/v1'

let token = null

export function setAuthToken(newToken) {
  token = newToken
}

export function getAuthToken() {
  return token
}

async function request(path, options = {}) {
  const headers = { 'Content-Type': 'application/json', ...options.headers }
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }
  const res = await fetch(`${BASE_URL}${path}`, { ...options, headers })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ message: res.statusText }))
    throw new Error(err.detail?.message || err.message || 'Error de red')
  }
  const ct = res.headers.get('content-type') || ''
  if (ct.includes('application/json')) {
    return res.json()
  }
  return res.text()
}

export const authApi = {
  login: (email, password) =>
    request('/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) }),
  me: () => request('/auth/me'),
}

export const parcelsApi = {
  list: (params = {}) => {
    const q = new URLSearchParams()
    if (params.search) q.set('search', params.search)
    if (params.status) q.set('status', params.status)
    if (params.page) q.set('page', params.page)
    if (params.pageSize) q.set('pageSize', params.pageSize)
    return request(`/parcels?${q}`)
  },
  get: (id) => request(`/parcels/${id}`),
  create: (data) => request('/parcels', { method: 'POST', body: JSON.stringify(data) }),
  update: (id, data) => request(`/parcels/${id}`, { method: 'PATCH', body: JSON.stringify(data) }),
  updateStatus: (id, status) => request(`/parcels/${id}/status`, { method: 'POST', body: JSON.stringify({ status }) }),
  cancel: (id) => request(`/parcels/${id}/cancel`, { method: 'POST' }),
  tracking: (guide) => request(`/parcels/${guide}/tracking`),
  myParcels: () => request('/parcels/my-parcels'),
}

export const trackingApi = {
  publicTrack: (guide) => request(`/tracking/${guide}`),
}

export const logisticsApi = {
  listBatches: (params = {}) => {
    const q = new URLSearchParams()
    if (params.page) q.set('page', params.page)
    if (params.pageSize) q.set('pageSize', params.pageSize)
    return request(`/logistics/batches?${q}`)
  },
  getBatch: (id) => request(`/logistics/batches/${id}`),
  createBatch: (data) => request('/logistics/batches', { method: 'POST', body: JSON.stringify(data) }),
  updateBatch: (id, data) => request(`/logistics/batches/${id}`, { method: 'PATCH', body: JSON.stringify(data) }),
  assignBatch: (id, data) => request(`/logistics/batches/${id}/assign`, { method: 'POST', body: JSON.stringify(data) }),
  listVehicles: (params = {}) => {
    const q = new URLSearchParams()
    if (params.page) q.set('page', params.page)
    if (params.pageSize) q.set('pageSize', params.pageSize)
    return request(`/logistics/vehicles?${q}`)
  },
  createVehicle: (data) => request('/logistics/vehicles', { method: 'POST', body: JSON.stringify(data) }),
}

export const dashboardApi = {
  get: () => request('/dashboard'),
}

export const reportsApi = {
  kpis: (params = {}) => {
    const q = new URLSearchParams()
    if (params.dateFrom) q.set('date_from', params.dateFrom)
    if (params.dateTo) q.set('date_to', params.dateTo)
    return request(`/reports/kpis?${q}`)
  },
  dailyVolume: (params = {}) => {
    const q = new URLSearchParams()
    if (params.dateFrom) q.set('date_from', params.dateFrom)
    if (params.dateTo) q.set('date_to', params.dateTo)
    return request(`/reports/daily-volume?${q}`)
  },
  deliveriesByBranch: () => request('/reports/deliveries-by-branch'),
  summary: () => request('/reports/summary'),
  topRoutes: () => request('/reports/top-routes'),
  activity: () => request('/reports/activity'),
  exportCsv: (format = 'csv') => request(`/reports/export?format=${format}`),
}

export const usersApi = {
  list: (params = {}) => {
    const q = new URLSearchParams()
    if (params.search) q.set('search', params.search)
    if (params.role) q.set('role', params.role)
    if (params.page) q.set('page', params.page)
    if (params.pageSize) q.set('pageSize', params.pageSize)
    return request(`/users?${q}`)
  },
  get: (id) => request(`/users/${id}`),
  create: (data) => request('/users', { method: 'POST', body: JSON.stringify(data) }),
  update: (id, data) => request(`/users/${id}`, { method: 'PATCH', body: JSON.stringify(data) }),
  delete: (id) => request(`/users/${id}`, { method: 'DELETE' }),
  me: () => request('/users/me'),
  updateMe: (data) => request('/users/me', { method: 'PATCH', body: JSON.stringify(data) }),
}

export const branchesApi = {
  list: (params = {}) => {
    const q = new URLSearchParams()
    if (params.search) q.set('search', params.search)
    if (params.page) q.set('page', params.page)
    if (params.pageSize) q.set('pageSize', params.pageSize)
    return request(`/branches?${q}`)
  },
  get: (id) => request(`/branches/${id}`),
  create: (data) => request('/branches', { method: 'POST', body: JSON.stringify(data) }),
  update: (id, data) => request(`/branches/${id}`, { method: 'PATCH', body: JSON.stringify(data) }),
  delete: (id) => request(`/branches/${id}`, { method: 'DELETE' }),
}

async function requestForm(path, formData) {
  const headers = {}
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }
  const res = await fetch(`${BASE_URL}${path}`, { method: 'POST', headers, body: formData })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ message: res.statusText }))
    throw new Error(err.detail?.message || err.message || 'Error de red')
  }
  return res.json()
}

export const deliveriesApi = {
  list: (params = {}) => {
    const q = new URLSearchParams()
    if (params.page) q.set('page', params.page)
    if (params.pageSize) q.set('pageSize', params.pageSize)
    return request(`/deliveries?${q}`)
  },
  get: (id) => request(`/deliveries/${id}`),
  update: (id, data) => request(`/deliveries/${id}`, { method: 'PATCH', body: JSON.stringify(data) }),
  addPod: (id, data) => request(`/deliveries/${id}/pod`, { method: 'POST', body: JSON.stringify(data) }),
  uploadEvidence: (id, file) => {
    const fd = new FormData()
    fd.append('file', file)
    return requestForm(`/deliveries/${id}/upload`, fd)
  },
}

export const notificationsApi = {
  list: () => request('/notifications'),
  markRead: (id) => request(`/notifications/${id}/read`, { method: 'PATCH' }),
  markAllRead: () => request('/notifications/read-all', { method: 'PATCH' }),
}
