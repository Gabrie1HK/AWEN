import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import ClientProfile from '../../pages/ClientProfile'
import { AuthContext } from '../../context/constants'
import { mockUsers } from '../fixtures/users'

const api = vi.hoisted(() => ({
  myParcels: vi.fn(),
  tracking: vi.fn(),
  getNotes: vi.fn(),
  create: vi.fn(),
  publicTrack: vi.fn(),
  updateMe: vi.fn(),
  getRoute: vi.fn(),
}))

vi.mock('../../services/api', () => ({
  parcelsApi: {
    myParcels: api.myParcels,
    tracking: api.tracking,
    getNotes: api.getNotes,
    create: api.create,
  },
  trackingApi: { publicTrack: api.publicTrack },
  usersApi: { updateMe: api.updateMe },
  mapsApi: { getRoute: api.getRoute },
}))

vi.mock('react-leaflet', () => ({
  MapContainer: () => null,
  TileLayer: () => null,
  Marker: () => null,
  Polyline: () => null,
  useMapEvents: () => {},
}))

const myParcels = [
  {
    id: 'ENV-001',
    guide: 'AWEN-2026-0001',
    originBranch: 'Sucursal Central',
    destinationBranch: 'Sucursal Norte',
    status: 'In Transit',
    createdAt: '2026-05-10',
  },
  {
    id: 'ENV-002',
    guide: 'AWEN-2026-0002',
    originBranch: 'Sucursal Central',
    destinationBranch: 'Sucursal Sur',
    status: 'Delivered',
    createdAt: '2026-05-08',
  },
]

function renderPage(user = mockUsers.client) {
  return render(
    <AuthContext.Provider value={{ user, login: vi.fn(), logout: vi.fn(), canAccess: () => true }}>
      <ClientProfile />
    </AuthContext.Provider>
  )
}

describe('ClientProfile', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    api.myParcels.mockResolvedValue({ data: myParcels, total: myParcels.length })
    api.tracking.mockResolvedValue([])
    api.getNotes.mockResolvedValue([])
    api.create.mockResolvedValue({ id: 'ENV-003', guide: 'AWEN-2026-0003' })
    api.publicTrack.mockResolvedValue({
      history: [
        {
          step: 'In Transit',
          completed: true,
          date: '2026-05-12',
          time: '10:00',
          location: 'Sucursal Norte',
          operator: 'Carlos Operador',
        },
      ],
      delivery_evidence: {
        driver: 'Pedro Conductor',
        deliveryDate: '2026-05-12',
        gps: '10.4806, -66.9036',
        photoUrl: '/uploads/evidencia.jpg',
      },
    })
    api.updateMe.mockResolvedValue({ status: 'ok' })
    api.getRoute.mockResolvedValue({ route: [], distance_km: 0 })
  })

  it('muestra los datos del perfil', async () => {
    renderPage()

    expect(await screen.findByText('Mi Perfil')).toBeInTheDocument()
    expect(screen.getByText('Nombre:')).toBeInTheDocument()
    expect(screen.getByText('Juan')).toBeInTheDocument()
    expect(screen.getByText('Apellido:')).toBeInTheDocument()
    expect(screen.getByText('Cliente')).toBeInTheDocument()
    expect(screen.getByText('Documento de Identidad:')).toBeInTheDocument()
    expect(screen.getByText('V-67890123')).toBeInTheDocument()
    expect(screen.getByText('juan@email.com')).toBeInTheDocument()
  })

  it('muestra el historial de encomiendas', async () => {
    renderPage()

    expect(await screen.findByText('Historial de Envios')).toBeInTheDocument()
    expect(screen.getAllByText('AWEN-2026-0001').length).toBeGreaterThanOrEqual(2)
    expect(screen.getAllByText('AWEN-2026-0002').length).toBeGreaterThanOrEqual(2)
    expect(screen.getAllByText('Sucursal Norte').length).toBeGreaterThanOrEqual(1)
  })

  it('muestra el estado vacio cuando no hay encomiendas', async () => {
    api.myParcels.mockResolvedValue({ data: [], total: 0 })

    renderPage()

    await waitFor(() => {
      expect(screen.getAllByText('No tienes envios registrados.')).toHaveLength(2)
    })
  })

  it('abre el tracking de una encomienda y muestra el comprobante', async () => {
    const user = userEvent.setup()
    renderPage()
    await screen.findByText('Historial de Envios')

    await user.click(screen.getAllByText('AWEN-2026-0001')[0])

    expect(await screen.findByText('Tracking: AWEN-2026-0001')).toBeInTheDocument()
    expect(api.publicTrack).toHaveBeenCalledWith('AWEN-2026-0001')
    const timeline = document.querySelector('.stepper-timeline')
    expect(within(timeline).getByText('En Tránsito')).toBeInTheDocument()
    expect(screen.getByText('Comprobante de Entrega')).toBeInTheDocument()
    expect(screen.getByText('Conductor: Pedro Conductor')).toBeInTheDocument()
    expect(screen.getByAltText('Evidencia de entrega')).toBeInTheDocument()
  })

  it('muestra las notificaciones del conductor en el tracking', async () => {
    api.getNotes.mockResolvedValue([
      { text: 'Tu paquete llego a la sucursal', created_at: '2026-05-12 10:00', created_by: 'Pedro' },
    ])
    const user = userEvent.setup()
    renderPage()
    await screen.findByText('Historial de Envios')

    await user.click(screen.getAllByText('AWEN-2026-0001')[0])

    expect(await screen.findByText('Notificaciones del Conductor')).toBeInTheDocument()
    expect(screen.getByText('Tu paquete llego a la sucursal')).toBeInTheDocument()
  })

  it('actualiza los datos de contacto del perfil', async () => {
    const user = userEvent.setup()
    renderPage()
    await screen.findByText('Mi Perfil')

    await user.click(screen.getByRole('button', { name: 'Editar Datos' }))

    const phone = screen.getByPlaceholderText('+58 XXX XXX XXXX')
    await user.clear(phone)
    await user.type(phone, '+58 412 000 0000')

    const address = screen.getByPlaceholderText('Calle, ciudad')
    await user.clear(address)
    await user.type(address, 'Nueva Direccion 123')

    await user.click(screen.getByRole('button', { name: 'Guardar' }))

    await waitFor(() => {
      expect(api.updateMe).toHaveBeenCalledWith(expect.objectContaining({
        phone: '+58 412 000 0000',
        address: 'Nueva Direccion 123',
      }))
    })
    expect(await screen.findByRole('button', { name: 'Editar Datos' })).toBeInTheDocument()
  })

  it('valida que se seleccione origen y destino al crear una encomienda', async () => {
    const user = userEvent.setup()
    renderPage()
    await screen.findByText('Mi Perfil')

    await user.click(screen.getByRole('button', { name: 'Nuevo Paquete' }))
    expect(await screen.findByText('Nueva Encomienda')).toBeInTheDocument()

    await user.click(screen.getByRole('button', { name: 'Crear Encomienda' }))

    expect(await screen.findByText('Selecciona origen y destino en el mapa.')).toBeInTheDocument()
    expect(api.create).not.toHaveBeenCalled()
  })

  it('muestra el error cuando falla la carga de encomiendas', async () => {
    api.myParcels.mockRejectedValue(new Error('No se pudieron cargar las encomiendas'))

    renderPage()

    expect(await screen.findByText('No se pudieron cargar las encomiendas')).toBeInTheDocument()
  })
})
