import { describe, it, expect } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import DataTable from '../../../components/ui/DataTable'

const columns = [
  { key: 'name', label: 'Nombre', sortable: true },
  { key: 'age', label: 'Edad', sortable: true },
  { key: 'role', label: 'Rol' },
]

const data = [
  { id: 1, name: 'Ana', age: 30, role: 'Admin' },
  { id: 2, name: 'Luis', age: 25, role: 'Driver' },
  { id: 3, name: 'Carlos', age: 35, role: 'Operator' },
  { id: 4, name: 'Maria', age: 28, role: 'Client' },
  { id: 5, name: 'Pedro', age: 32, role: 'Driver' },
]

describe('DataTable', () => {
  it('renders all columns in header', () => {
    render(<DataTable columns={columns} data={data} />)
    expect(screen.getByText('Nombre')).toBeInTheDocument()
    expect(screen.getByText('Edad')).toBeInTheDocument()
    expect(screen.getByText('Rol')).toBeInTheDocument()
  })

  it('renders row data', () => {
    render(<DataTable columns={columns} data={data} />)
    expect(screen.getByText('Ana')).toBeInTheDocument()
    expect(screen.getByText('Luis')).toBeInTheDocument()
  })

  it('sorts by name ascending on click', () => {
    render(<DataTable columns={columns} data={data} />)
    fireEvent.click(screen.getByText('Nombre'))
    const rows = screen.getAllByRole('row')
    expect(rows[1]).toHaveTextContent('Ana')
    expect(rows[2]).toHaveTextContent('Carlos')
  })

  it('sorts by age descending on double click', () => {
    render(<DataTable columns={columns} data={data} />)
    fireEvent.click(screen.getByText('Edad'))
    fireEvent.click(screen.getByText('Edad'))
    const rows = screen.getAllByRole('row')
    expect(rows[1]).toHaveTextContent('35')
    expect(rows[5]).toHaveTextContent('25')
  })

  it('shows pagination when data exceeds pageSize', () => {
    render(<DataTable columns={columns} data={data} pageSize={2} />)
    expect(screen.getByText('1 / 3')).toBeInTheDocument()
    expect(screen.getByText('Siguiente')).toBeInTheDocument()
    expect(screen.getByText('Anterior')).toBeInTheDocument()
  })

  it('does not show pagination when data fits in one page', () => {
    render(<DataTable columns={columns} data={data} pageSize={10} />)
    expect(screen.queryByText('1 / 1')).not.toBeInTheDocument()
  })

  it('navigates pages', () => {
    render(<DataTable columns={columns} data={data} pageSize={2} />)
    expect(screen.getByText('Ana')).toBeInTheDocument()
    fireEvent.click(screen.getByText('Siguiente'))
    expect(screen.getByText('Carlos')).toBeInTheDocument()
    expect(screen.getByText('2 / 3')).toBeInTheDocument()
  })

  it('shows empty state when no data', () => {
    render(<DataTable columns={columns} data={[]} />)
    expect(screen.getByText('No hay datos disponibles')).toBeInTheDocument()
  })

  it('uses custom render function', () => {
    const cols = [
      { key: 'name', label: 'Nombre', render: (row) => <strong>{row.name}</strong> },
    ]
    render(<DataTable columns={cols} data={[{ id: 1, name: 'Ana' }]} />)
    expect(screen.getByText('Ana').tagName).toBe('STRONG')
  })

  describe('server-side pagination', () => {
    it('shows server page info when onPageChange is provided', () => {
      render(
        <DataTable
          columns={columns}
          data={data.slice(0, 2)}
          pageSize={2}
          totalItems={10}
          currentPage={1}
          onPageChange={() => {}}
        />
      )
      expect(screen.getByText('1 / 5')).toBeInTheDocument()
    })

    it('disables previous on first page in server mode', () => {
      render(
        <DataTable
          columns={columns}
          data={[]}
          pageSize={2}
          totalItems={10}
          currentPage={1}
          onPageChange={() => {}}
        />
      )
      expect(screen.getByText('Anterior')).toBeDisabled()
    })

    it('disables next on last page in server mode', () => {
      render(
        <DataTable
          columns={columns}
          data={[]}
          pageSize={2}
          totalItems={10}
          currentPage={5}
          onPageChange={() => {}}
        />
      )
      expect(screen.getByText('Siguiente')).toBeDisabled()
    })
  })
})
