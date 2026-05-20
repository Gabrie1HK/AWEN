import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import SearchBar from '../../../components/ui/SearchBar'

const statusOptions = [
  { value: 'Registered', label: 'Registrado' },
  { value: 'Delivered', label: 'Entregado' },
]

describe('SearchBar', () => {
  it('renders search input', () => {
    render(<SearchBar search="" onSearchChange={() => {}} />)
    expect(screen.getByPlaceholderText('Buscar...')).toBeInTheDocument()
  })

  it('calls onSearchChange when typing', () => {
    const onChange = vi.fn()
    render(<SearchBar search="" onSearchChange={onChange} />)
    fireEvent.change(screen.getByPlaceholderText('Buscar...'), { target: { value: 'test' } })
    expect(onChange).toHaveBeenCalledWith('test')
  })

  it('renders filter selects when provided', () => {
    render(
      <SearchBar
        search=""
        onSearchChange={() => {}}
        filters={[{ key: 'status', value: '', placeholder: 'Filtrar por estado', options: statusOptions }]}
        onFilterChange={() => {}}
      />
    )
    expect(screen.getByText('Filtrar por estado')).toBeInTheDocument()
    expect(screen.getByText('Registrado')).toBeInTheDocument()
  })

  it('calls onFilterChange when filter changes', () => {
    const onFilterChange = vi.fn()
    render(
      <SearchBar
        search=""
        onSearchChange={() => {}}
        filters={[{ key: 'status', value: '', placeholder: 'Filtrar por estado', options: statusOptions }]}
        onFilterChange={onFilterChange}
      />
    )
    const select = screen.getByRole('combobox')
    fireEvent.change(select, { target: { value: 'Delivered' } })
    expect(onFilterChange).toHaveBeenCalledWith('status', 'Delivered')
  })

  it('renders multiple filters', () => {
    render(
      <SearchBar
        search=""
        onSearchChange={() => {}}
        filters={[
          { key: 'status', value: '', placeholder: 'Estado', options: statusOptions },
          { key: 'role', value: '', placeholder: 'Rol', options: [{ value: 'Admin', label: 'Admin' }] },
        ]}
        onFilterChange={() => {}}
      />
    )
    expect(screen.getAllByRole('combobox')).toHaveLength(2)
  })
})
