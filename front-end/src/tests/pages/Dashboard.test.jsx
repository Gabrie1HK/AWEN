import { describe, it, expect, afterEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import { http, HttpResponse } from 'msw'
import Dashboard from '../../pages/Dashboard'
import { server } from '../mocks/setup'

describe('Dashboard', () => {
  afterEach(() => {
    server.resetHandlers()
  })

  it('muestra los KPIs principales', async () => {
    render(<Dashboard />)

    expect(await screen.findByText('Envíos Totales Hoy')).toBeInTheDocument()
    expect(screen.getByText('En Tránsito')).toBeInTheDocument()
    expect(screen.getByText('Entregados Exitosamente')).toBeInTheDocument()
    expect(screen.getByText('Devueltos / Fallidos')).toBeInTheDocument()

    const values = [...document.querySelectorAll('.stat-card-value')].map(el => el.textContent)
    expect(values).toEqual(['150', '45', '95', '10'])
  })

  it('muestra los graficos de envios y sucursales', async () => {
    render(<Dashboard />)

    expect(await screen.findByText('Envíos Últimos 7 Días')).toBeInTheDocument()
    expect(screen.getByText('Entregas por Sucursal')).toBeInTheDocument()
    expect(screen.getByText('Sucursal Central')).toBeInTheDocument()
    expect(screen.getByText('Sucursal Norte')).toBeInTheDocument()
    expect(screen.getByText('Sucursal Sur')).toBeInTheDocument()
  })

  it('muestra la actividad reciente', async () => {
    render(<Dashboard />)

    expect(await screen.findByText('Actividad Reciente')).toBeInTheDocument()
    expect(screen.getByText('Encomienda creada')).toBeInTheDocument()
    expect(screen.getByText('Carlos Operador')).toBeInTheDocument()
  })

  it('muestra el error cuando falla la carga', async () => {
    server.use(
      http.get('/api/v1/dashboard', () =>
        HttpResponse.json({ message: 'Fallo del dashboard' }, { status: 500 }),
      ),
    )

    render(<Dashboard />)

    expect(await screen.findByText('Fallo del dashboard')).toBeInTheDocument()
  })
})
