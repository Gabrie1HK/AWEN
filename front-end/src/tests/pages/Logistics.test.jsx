import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import Logistics from '../../pages/Logistics'

const api = vi.hoisted(() => ({
  listBatches: vi.fn(),
  listVehicles: vi.fn(),
  createBatch: vi.fn(),
  assignBatch: vi.fn(),
  updateBatch: vi.fn(),
  parcelsList: vi.fn(),
}))

vi.mock('../../services/api', () => ({
  logisticsApi: {
    listBatches: api.listBatches,
    listVehicles: api.listVehicles,
    createBatch: api.createBatch,
    assignBatch: api.assignBatch,
    updateBatch: api.updateBatch,
  },
  parcelsApi: { list: api.parcelsList },
}))

const batches = [
  {
    id: 'LOTE-001',
    parcels: ['ENV-001', 'ENV-002'],
    status: 'Pending Assignment',
    vehicle: null,
    driver: null,
    parcelCount: 2,
  },
]

const vehicles = [
  { id: 1, plate: 'ABC-123', model: 'Foton Aumark', capacity: '1500 kg', driver: 'Pedro Conductor' },
  { id: 2, plate: 'XYZ-789', model: 'JMC Carrying', capacity: '1200 kg', driver: 'Ana Conductor' },
]

const parcels = [
  {
    id: 'ENV-001',
    guide: 'AWEN-2026-0001',
    originBranch: 'Sucursal Central',
    destinationBranch: 'Sucursal Norte',
    status: 'Registered',
  },
  {
    id: 'ENV-002',
    guide: 'AWEN-2026-0002',
    originBranch: 'Sucursal Central',
    destinationBranch: 'Sucursal Sur',
    status: 'At Destination Branch',
  },
  {
    id: 'ENV-003',
    guide: 'AWEN-2026-0003',
    originBranch: 'Sucursal Central',
    destinationBranch: 'Sucursal Este',
    status: 'Delivered',
  },
]

describe('Logistics', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    api.listBatches.mockResolvedValue({ data: batches })
    api.listVehicles.mockResolvedValue({ data: vehicles })
    api.parcelsList.mockResolvedValue({ data: parcels, total: parcels.length })
    api.createBatch.mockResolvedValue({
      id: 'LOTE-002',
      parcels: ['ENV-001'],
      status: 'Pending Assignment',
      vehicle: null,
      driver: null,
      parcelCount: 1,
    })
    api.assignBatch.mockResolvedValue({
      ...batches[0],
      status: 'Assigned',
      vehicle: 'ABC-123',
      driver: 'Pedro Conductor',
    })
    api.updateBatch.mockResolvedValue(batches[0])
  })

  it('muestra los lotes pendientes y los vehiculos', async () => {
    render(<Logistics />)

    expect(await screen.findByText('LOTE-001')).toBeInTheDocument()
    expect(screen.getByText('2 encomiendas')).toBeInTheDocument()
    expect(screen.getByText('Pedro Conductor')).toBeInTheDocument()
    expect(screen.getByText('ABC-123 — Foton Aumark')).toBeInTheDocument()
    expect(screen.getByText('Ana Conductor')).toBeInTheDocument()
  })

  it('pide lotes, vehiculos y encomiendas al cargar', async () => {
    render(<Logistics />)

    await waitFor(() => {
      expect(api.listBatches).toHaveBeenCalled()
      expect(api.listVehicles).toHaveBeenCalled()
      expect(api.parcelsList).toHaveBeenCalledWith({ pageSize: 100 })
    })
  })

  it('muestra los estados vacios cuando no hay datos', async () => {
    api.listBatches.mockResolvedValue({ data: [] })
    api.listVehicles.mockResolvedValue({ data: [] })
    api.parcelsList.mockResolvedValue({ data: [], total: 0 })

    render(<Logistics />)

    expect(await screen.findByText('No hay lotes pendientes')).toBeInTheDocument()
    expect(screen.getByText('No hay paquetes disponibles')).toBeInTheDocument()
  })

  it('solo ofrece encomiendas registradas o en sucursal destino', async () => {
    render(<Logistics />)

    expect(await screen.findByText('AWEN-2026-0001 — Sucursal Norte')).toBeInTheDocument()
    expect(screen.getByText('AWEN-2026-0002 — Sucursal Sur')).toBeInTheDocument()
    expect(screen.queryByText('AWEN-2026-0003 — Sucursal Este')).not.toBeInTheDocument()
  })

  it('expande un lote y muestra sus envios', async () => {
    const user = userEvent.setup()
    render(<Logistics />)
    await screen.findByText('LOTE-001')

    await user.click(screen.getByText('2 encomiendas'))

    expect(await screen.findByText('Envíos del lote')).toBeInTheDocument()
    const expanded = screen.getByText('Envíos del lote').closest('.batch-card')
    expect(within(expanded).getByText(/AWEN-2026-0001/)).toBeInTheDocument()
    expect(within(expanded).getByText(/AWEN-2026-0002/)).toBeInTheDocument()
  })

  it('crea un lote con las encomiendas seleccionadas', async () => {
    const user = userEvent.setup()
    render(<Logistics />)
    await screen.findByText('LOTE-001')

    await user.click(screen.getByLabelText('AWEN-2026-0001 — Sucursal Norte'))
    await user.click(screen.getByRole('button', { name: 'Crear Lote (1)' }))

    await waitFor(() => {
      expect(api.createBatch).toHaveBeenCalledWith({ parcels: ['ENV-001'] })
    })
    expect(await screen.findByText('LOTE-002')).toBeInTheDocument()
  })

  it('muestra error si falla la creacion del lote', async () => {
    api.createBatch.mockRejectedValue(new Error('fallo'))
    const user = userEvent.setup()
    render(<Logistics />)
    await screen.findByText('LOTE-001')

    await user.click(screen.getByLabelText('AWEN-2026-0001 — Sucursal Norte'))
    await user.click(screen.getByRole('button', { name: 'Crear Lote (1)' }))

    expect(await screen.findByText('No se pudo crear el lote')).toBeInTheDocument()
  })

  it('asigna un vehiculo a un lote pendiente', async () => {
    const user = userEvent.setup()
    render(<Logistics />)
    await screen.findByText('LOTE-001')

    await user.selectOptions(screen.getByRole('combobox'), '1')
    await user.click(screen.getByRole('button', { name: 'Asignar' }))

    await waitFor(() => {
      expect(api.assignBatch).toHaveBeenCalledWith('LOTE-001', {
        vehicle: 'ABC-123',
        driver: 'Pedro Conductor',
      })
    })
  })

  it('muestra error si falla la asignacion del lote', async () => {
    api.assignBatch.mockRejectedValue(new Error('fallo'))
    const user = userEvent.setup()
    render(<Logistics />)
    await screen.findByText('LOTE-001')

    await user.selectOptions(screen.getByRole('combobox'), '1')
    await user.click(screen.getByRole('button', { name: 'Asignar' }))

    expect(await screen.findByText('No se pudo asignar el lote')).toBeInTheDocument()
  })
})
