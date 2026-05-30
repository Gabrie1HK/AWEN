import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import StatusBadge from '../../../components/ui/StatusBadge'

describe('StatusBadge', () => {
  it('renders the status text in Spanish', () => {
    render(<StatusBadge status="Delivered" />)
    expect(screen.getByText('Entregado')).toBeInTheDocument()
  })

  it('renders Registered status in Spanish', () => {
    render(<StatusBadge status="Registered" />)
    expect(screen.getByText('Registrado')).toBeInTheDocument()
  })

  it('renders In Transit status in Spanish', () => {
    render(<StatusBadge status="In Transit" />)
    expect(screen.getByText('En Tránsito')).toBeInTheDocument()
  })

  it('renders Returned status in Spanish', () => {
    render(<StatusBadge status="Returned" />)
    expect(screen.getByText('Devuelto')).toBeInTheDocument()
  })

  it('handles unknown status gracefully', () => {
    render(<StatusBadge status="Unknown" />)
    expect(screen.getByText('Unknown')).toBeInTheDocument()
  })
})
