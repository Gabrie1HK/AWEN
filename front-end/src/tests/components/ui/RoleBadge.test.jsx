import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import RoleBadge from '../../../components/ui/RoleBadge'

describe('RoleBadge', () => {
  it('renders Admin role', () => {
    render(<RoleBadge role="Admin" />)
    expect(screen.getByText('Admin')).toBeInTheDocument()
  })

  it('renders Warehouse Operator role', () => {
    render(<RoleBadge role="Warehouse Operator" />)
    expect(screen.getByText('Warehouse Operator')).toBeInTheDocument()
  })

  it('renders Driver role', () => {
    render(<RoleBadge role="Driver" />)
    expect(screen.getByText('Driver')).toBeInTheDocument()
  })

  it('renders Client role', () => {
    render(<RoleBadge role="Client" />)
    expect(screen.getByText('Client')).toBeInTheDocument()
  })

  it('handles unknown role', () => {
    render(<RoleBadge role="Visitor" />)
    expect(screen.getByText('Visitor')).toBeInTheDocument()
  })
})
