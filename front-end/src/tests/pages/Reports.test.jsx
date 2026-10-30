import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import Reports from '../../pages/Reports'

const api = vi.hoisted(() => ({
  summary: vi.fn(),
  dailyVolume: vi.fn(),
  deliveriesByBranch: vi.fn(),
  topRoutes: vi.fn(),
  exportCsv: vi.fn(),
  parcelsList: vi.fn(),
}))

vi.mock('../../services/api', () => ({
  reportsApi: {
    summary: api.summary,
    dailyVolume: api.dailyVolume,
    deliveriesByBranch: api.deliveriesByBranch,
    topRoutes: api.topRoutes,
    exportCsv: api.exportCsv,
  },
  parcelsApi: { list: api.parcelsList },
}))

const summary = {
  totalVolume: 150,
  avgDeliveryTime: '2.5 dias',
  successRate: '92%',
  returnRate: '8%',
}

const parcels = [
  { id: '1', status: 'Delivered' },
  { id: '2', status: 'Delivered' },
  { id: '3', status: 'In Transit' },
  { id: '4', status: 'Registered' },
]

describe('Reports', () => {
  let originalCreateObjectURL
  let originalRevokeObjectURL
  let clickSpy

  beforeEach(() => {
    vi.clearAllMocks()
    api.summary.mockResolvedValue(summary)
    api.dailyVolume.mockResolvedValue([
      { day: 'May 10', count: 25 },
      { day: 'May 11', count: 30 },
    ])
    api.deliveriesByBranch.mockResolvedValue([
      { branch: 'Sucursal Central', count: 80 },
      { branch: 'Sucursal Norte', count: 45 },
    ])
    api.topRoutes.mockResolvedValue([
      { route: 'Central → Norte', volume: 40, avgTime: '2h' },
    ])
    api.parcelsList.mockResolvedValue({ data: parcels, total: parcels.length })
    api.exportCsv.mockResolvedValue('ruta,volumen\nCentral,40')

    originalCreateObjectURL = URL.createObjectURL
    originalRevokeObjectURL = URL.revokeObjectURL
    URL.createObjectURL = vi.fn(() => 'blob:reporte')
    URL.revokeObjectURL = vi.fn()
    clickSpy = vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(() => {})
  })

  afterEach(() => {
    URL.createObjectURL = originalCreateObjectURL
    URL.revokeObjectURL = originalRevokeObjectURL
    clickSpy.mockRestore()
  })

  it('muestra el resumen de KPIs', async () => {
    render(<Reports />)

    expect(await screen.findByText('Volumen Total')).toBeInTheDocument()
    expect(screen.getByText('150')).toBeInTheDocument()
    expect(screen.getByText('2.5 dias')).toBeInTheDocument()
    expect(screen.getByText('92%')).toBeInTheDocument()
    expect(screen.getByText('8%')).toBeInTheDocument()
  })

  it('muestra los graficos y la tabla de rutas', async () => {
    render(<Reports />)

    expect(await screen.findByText('Volumen Diario (30 dias)')).toBeInTheDocument()
    expect(screen.getByText('Entregas por Sucursal')).toBeInTheDocument()
    expect(screen.getByText('Distribucion por Estado')).toBeInTheDocument()
    expect(screen.getByText('Top Rutas por Volumen')).toBeInTheDocument()
    expect(screen.getByText('Central → Norte')).toBeInTheDocument()
  })

  it('consulta los datos con el rango de fechas inicial', async () => {
    render(<Reports />)

    await waitFor(() => {
      expect(api.dailyVolume).toHaveBeenCalledWith({
        dateFrom: '2026-05-01',
        dateTo: '2026-05-13',
      })
    })
    expect(api.summary).toHaveBeenCalled()
    expect(api.deliveriesByBranch).toHaveBeenCalled()
    expect(api.topRoutes).toHaveBeenCalled()
    expect(api.parcelsList).toHaveBeenCalledWith({ pageSize: 100 })
  })

  it('exporta el reporte a CSV', async () => {
    const user = userEvent.setup()
    render(<Reports />)
    await screen.findByText('Volumen Total')

    await user.click(screen.getByRole('button', { name: /Exportar/i }))

    await waitFor(() => {
      expect(api.exportCsv).toHaveBeenCalled()
    })
    expect(URL.createObjectURL).toHaveBeenCalled()
    expect(clickSpy).toHaveBeenCalled()
    expect(URL.revokeObjectURL).toHaveBeenCalledWith('blob:reporte')
  })

  it('muestra error si falla la exportacion', async () => {
    api.exportCsv.mockRejectedValue(new Error('fallo'))
    const user = userEvent.setup()
    render(<Reports />)
    await screen.findByText('Volumen Total')

    await user.click(screen.getByRole('button', { name: /Exportar/i }))

    expect(await screen.findByText('No se pudo exportar el reporte')).toBeInTheDocument()
  })
})
