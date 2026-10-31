import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor, fireEvent, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import ProofOfDelivery from '../../pages/ProofOfDelivery'
import { AuthContext } from '../../context/constants'
import { mockUsers } from '../fixtures/users'

const api = vi.hoisted(() => ({
  list: vi.fn(),
  addPod: vi.fn(),
  uploadEvidence: vi.fn(),
}))

vi.mock('../../services/api', () => ({
  deliveriesApi: {
    list: api.list,
    addPod: api.addPod,
    uploadEvidence: api.uploadEvidence,
  },
}))

const deliveries = [
  {
    id: 'DEL-001',
    guide: 'AWEN-2026-0001',
    recipient: 'Roberto Garcia',
    driver: 'Pedro Conductor',
    deliveryDate: null,
    podType: 'Photo',
    status: 'Pending',
    photoUrl: null,
    gps: null,
  },
  {
    id: 'DEL-002',
    guide: 'AWEN-2026-0002',
    recipient: 'Carmen Flores',
    driver: 'Ana Conductor',
    deliveryDate: '2026-05-12',
    podType: 'Signature',
    status: 'Completed',
    photoUrl: '/uploads/firma.png',
    gps: '8.3519, -62.6414',
  },
]

function renderPage(user = mockUsers.operator) {
  return render(
    <AuthContext.Provider value={{ user, login: vi.fn(), logout: vi.fn(), canAccess: () => true }}>
      <ProofOfDelivery />
    </AuthContext.Provider>
  )
}

describe('ProofOfDelivery', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    api.list.mockResolvedValue({ data: deliveries, total: deliveries.length })
    api.addPod.mockResolvedValue({ id: 'DEL-001', status: 'Completed' })
    api.uploadEvidence.mockResolvedValue({ url: '/uploads/evidencia.jpg' })
  })

  it('lista las entregas con sus datos principales', async () => {
    renderPage()

    expect(await screen.findByText('AWEN-2026-0001')).toBeInTheDocument()
    expect(screen.getByText('AWEN-2026-0002')).toBeInTheDocument()
    expect(screen.getByText('Roberto Garcia')).toBeInTheDocument()
    expect(screen.getByText('Pedro Conductor')).toBeInTheDocument()
    expect(screen.getByText('Photo')).toBeInTheDocument()
    expect(screen.getByText('Pendiente')).toBeInTheDocument()
    expect(screen.getByText('Completado')).toBeInTheDocument()
  })

  it('consulta la primera pagina al cargar', async () => {
    renderPage()

    await waitFor(() => {
      expect(api.list).toHaveBeenCalledWith({ page: 1, pageSize: 10 })
    })
  })

  it('abre el modal de comprobante con la informacion de la entrega', async () => {
    const user = userEvent.setup()
    renderPage()
    await screen.findByText('AWEN-2026-0001')

    await user.click(screen.getAllByRole('button', { name: 'Ver POD' })[0])

    expect(await screen.findByText('Comprobante de Entrega')).toBeInTheDocument()
    expect(screen.getByText('Informacion')).toBeInTheDocument()
    expect(screen.getByText('Guia: AWEN-2026-0001')).toBeInTheDocument()
    expect(screen.getByText('Destinatario: Roberto Garcia')).toBeInTheDocument()
    expect(screen.getByText('Registrar Entrega')).toBeInTheDocument()
  })

  it('mantiene deshabilitado el registro hasta subir evidencia', async () => {
    const user = userEvent.setup()
    renderPage()
    await screen.findByText('AWEN-2026-0001')

    await user.click(screen.getAllByRole('button', { name: 'Ver POD' })[0])

    expect(await screen.findByRole('button', { name: 'Registrar Comprobante' })).toBeDisabled()
    expect(screen.getByRole('button', { name: 'Subir Foto' })).toBeInTheDocument()
  })

  it('sube la evidencia y registra el comprobante', async () => {
    const user = userEvent.setup()
    const { container } = renderPage()
    await screen.findByText('AWEN-2026-0001')

    await user.click(screen.getAllByRole('button', { name: 'Ver POD' })[0])
    await screen.findByText('Registrar Entrega')

    const fileInput = container.querySelector('input[type="file"]')
    fireEvent.change(fileInput, {
      target: { files: [new File(['foto'], 'evidencia.jpg', { type: 'image/jpeg' })] },
    })

    expect(await screen.findByText('Archivo subido correctamente')).toBeInTheDocument()

    await user.type(screen.getByPlaceholderText('Ej: 10.4806, -66.9036'), '10.4806, -66.9036')
    await user.click(screen.getByRole('button', { name: 'Registrar Comprobante' }))

    await waitFor(() => {
      expect(api.addPod).toHaveBeenCalledWith('DEL-001', expect.objectContaining({
        podType: 'Photo',
        photoUrl: '/uploads/evidencia.jpg',
        gps: '10.4806, -66.9036',
        deliveryDate: expect.any(String),
      }))
    })
    const modal = screen.getByText('Comprobante de Entrega').closest('.modal-content')
    expect(within(modal).getByText('Completado')).toBeInTheDocument()
  })

  it('muestra error si falla la subida de evidencia', async () => {
    api.uploadEvidence.mockRejectedValue(new Error('fallo'))
    const user = userEvent.setup()
    const { container } = renderPage()
    await screen.findByText('AWEN-2026-0001')

    await user.click(screen.getAllByRole('button', { name: 'Ver POD' })[0])
    await screen.findByText('Registrar Entrega')

    fireEvent.change(container.querySelector('input[type="file"]'), {
      target: { files: [new File(['foto'], 'evidencia.jpg', { type: 'image/jpeg' })] },
    })

    expect(await screen.findByText('Error al subir archivo. Intente de nuevo.')).toBeInTheDocument()
  })

  it('filtra las entregas del conductor autenticado', async () => {
    renderPage({ ...mockUsers.driver, name: 'Pedro Conductor' })

    expect(await screen.findByText('AWEN-2026-0001')).toBeInTheDocument()
    expect(screen.queryByText('AWEN-2026-0002')).not.toBeInTheDocument()
  })

  it('muestra el error cuando falla la carga', async () => {
    api.list.mockRejectedValue(new Error('No se pudieron cargar las entregas'))

    renderPage()

    expect(await screen.findByText('No se pudieron cargar las entregas')).toBeInTheDocument()
  })

  it('cambia de pagina en el listado', async () => {
    api.list.mockResolvedValue({ data: deliveries, total: 25 })
    const user = userEvent.setup()
    renderPage()
    await screen.findByText('AWEN-2026-0001')
    await waitFor(() => expect(screen.getByText('1 / 3')).toBeInTheDocument())

    await user.click(screen.getByRole('button', { name: 'Siguiente' }))

    await waitFor(() => {
      expect(api.list).toHaveBeenCalledWith({ page: 2, pageSize: 10 })
    })
  })
})
