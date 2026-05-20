import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import StatusBadge from '../../../components/ui/StatusBadge'

describe('StatusBadge', () => {
  it('renders the status text', () => {
    render(<StatusBadge status="Delivered" />)
    expect(screen.getByText('Delivered')).toBeInTheDocument()
  })

  it('renders Registered status', () => {
    render(<StatusBadge status="Registered" />)
    expect(screen.getByText('Registered')).toBeInTheDocument()
  })

  it('renders In Transit status', () => {
    render(<StatusBadge status="In Transit" />)
    expect(screen.getByText('In Transit')).toBeInTheDocument()
  })

  it('renders Returned status', () => {
    render(<StatusBadge status="Returned" />)
    expect(screen.getByText('Returned')).toBeInTheDocument()
  })

  it('handles unknown status gracefully', () => {
    render(<StatusBadge status="Unknown" />)
    expect(screen.getByText('Unknown')).toBeInTheDocument()
  })
})
