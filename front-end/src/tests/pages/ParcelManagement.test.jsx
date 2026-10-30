import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import ParcelManagement from '../../pages/ParcelManagement'

const api = vi.hoisted(() => ({
  list: vi.fn(),
  create: vi.fn(),
  update: vi.fn(),
  remove: vi.fn(),
  branchesList: vi.fn(),
  getRoute: vi.fn(),
}))

vi.mock('../../services/api', () => ({
  parcelsApi: {
    list: api.list,
    create: api.create,
    update: api.update,
    remove: api.remove,
  },
  branchesApi: { list: api.branchesList },
  mapsApi: { getRoute: api.getRoute },
}))

vi.mock('react-leaflet', () => ({
  MapContainer: () => null,
  TileLayer: () => null,
  Marker: () => null,
  Polyline: () => null,
  useMapEvents: () => {},
}))

beforeEach(() => {
  vi.clearAllMocks()
  // Default mock for list
  api.list.mockResolvedValue(listResponse(parcels))
  api.branchesList.mockResolvedValue(listResponse([
    { id: 'SUC-001', name: 'Sucursal Central', city: 'Valencia', address: 'Av. Principal', manager: 'Juan', phone: '123', active: true },
    { id: 'SUC-002', name: 'Sucursal Norte', city: 'Maracaibo', address: 'Calle 2', manager: 'Pedro', phone: '456', active: true },
  ]))
  api.getRoute.mockResolvedValue({ route: [], distance_km: 0 })
})

const parcels = [
  {
    id: 'ENV-001',
    guide: 'AWEN-2026-0001',
    sender: 'TechStore CA',
    senderId: 'J-12345678',
    senderPhone: '+58 212 123 4567',
    recipient: 'Roberto Garcia',
    recipientId: 'V-12345678',
    recipientPhone: '+58 414 123 4567',
    recipientAddress: 'Av. Universidad 742',
    originBranch: 'Sucursal Central',
    destinationBranch: 'Sucursal Norte',
    originAddress: 'Valencia, Carabobo',
    destinationAddress: 'Maracaibo, Zulia',
    weight: 2.5,
    dimensions: '30x20x15 cm',
    declaredValue: 150000,
    description: 'Notebook y accesorios',
    barcode: '|||AWEN-2026-0001|||',
    status: 'In Transit',
    createdAt: '2026-05-10',
  },
  {
    id: 'ENV-002',
    guide: 'AWEN-2026-0002',
    sender: 'Distribuidora Sur',
    senderId: 'J-87654321',
    senderPhone: '+58 212 765 4321',
    recipient: 'Carmen Flores',
    recipientId: 'V-87654321',
    recipientPhone: '+58 414 765 4321',
    recipientAddress: 'Calle 60 123',
    originBranch: 'Sucursal Central',
    destinationBranch: 'Sucursal Sur',
    originAddress: 'Valencia, Carabobo',
    destinationAddress: 'Merida',
    weight: 15,
    dimensions: '50x40x30 cm',
    declaredValue: 320000,
    description: 'Documentos',
    barcode: '|||AWEN-2026-0002|||',
    status: 'Delivered',
    createdAt: '2026-05-08',
  },
]

function listResponse(items, total = items.length) {
  return {
    data: items,
    total,
    page: 1,
    pageSize: 10,
    totalPages: Math.max(1, Math.ceil(total / 10)),
  }
}

describe('ParcelManagement', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    api.list.mockResolvedValue(listResponse(parcels))
    api.branchesList.mockResolvedValue({
      data: [{ id: 1, name: 'Sucursal Central', active: true }],
      total: 1,
    })
    api.create.mockResolvedValue({ id: 'ENV-003', guide: 'AWEN-2026-0003' })
    api.update.mockResolvedValue({ id: 'ENV-001' })
    api.remove.mockResolvedValue({ status: 'ok' })
    api.getRoute.mockResolvedValue({ route: [], distance_km: 0 })
  })

  it('muestra el listado de encomiendas', async () => {
    render(<ParcelManagement />)

    expect(await screen.findByText('AWEN-2026-0001')).toBeInTheDocument()
    expect(screen.getByText('AWEN-2026-0002')).toBeInTheDocument()
    expect(screen.getByText('TechStore CA')).toBeInTheDocument()
    expect(screen.getByText('Roberto Garcia')).toBeInTheDocument()
  })

  it('solicita la primera pagina al cargar', async () => {
    render(<ParcelManagement />)

    await waitFor(() => {
      expect(api.list).toHaveBeenCalledWith(expect.objectContaining({
        page: 1,
        pageSize: 10,
      }))
    })
    expect(api.branchesList).toHaveBeenCalled()
  })

  it('muestra el estado vacio cuando no hay encomiendas', async () => {
    api.list.mockResolvedValue(listResponse([], 0))

    render(<ParcelManagement />)

    expect(await screen.findByText('No hay datos disponibles')).toBeInTheDocument()
  })

  it('muestra el error cuando falla la carga', async () => {
    api.list.mockRejectedValue(new Error('Fallo de red'))

    render(<ParcelManagement />)

    expect(await screen.findByText('Fallo de red')).toBeInTheDocument()
  })

  it('filtra por texto de busqueda', async () => {
    const user = userEvent.setup()
    render(<ParcelManagement />)
    await screen.findByText('AWEN-2026-0001')

    await user.type(screen.getByPlaceholderText('Buscar...'), 'TechStore')

    await waitFor(() => {
      expect(api.list).toHaveBeenCalledWith(expect.objectContaining({
        search: 'TechStore',
      }))
    })
  })

  it('filtra por estado', async () => {
    const user = userEvent.setup()
    render(<ParcelManagement />)
    await screen.findByText('AWEN-2026-0001')

    await user.selectOptions(screen.getByRole('combobox'), 'Delivered')

    await waitFor(() => {
      expect(api.list).toHaveBeenCalledWith(expect.objectContaining({
        status: 'Delivered',
      }))
    })
  })

  it('abre el formulario de nueva encomienda', async () => {
    const user = userEvent.setup()
    render(<ParcelManagement />)
    await screen.findByText('AWEN-2026-0001')

    await user.click(screen.getByRole('button', { name: /Nueva Encomienda/i }))

    expect(screen.getByRole('heading', { name: 'Nueva Encomienda' })).toBeInTheDocument()
    expect(screen.getByText('Sucursal Origen')).toBeInTheDocument()
    expect(screen.getByText('Sucursal Destino')).toBeInTheDocument()
  })

  it('crea una encomienda desde el formulario', async () => {
    const user = userEvent.setup()
    render(<ParcelManagement />)
    await screen.findByText('AWEN-2026-0001')

    await user.click(screen.getByRole('button', { name: /Nueva Encomienda/i }))

    const form = document.querySelector('form.form-grid')
    const sender = form.querySelector('input[name="sender"]')
    await user.type(sender, 'Nuevo Remitente')

    await user.click(screen.getByRole('button', { name: 'Crear Encomienda' }))

    await waitFor(() => {
      expect(api.create).toHaveBeenCalledWith(expect.objectContaining({
        sender: 'Nuevo Remitente',
      }))
    })
  })

  it('muestra error si falla la creacion', async () => {
    api.create.mockRejectedValue(new Error('Datos invalidos'))
    const user = userEvent.setup()
    render(<ParcelManagement />)
    await screen.findByText('AWEN-2026-0001')

    await user.click(screen.getByRole('button', { name: /Nueva Encomienda/i }))
    await user.click(screen.getByRole('button', { name: 'Crear Encomienda' }))

    expect(await screen.findByText('Datos invalidos')).toBeInTheDocument()
  })

  it('elimina una encomienda tras confirmar', async () => {
    const user = userEvent.setup()
    render(<ParcelManagement />)
    await screen.findByText('AWEN-2026-0001')
    let listCallCount = 0
    api.list.mockImplementation(() => {
      listCallCount++
      if (listCallCount === 1) return Promise.resolve(listResponse(parcels))
      return Promise.resolve(listResponse([parcels[1]]))
    })

    await user.click(screen.getAllByTitle('Eliminar')[0])

    const dialog = await screen.findByText('Eliminar encomienda').then(el => el.closest('.modal-content'))
    expect(dialog).not.toBeNull()
    await user.click(within(dialog).getByRole('button', { name: 'Si, Eliminar' }))

    await waitFor(() => {
      expect(api.remove).toHaveBeenCalledWith('ENV-001')
    })
    await waitFor(() => {
      expect(screen.queryByText('AWEN-2026-0001')).not.toBeInTheDocument()
    })
  })

  it('muestra el detalle de una encomienda', async () => {
    const user = userEvent.setup()
    render(<ParcelManagement />)
    await screen.findByText('AWEN-2026-0001')

    await user.click(screen.getAllByTitle('Ver')[0])

    const heading = await screen.findByRole('heading', { name: 'Encomienda AWEN-2026-0001' })
    const modal = heading.closest('.modal-content')
    expect(within(modal).getByText('Remitente')).toBeInTheDocument()
    expect(within(modal).getByText('Destinatario')).toBeInTheDocument()
    expect(within(modal).getByText('Paquete')).toBeInTheDocument()
    expect(within(modal).getByText('Ruta')).toBeInTheDocument()
    expect(within(modal).getByText('Codigos')).toBeInTheDocument()
    expect(within(modal).getByText('|||AWEN-2026-0001|||')).toBeInTheDocument()
  })

  it('edita una encomienda existente', async () => {
    const updatedParcel = { ...parcels[0], sender: 'TechStore Editado' }
    api.update.mockResolvedValue(updatedParcel)
    let listCallCount = 0
    api.list.mockImplementation(() => {
      listCallCount++
      if (listCallCount === 1) return Promise.resolve(listResponse(parcels))
      return Promise.resolve(listResponse([updatedParcel, parcels[1]]))
    })
    const user = userEvent.setup()
    render(<ParcelManagement />)
    await screen.findByText('AWEN-2026-0001')

    await user.click(screen.getAllByTitle('Editar')[0])

    expect(await screen.findByRole('heading', { name: 'Editar Encomienda' })).toBeInTheDocument()

    const form = document.querySelector('form.form-grid')
    const sender = form.querySelector('input[name="sender"]')
    await user.clear(sender)
    await user.type(sender, 'TechStore Editado')

    await user.click(screen.getByRole('button', { name: 'Guardar Cambios' }))

    await waitFor(() => {
      expect(api.update).toHaveBeenCalledWith('ENV-001', expect.objectContaining({
        sender: 'TechStore Editado',
      }))
    })
    expect(await screen.findByText('TechStore Editado')).toBeInTheDocument()
  })

  it('muestra error si falla la actualizacion', async () => {
    api.update.mockRejectedValue(new Error('No se pudo actualizar'))
    const user = userEvent.setup()
    render(<ParcelManagement />)
    await screen.findByText('AWEN-2026-0001')

    await user.click(screen.getAllByTitle('Editar')[0])
    await screen.findByRole('heading', { name: 'Editar Encomienda' })
    await user.click(screen.getByRole('button', { name: 'Guardar Cambios' }))

    expect(await screen.findByText('No se pudo actualizar')).toBeInTheDocument()
  })

  it('cambia de pagina en el listado', async () => {
    api.list.mockResolvedValue(listResponse(parcels, 25))
    const user = userEvent.setup()
    render(<ParcelManagement />)
    await screen.findByText('AWEN-2026-0001')
    await waitFor(() => expect(screen.getByText('1 / 3')).toBeInTheDocument())

    await user.click(screen.getByRole('button', { name: 'Siguiente' }))

    await waitFor(() => {
      expect(api.list).toHaveBeenCalledWith(expect.objectContaining({ page: 2 }))
    })
  })
})
