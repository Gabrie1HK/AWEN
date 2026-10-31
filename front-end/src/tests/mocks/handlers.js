import { http, HttpResponse } from 'msw'

// Datos de prueba (fixtures)
const mockUser = {
  id: 1,
  name: 'Carlos',
  last_name: 'Operador',
  ci: 'V-23456789',
  email: 'operador.carlos@awen.com',
  role: 'Warehouse Operator',
  branch: 'Sucursal Central',
  phone: '+58 412 123 4567',
  active: true,
  lastLogin: '2026-05-13 07:15',
  avatar: null
}

const mockDriver = {
  id: 4,
  name: 'Pedro',
  last_name: 'Conductor',
  ci: 'V-34567890',
  email: 'conductor.pedro@awen.com',
  role: 'Driver',
  branch: 'Sucursal Central',
  phone: '+58 414 987 6543',
  active: true,
  lastLogin: '2026-05-13 06:00',
  avatar: null
}

const mockAdmin = {
  id: 1,
  name: 'Admin',
  last_name: 'Principal',
  ci: 'V-12345678',
  email: 'admin@awen.com',
  role: 'Admin',
  branch: 'Sucursal Central',
  phone: '+58 212 212 3456',
  active: true,
  lastLogin: '2026-05-12 09:30',
  avatar: null
}

const mockClient = {
  id: 6,
  name: 'Juan',
  last_name: 'Cliente',
  ci: 'V-67890123',
  email: 'juan@email.com',
  role: 'Client',
  branch: null,
  phone: '+58 412 789 0123',
  address: 'Calle 60 123, Merida',
  active: true,
  lastLogin: '2026-05-10 14:00',
  avatar: null
}

const mockParcels = [
  {
    id: 'ENV-001',
    guide: 'AWEN-2026-0001',
    sender: 'TechStore CA',
    senderId: 'J-12345678',
    senderPhone: '+56 9 1234 5678',
    recipient: 'Roberto Garcia',
    recipientId: '12.345.678-9',
    recipientPhone: '+56 9 8765 4321',
    recipientAddress: 'Av. Universidad 742, Caracas',
    originBranch: 'Sucursal Central',
    destinationBranch: 'Sucursal Norte',
    originAddress: 'Valencia, Carabobo',
    originLat: 10.1620,
    originLng: -68.0077,
    destinationAddress: 'Maracaibo, Zulia',
    destinationLat: 10.6545,
    destinationLng: -71.6506,
    weight: 2.5,
    dimensions: '30x20x15 cm',
    declaredValue: 150000,
    description: 'Notebook y accesorios',
    status: 'IN_TRANSIT',
    createdAt: '2026-05-10',
    updatedAt: '2026-05-13',
    qrData: 'AWEN-2026-0001',
    barcode: '|||AWEN-2026-0001|||'
  },
  {
    id: 'ENV-004',
    guide: 'AWEN-2026-0004',
    sender: 'ElectroHogar SA',
    senderId: 'J-45678901-0',
    senderPhone: '+58 424 456 7890',
    recipient: 'Laura Martinez',
    recipientId: 'V-45678901',
    recipientPhone: '+58 416 654 3210',
    recipientAddress: 'Av. Las Delicias 234, Maracay',
    originBranch: 'Sucursal Este',
    destinationBranch: 'Sucursal Costa',
    originAddress: 'Valencia, Carabobo',
    originLat: 10.1620,
    originLng: -68.0077,
    destinationAddress: 'Maracay, Aragua',
    destinationLat: 10.2469,
    destinationLng: -67.5958,
    weight: 8.0,
    dimensions: '60x40x35 cm',
    declaredValue: 320000,
    description: 'Aspiradora robot',
    status: 'AT_DESTINATION_BRANCH',
    createdAt: '2026-05-09',
    updatedAt: '2026-05-13',
    qrData: 'AWEN-2026-0004',
    barcode: '|||AWEN-2026-0004|||'
  }
]

const mockDeliveries = [
  {
    id: 'DEL-001',
    guide: 'AWEN-2026-0002',
    recipient: 'Carmen Flores',
    driver: 'Conductor Ana',
    deliveryDate: '2026-05-12',
    podType: 'SIGNATURE',
    status: 'COMPLETED',
    signatureData: null,
    photoUrl: null,
    gps: '8.3519, -62.6414'
  },
  {
    id: 'DEL-002',
    guide: 'AWEN-2026-0001',
    recipient: 'Roberto Garcia',
    driver: 'Conductor Pedro',
    deliveryDate: null,
    podType: 'PHOTO',
    status: 'PENDING',
    signatureData: null,
    photoUrl: null,
    gps: '10.6312, -71.6404'
  }
]

const mockBatches = [
  {
    id: 'LOT-001',
    parcels: ['ENV-001', 'ENV-006'],
    status: 'ASSIGNED',
    vehicle: 'ABC-123',
    driver: 'Conductor Pedro',
    driverId: 4,
    parcelCount: 2
  },
  {
    id: 'LOT-003',
    parcels: ['ENV-003', 'ENV-007'],
    status: 'PENDING',
    vehicle: null,
    driver: null,
    driverId: null,
    parcelCount: 2
  }
]

const mockVehicles = [
  { id: 1, plate: 'ABC-123', model: 'Foton Aumark', capacity: '1500 kg', driver: 'Conductor Pedro' },
  { id: 2, plate: 'XYZ-789', model: 'JMC Carrying', capacity: '1200 kg', driver: 'Conductor Ana' }
]

const mockUsers = [
  mockAdmin,
  mockDriver,
  mockClient,
  {
    id: 3,
    name: 'Maria',
    last_name: 'Operador',
    ci: 'V-98765432',
    email: 'operador.maria@awen.com',
    role: 'Warehouse Operator',
    branch: 'Sucursal Norte',
    phone: '+58 416 765 4321',
    active: true,
    lastLogin: '2026-05-12 22:40',
    avatar: null
  }
]

const mockKpis = {
  totalShipments: 150,
  inTransit: 45,
  delivered: 95,
  returned: 10,
  totalShipmentsTrend: 5,
  inTransitTrend: -2,
  deliveredTrend: 8,
  returnedTrend: -1
}

const mockDashboard = {
  kpis: mockKpis,
  dailyShipments: [
    { day: 'Lun', count: 20 },
    { day: 'Mar', count: 25 },
    { day: 'Mié', count: 30 },
    { day: 'Jue', count: 28 },
    { day: 'Vie', count: 35 },
    { day: 'Sáb', count: 15 },
    { day: 'Dom', count: 5 }
  ],
  deliveriesByBranch: [
    { branch: 'Sucursal Central', count: 80 },
    { branch: 'Sucursal Norte', count: 45 },
    { branch: 'Sucursal Sur', count: 25 }
  ],
  recentActivity: [
    { time: '10:30', action: 'Encomienda creada', user: 'Carlos Operador' },
    { time: '10:15', action: 'Entrega completada', user: 'Pedro Conductor' },
    { time: '09:45', action: 'Lote asignado', user: 'Maria Operador' }
  ]
}

// Helper para obtener usuario por token (simulado)
const getUserByToken = (token) => {
  if (!token) return null
  if (token.includes('operator')) return mockUser
  if (token.includes('driver')) return mockDriver
  if (token.includes('admin')) return mockAdmin
  if (token.includes('client')) return mockClient
  return null
}

export const handlers = [
  // Auth
  http.post('/api/v1/auth/login', async ({ request }) => {
    const body = await request.json()
    const { email, password } = body
    
    let user = null
    if (email === 'operador.carlos@awen.com' && password === '123456') user = { ...mockUser, token: 'operator-token-123' }
    else if (email === 'conductor.pedro@awen.com' && password === '123456') user = { ...mockDriver, token: 'driver-token-123' }
    else if (email === 'admin@awen.com' && password === '123456') user = { ...mockAdmin, token: 'admin-token-123' }
    else if (email === 'juan@email.com' && password === '123456') user = { ...mockClient, token: 'client-token-123' }
    
    if (!user) {
      return HttpResponse.json({ message: 'Credenciales invalidas' }, { status: 401 })
    }
    
    return HttpResponse.json({
      access_token: user.token,
      token_type: 'bearer',
      user: { ...user, token: undefined }
    })
  }),

  http.get('/api/v1/auth/me', ({ request }) => {
    const auth = request.headers.get('Authorization')
    if (!auth) return HttpResponse.json({ message: 'No autenticado' }, { status: 401 })
    const token = auth.replace('Bearer ', '')
    const user = getUserByToken(token)
    if (!user) return HttpResponse.json({ message: 'Token invalido' }, { status: 401 })
    return HttpResponse.json(user)
  }),

  // Health
  http.get('/api/v1/health', () => HttpResponse.json({ status: 'ok' })),

  // Parcels
  http.get('/api/v1/parcels', ({ request }) => {
    const url = new URL(request.url)
    const search = url.searchParams.get('search')
    const status = url.searchParams.get('status')
    const originBranch = url.searchParams.get('originBranch')
    const destinationBranch = url.searchParams.get('destinationBranch')
    const page = parseInt(url.searchParams.get('page') || '1')
    const pageSize = parseInt(url.searchParams.get('pageSize') || '20')
    
    let items = [...mockParcels]
    
    if (search) {
      const lowered = search.toLowerCase()
      items = items.filter(p => 
        p.guide.toLowerCase().includes(lowered) ||
        p.sender.toLowerCase().includes(lowered) ||
        p.recipient.toLowerCase().includes(lowered)
      )
    }
    if (status) items = items.filter(p => p.status === status)
    if (originBranch) items = items.filter(p => p.originBranch === originBranch)
    if (destinationBranch) items = items.filter(p => p.destinationBranch === destinationBranch)
    
    const start = (page - 1) * pageSize
    const end = start + pageSize
    const paginated = items.slice(start, end)
    
    return HttpResponse.json({
      data: paginated,
      total: items.length,
      page,
      pageSize,
      totalPages: Math.ceil(items.length / pageSize)
    })
  }),

  http.get('/api/v1/parcels/:id', ({ params }) => {
    const parcel = mockParcels.find(p => p.id === params.id)
    if (!parcel) return HttpResponse.json({ message: 'Encomienda no encontrada' }, { status: 404 })
    return HttpResponse.json(parcel)
  }),

  http.post('/api/v1/parcels', async ({ request }) => {
    const body = await request.json()
    const newParcel = {
      id: `ENV-${String(mockParcels.length + 1).padStart(3, '0')}`,
      guide: `AWEN-2026-${String(mockParcels.length + 1).padStart(4, '0')}`,
      status: 'REGISTERED',
      createdAt: new Date().toISOString().split('T')[0],
      updatedAt: new Date().toISOString().split('T')[0],
      qrData: `AWEN-2026-${String(mockParcels.length + 1).padStart(4, '0')}`,
      barcode: `|||AWEN-2026-${String(mockParcels.length + 1).padStart(4, '0')}|||`,
      ...body
    }
    mockParcels.push(newParcel)
    return HttpResponse.json(newParcel, { status: 201 })
  }),

  http.patch('/api/v1/parcels/:id', async ({ params, request }) => {
    const index = mockParcels.findIndex(p => p.id === params.id)
    if (index === -1) return HttpResponse.json({ message: 'Encomienda no encontrada' }, { status: 404 })
    const body = await request.json()
    mockParcels[index] = { ...mockParcels[index], ...body, updatedAt: new Date().toISOString().split('T')[0] }
    return HttpResponse.json(mockParcels[index])
  }),

  http.post('/api/v1/parcels/:id/status', async ({ params, request }) => {
    const index = mockParcels.findIndex(p => p.id === params.id)
    if (index === -1) return HttpResponse.json({ message: 'Encomienda no encontrada' }, { status: 404 })
    const body = await request.json()
    mockParcels[index] = { ...mockParcels[index], status: body.status, updatedAt: new Date().toISOString().split('T')[0] }
    return HttpResponse.json(mockParcels[index])
  }),

  http.post('/api/v1/parcels/:id/cancel', ({ params }) => {
    const index = mockParcels.findIndex(p => p.id === params.id)
    if (index === -1) return HttpResponse.json({ message: 'Encomienda no encontrada' }, { status: 404 })
    mockParcels[index] = { ...mockParcels[index], status: 'RETURNED', updatedAt: new Date().toISOString().split('T')[0] }
    return HttpResponse.json(mockParcels[index])
  }),

  http.get('/api/v1/parcels/:guide/tracking', ({ params }) => {
    const parcel = mockParcels.find(p => p.guide === params.guide)
    if (!parcel) return HttpResponse.json({ message: 'Encomienda no encontrada' }, { status: 404 })
    return HttpResponse.json([
      { step: 'REGISTERED', date: '2026-05-10', time: '14:30', location: 'Sucursal Central', operator: 'Carlos Operador', completed: true },
      { step: 'PICKED_UP', date: '2026-05-10', time: '16:00', location: 'Sucursal Central', operator: 'Pedro Conductor', completed: true },
      { step: 'IN_TRANSIT', date: '2026-05-11', time: '08:00', location: 'Autopista Regional del Centro', operator: 'Pedro Conductor', completed: true }
    ])
  }),

  // Deliveries
  http.get('/api/v1/deliveries', ({ request }) => {
    const url = new URL(request.url)
    const page = parseInt(url.searchParams.get('page') || '1')
    const pageSize = parseInt(url.searchParams.get('pageSize') || '20')
    
    const start = (page - 1) * pageSize
    const end = start + pageSize
    const paginated = mockDeliveries.slice(start, end)
    
    return HttpResponse.json({
      data: paginated,
      total: mockDeliveries.length,
      page,
      pageSize,
      totalPages: Math.ceil(mockDeliveries.length / pageSize)
    })
  }),

  http.get('/api/v1/deliveries/:id', ({ params }) => {
    const delivery = mockDeliveries.find(d => d.id === params.id)
    if (!delivery) return HttpResponse.json({ message: 'Entrega no encontrada' }, { status: 404 })
    return HttpResponse.json(delivery)
  }),

  http.patch('/api/v1/deliveries/:id', async ({ params, request }) => {
    const index = mockDeliveries.findIndex(d => d.id === params.id)
    if (index === -1) return HttpResponse.json({ message: 'Entrega no encontrada' }, { status: 404 })
    const body = await request.json()
    mockDeliveries[index] = { ...mockDeliveries[index], ...body }
    return HttpResponse.json(mockDeliveries[index])
  }),

  http.post('/api/v1/deliveries/:id/pod', async ({ params, request }) => {
    const index = mockDeliveries.findIndex(d => d.id === params.id)
    if (index === -1) return HttpResponse.json({ message: 'Entrega no encontrada' }, { status: 404 })
    const body = await request.json()
    mockDeliveries[index] = { 
      ...mockDeliveries[index], 
      podType: body.podType,
      signatureData: body.signatureData,
      photoUrl: body.photoUrl,
      gps: body.gps,
      deliveryDate: body.deliveryDate || new Date().toISOString().split('T')[0],
      status: 'COMPLETED'
    }
    return HttpResponse.json(mockDeliveries[index])
  }),

  http.post('/api/v1/deliveries/:id/upload', async () => {
    // Simular upload de archivo
    return HttpResponse.json({
      filename: 'test.pdf',
      url: '/uploads/test.pdf',
      size: 1024
    })
  }),

  // Logistics
  http.get('/api/v1/logistics/batches', ({ request }) => {
    const url = new URL(request.url)
    const page = parseInt(url.searchParams.get('page') || '1')
    const pageSize = parseInt(url.searchParams.get('pageSize') || '20')
    
    const start = (page - 1) * pageSize
    const end = start + pageSize
    const paginated = mockBatches.slice(start, end)
    
    return HttpResponse.json({
      data: paginated,
      total: mockBatches.length,
      page,
      pageSize,
      totalPages: Math.ceil(mockBatches.length / pageSize)
    })
  }),

  http.get('/api/v1/logistics/batches/:id', ({ params }) => {
    const batch = mockBatches.find(b => b.id === params.id)
    if (!batch) return HttpResponse.json({ message: 'Lote no encontrado' }, { status: 404 })
    return HttpResponse.json(batch)
  }),

  http.post('/api/v1/logistics/batches', async ({ request }) => {
    const body = await request.json()
    const newBatch = {
      id: `LOT-${String(mockBatches.length + 1).padStart(3, '0')}`,
      status: body.status || 'PENDING',
      parcels: body.parcels || [],
      ...body
    }
    mockBatches.push(newBatch)
    return HttpResponse.json(newBatch, { status: 201 })
  }),

  http.patch('/api/v1/logistics/batches/:id', async ({ params, request }) => {
    const index = mockBatches.findIndex(b => b.id === params.id)
    if (index === -1) return HttpResponse.json({ message: 'Lote no encontrado' }, { status: 404 })
    const body = await request.json()
    mockBatches[index] = { ...mockBatches[index], ...body }
    return HttpResponse.json(mockBatches[index])
  }),

  http.post('/api/v1/logistics/batches/:id/assign', async ({ params, request }) => {
    const index = mockBatches.findIndex(b => b.id === params.id)
    if (index === -1) return HttpResponse.json({ message: 'Lote no encontrado' }, { status: 404 })
    const body = await request.json()
    mockBatches[index] = { 
      ...mockBatches[index], 
      vehicle: body.vehicle,
      driver: body.driver,
      driverId: body.driverId,
      status: body.status || 'ASSIGNED',
      parcels: body.parcels
    }
    return HttpResponse.json(mockBatches[index])
  }),

  http.get('/api/v1/logistics/vehicles', ({ request }) => {
    const url = new URL(request.url)
    const page = parseInt(url.searchParams.get('page') || '1')
    const pageSize = parseInt(url.searchParams.get('pageSize') || '20')
    
    const start = (page - 1) * pageSize
    const end = start + pageSize
    const paginated = mockVehicles.slice(start, end)
    
    return HttpResponse.json({
      data: paginated,
      total: mockVehicles.length,
      page,
      pageSize,
      totalPages: Math.ceil(mockVehicles.length / pageSize)
    })
  }),

  http.post('/api/v1/logistics/vehicles', async ({ request }) => {
    const body = await request.json()
    const newVehicle = { id: mockVehicles.length + 1, ...body }
    mockVehicles.push(newVehicle)
    return HttpResponse.json(newVehicle, { status: 201 })
  }),

  // Users
  http.get('/api/v1/users', ({ request }) => {
    const url = new URL(request.url)
    const search = url.searchParams.get('search')
    const role = url.searchParams.get('role')
    const page = parseInt(url.searchParams.get('page') || '1')
    const pageSize = parseInt(url.searchParams.get('pageSize') || '20')
    
    let items = [...mockUsers]
    
    if (search) {
      const lowered = search.toLowerCase()
      items = items.filter(u => 
        u.name.toLowerCase().includes(lowered) ||
        u.last_name?.toLowerCase().includes(lowered) ||
        u.email.toLowerCase().includes(lowered)
      )
    }
    if (role) items = items.filter(u => u.role === role)
    
    const start = (page - 1) * pageSize
    const end = start + pageSize
    const paginated = items.slice(start, end)
    
    return HttpResponse.json({
      data: paginated,
      total: items.length,
      page,
      pageSize,
      totalPages: Math.ceil(items.length / pageSize)
    })
  }),

  http.get('/api/v1/users/me', ({ request }) => {
    const auth = request.headers.get('Authorization')
    const token = auth?.replace('Bearer ', '')
    const user = getUserByToken(token)
    if (!user) return HttpResponse.json({ message: 'Token invalido' }, { status: 401 })
    return HttpResponse.json(user)
  }),

  http.patch('/api/v1/users/me', async ({ request }) => {
    const auth = request.headers.get('Authorization')
    const token = auth?.replace('Bearer ', '')
    const user = getUserByToken(token)
    if (!user) return HttpResponse.json({ message: 'Token invalido' }, { status: 401 })
    const body = await request.json()
    Object.assign(user, body)
    return HttpResponse.json(user)
  }),

  http.get('/api/v1/users/:id', ({ params }) => {
    const user = mockUsers.find(u => u.id === parseInt(params.id))
    if (!user) return HttpResponse.json({ message: 'Usuario no encontrado' }, { status: 404 })
    return HttpResponse.json(user)
  }),

  // Reports
  http.get('/api/v1/reports/kpis', () => {
    return HttpResponse.json(mockKpis)
  }),

  http.get('/api/v1/reports/daily-volume', () => {
    return HttpResponse.json([
      { day: '2026-05-10', count: 25 },
      { day: '2026-05-11', count: 30 },
      { day: '2026-05-12', count: 28 }
    ])
  }),

  http.get('/api/v1/reports/deliveries-by-branch', () => 
    HttpResponse.json([
      { branch: 'Sucursal Central', count: 80 },
      { branch: 'Sucursal Norte', count: 45 },
      { branch: 'Sucursal Sur', count: 25 }
    ])
  ),

  http.get('/api/v1/reports/activity', () => 
    HttpResponse.json([
      { time: '10:30', action: 'Encomienda creada', user: 'Carlos Operador' },
      { time: '10:15', action: 'Entrega completada', user: 'Pedro Conductor' }
    ])
  ),

  http.get('/api/v1/reports/summary', () => 
    HttpResponse.json({
      totalParcels: 150,
      totalDeliveries: 120,
      totalUsers: 10,
      totalBranches: 5
    })
  ),

  // Dashboard
  http.get('/api/v1/dashboard', () => 
    HttpResponse.json(mockDashboard)
  ),

  // Tracking público
  http.get('/api/v1/tracking/:guide', ({ params }) => {
    const parcel = mockParcels.find(p => p.guide === params.guide)
    if (!parcel) return HttpResponse.json({ guide: params.guide, parcel: null, history: null })
    return HttpResponse.json({
      guide: parcel.guide,
      parcel: { ...parcel },
      history: [
        { step: 'REGISTERED', date: '2026-05-10', time: '14:30', location: 'Sucursal Central' },
        { step: 'IN_TRANSIT', date: '2026-05-11', time: '08:00', location: 'En tránsito' }
      ],
      route: null,
      publicNotes: [],
      deliveryEvidence: null
    })
  }),

  // Maps
  http.get('/api/v1/maps/route', ({ request }) => {
    const url = new URL(request.url)
    const originLat = parseFloat(url.searchParams.get('origin_lat'))
    const originLng = parseFloat(url.searchParams.get('origin_lng'))
    const destLat = parseFloat(url.searchParams.get('destination_lat'))
    const destLng = parseFloat(url.searchParams.get('destination_lng'))
    
    return HttpResponse.json({
      route: [[originLat, originLng], [destLat, destLng]],
      distanceKm: 150.5
    })
  }),

  // Notifications
  http.get('/api/v1/notifications', () => 
    HttpResponse.json({
      data: [
        { id: '1', text: 'Nueva encomienda asignada', read: false, createdAt: '2026-05-13T10:00:00Z' },
        { id: '2', text: 'Entrega completada', read: true, createdAt: '2026-05-12T15:00:00Z' }
      ],
      total: 2,
      page: 1,
      pageSize: 20,
      totalPages: 1
    })
  ),

  http.patch('/api/v1/notifications/:id/read', () => 
    HttpResponse.json({ ok: true })
  ),

  http.patch('/api/v1/notifications/read-all', () => 
    HttpResponse.json({ ok: true })
  )
]