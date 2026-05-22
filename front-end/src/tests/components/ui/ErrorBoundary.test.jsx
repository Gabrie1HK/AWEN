import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import ErrorBoundary from '../../../components/ui/ErrorBoundary'

const GoodChild = () => <div>Todo bien</div>
const BadChild = () => { throw new Error('Test error') }

describe('ErrorBoundary', () => {
  it('renders children when no error', () => {
    render(<ErrorBoundary><GoodChild /></ErrorBoundary>)
    expect(screen.getByText('Todo bien')).toBeInTheDocument()
  })

  it('catches errors and shows default fallback', () => {
    vi.spyOn(console, 'error').mockImplementation(() => {})
    render(<ErrorBoundary><BadChild /></ErrorBoundary>)
    expect(screen.getByText('Algo salio mal')).toBeInTheDocument()
    expect(screen.getByText('Recargar Pagina')).toBeInTheDocument()
    vi.restoreAllMocks()
  })

  it('renders custom fallback when provided', () => {
    vi.spyOn(console, 'error').mockImplementation(() => {})
    render(<ErrorBoundary fallback={<div>Fallback personalizado</div>}><BadChild /></ErrorBoundary>)
    expect(screen.getByText('Fallback personalizado')).toBeInTheDocument()
    expect(screen.queryByText('Algo salio mal')).not.toBeInTheDocument()
    vi.restoreAllMocks()
  })
})