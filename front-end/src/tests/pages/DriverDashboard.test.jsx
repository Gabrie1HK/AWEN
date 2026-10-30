import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor, fireEvent, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import DriverDashboard from '../../pages/DriverDashboard'
import { AuthContext } from '../../context/constants'
import { mockUsers } from '../fixtures/users'

const api = vi.hoisted(() => ({
  list: vi.fn(),
  tracking: vi.fn(),
  getNotes: vi.fn(),
  uploadEvidence: vi.fn(),
  updateStatus: vi.fn(),
  addNote: vi.fn(),
}))

vi.mock('../../services/api', () => ({
  parcelsApi: {
    list: api.list,
    tracking: api.tracking,
    getNotes: api.getNotes,
    uploadEvidence: api.uploadEvidence,
    updateStatus: api.updateStatus,
    addNote: api.addNote,
  },
}))

const parcels = [
  {
    id: 'ENV-001',
    guide: 'AWEN-2026-0001',
    recipient: 'Roberto Garcia',
    recipientAddress: 'Av. Universidad 742',
    description: 'Notebook y accesorios',
    originBranch: 'Sucursal Central',
    destinationBranch: 'Sucursal Norte',
    status: 'In Transit',
    createdAt: '2026-05-10',
  },
  {
    id: 'ENV-002',
    guide: 'AWEN-2026-0002',
    recipient: 'Carmen Flores',
    recipientAddress: 'Calle 60',
    description: 'Documentos',
    originBranch: 'Sucursal Central',
    destinationBranch: 'Sucursal Sur',
    status: 'Registered',
    createdAt: '2026-05-09',
  },
]

const trackingSteps = [
  {
    step: 'Registered',
    completed: true,
    date: '2026-05-10',
    time: '09:00',
    location: 'Sucursal Central',
    operator: 'Carlos Operador',
  },
  {
    step: 'In Transit',
    completed: true,
    date: '2026-05-11',
    time: '12:00',
    location: 'Sucursal Norte',
    operator: 'Pedro Conductor',
  },
]

function renderPage() {
  return render(
    <AuthContext.Provider value={{
      user: mockUsers.driver,
      login: vi.fn(),
      logout: vi.fn(),
      canAccess: () => true,
    }}>
      <DriverDashboard />
    </AuthContext.Provider>
  )
}

describe('DriverDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    api.list.mockResolvedValue({ data: parcels, total: parcels.length })
    api.tracking.mockResolvedValue(trackingSteps)
    api.getNotes.mockResolvedValue([
      { text: 'Cliente no estaba en casa', is_public: false, created_at: '2026-05-11 12:30', created_by: 'Pedro' },
    ])
    api.uploadEvidence.mockResolvedValue({ url: '/uploads/foto.jpg' })
    api.updateStatus.mockImplementation((id, status) => Promise.resolve({
      ...parcels.find(p => p.id === id),
      status,
    }))
    api.addNote.mockResolvedValue({ status: 'ok' })
  })

  it('muestra el listado de entregas del conductor', async () => {
    renderPage()

    expect(await screen.findByText('AWEN-2026-0001')).toBeInTheDocument()
    expect(screen.getByText('Mis Entregas')).toBeInTheDocument()
    expect(screen.getByText('Conductor: Pedro')).toBeInTheDocument()
    expect(screen.getByText('Roberto Garcia')).toBeInTheDocument()
    expect(screen.getByText('Sucursal Central → Sucursal Norte')).toBeInTheDocument()
  })

  it('consulta las encomiendas al cargar', async () => {
    renderPage()

    await waitFor(() => {
      expect(api.list).toHaveBeenCalledWith({ pageSize: 50 })
    })
  })

  it('abre el detalle de una encomienda con tracking y notas', async () => {
    const user = userEvent.setup()
    renderPage()
    await screen.findByText('AWEN-2026-0001')

    await user.click(screen.getAllByRole('button', { name: 'Gestionar' })[0])

    expect(await screen.findByText('Encomienda AWEN-2026-0001')).toBeInTheDocument()
    expect(api.tracking).toHaveBeenCalledWith('AWEN-2026-0001')
    expect(api.getNotes).toHaveBeenCalledWith('AWEN-2026-0001')
    expect(screen.getByText('Actualizar Estado')).toBeInTheDocument()
    expect(screen.getByText('Agregar Notificacion')).toBeInTheDocument()
    expect(await screen.findByText('Cliente no estaba en casa')).toBeInTheDocument()
    const timeline = document.querySelector('.stepper-timeline')
    expect(within(timeline).getByText('Registrado')).toBeInTheDocument()
    expect(within(timeline).getByText('En Tránsito')).toBeInTheDocument()
  })

  it('actualiza el estado de una encomienda', async () => {
    const user = userEvent.setup()
    renderPage()
    await screen.findByText('AWEN-2026-0001')

    await user.click(screen.getAllByRole('button', { name: 'Gestionar' })[0])
    await screen.findByText('Encomienda AWEN-2026-0001')

    await user.selectOptions(screen.getByRole('combobox'), 'At Destination Branch')
    await user.click(screen.getByRole('button', { name: 'Actualizar' }))

    await waitFor(() => {
      expect(api.updateStatus).toHaveBeenCalledWith('ENV-001', 'At Destination Branch', {})
    })
    expect(await screen.findByText('Estado actualizado correctamente')).toBeInTheDocument()
  })

  it('registra una entrega con evidencia fotografica', async () => {
    const user = userEvent.setup()
    const { container } = renderPage()
    await screen.findByText('AWEN-2026-0001')

    await user.click(screen.getAllByRole('button', { name: 'Gestionar' })[0])
    await screen.findByText('Encomienda AWEN-2026-0001')

    await user.selectOptions(screen.getByRole('combobox'), 'Delivered')
    expect(await screen.findByRole('button', { name: 'Confirmar Entrega' })).toBeInTheDocument()

    const fileInput = container.querySelector('input[type="file"]')
    fireEvent.change(fileInput, {
      target: { files: [new File(['foto'], 'entrega.jpg', { type: 'image/jpeg' })] },
    })

    expect(await screen.findByText('Foto lista')).toBeInTheDocument()

    await user.type(screen.getByPlaceholderText('Ej: 10.4806, -66.9036'), '10.4806, -66.9036')
    await user.click(screen.getByRole('button', { name: 'Confirmar Entrega' }))

    await waitFor(() => {
      expect(api.updateStatus).toHaveBeenCalledWith('ENV-001', 'Delivered', expect.objectContaining({
        photoUrl: '/uploads/foto.jpg',
        gps: '10.4806, -66.9036',
      }))
    })
    expect(await screen.findByText('Entrega registrada exitosamente')).toBeInTheDocument()
  })

  it('muestra error si falla el cambio de estado', async () => {
    api.updateStatus.mockRejectedValue(new Error('No se pudo actualizar'))
    const user = userEvent.setup()
    renderPage()
    await screen.findByText('AWEN-2026-0001')

    await user.click(screen.getAllByRole('button', { name: 'Gestionar' })[0])
    await screen.findByText('Encomienda AWEN-2026-0001')

    await user.selectOptions(screen.getByRole('combobox'), 'In Transit')
    await user.click(screen.getByRole('button', { name: 'Actualizar' }))

    expect(await screen.findByText('No se pudo actualizar')).toBeInTheDocument()
  })

  it('agrega una notificacion interna a la encomienda', async () => {
    const user = userEvent.setup()
    renderPage()
    await screen.findByText('AWEN-2026-0001')

    await user.click(screen.getAllByRole('button', { name: 'Gestionar' })[0])
    await screen.findByText('Encomienda AWEN-2026-0001')

    await user.type(
      screen.getByPlaceholderText('Ej: Retraso de 30 min por trafico'),
      'Retraso por trafico',
    )
    await user.click(screen.getByRole('button', { name: 'Enviar' }))

    await waitFor(() => {
      expect(api.addNote).toHaveBeenCalledWith('AWEN-2026-0001', 'Retraso por trafico', false)
    })
    expect(await screen.findByText('Notificacion agregada')).toBeInTheDocument()
  })

  it('muestra el error cuando falla la carga de entregas', async () => {
    api.list.mockRejectedValue(new Error('No se pudieron cargar las entregas'))

    renderPage()

    expect(await screen.findByText('No se pudieron cargar las entregas')).toBeInTheDocument()
  })
})
