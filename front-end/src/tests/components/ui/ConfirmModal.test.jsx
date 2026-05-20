import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import ConfirmModal from '../../../components/ui/ConfirmModal'

describe('ConfirmModal', () => {
  it('renders nothing when not open', () => {
    const { container } = render(
      <ConfirmModal open={false} title="Test" message="msg" onConfirm={() => {}} onCancel={() => {}} />
    )
    expect(container.innerHTML).toBe('')
  })

  it('renders title and message when open', () => {
    render(
      <ConfirmModal open={true} title="Eliminar" message="Esta accion es irreversible" onConfirm={() => {}} onCancel={() => {}} />
    )
    expect(screen.getByText('Eliminar')).toBeInTheDocument()
    expect(screen.getByText('Esta accion es irreversible')).toBeInTheDocument()
  })

  it('renders default button labels', () => {
    render(
      <ConfirmModal open={true} title="Test" message="msg" onConfirm={() => {}} onCancel={() => {}} />
    )
    expect(screen.getByText('Confirmar')).toBeInTheDocument()
    expect(screen.getByText('Cancelar')).toBeInTheDocument()
  })

  it('renders custom button labels', () => {
    render(
      <ConfirmModal open={true} title="Test" message="msg" confirmLabel="Si, Eliminar" cancelLabel="No" onConfirm={() => {}} onCancel={() => {}} />
    )
    expect(screen.getByText('Si, Eliminar')).toBeInTheDocument()
    expect(screen.getByText('No')).toBeInTheDocument()
  })

  it('calls onConfirm when confirm button clicked', () => {
    const onConfirm = vi.fn()
    render(
      <ConfirmModal open={true} title="Test" message="msg" onConfirm={onConfirm} onCancel={() => {}} />
    )
    fireEvent.click(screen.getByText('Confirmar'))
    expect(onConfirm).toHaveBeenCalledOnce()
  })

  it('calls onCancel when cancel button clicked', () => {
    const onCancel = vi.fn()
    render(
      <ConfirmModal open={true} title="Test" message="msg" onConfirm={() => {}} onCancel={onCancel} />
    )
    fireEvent.click(screen.getByText('Cancelar'))
    expect(onCancel).toHaveBeenCalledOnce()
  })

  it('calls onCancel when overlay clicked', () => {
    const onCancel = vi.fn()
    const { container } = render(
      <ConfirmModal open={true} title="Test" message="msg" onConfirm={() => {}} onCancel={onCancel} />
    )
    const overlay = container.firstChild
    fireEvent.click(overlay)
    expect(onCancel).toHaveBeenCalledOnce()
  })

  it('does not call onCancel when modal content clicked', () => {
    const onCancel = vi.fn()
    render(
      <ConfirmModal open={true} title="Test" message="msg" onConfirm={() => {}} onCancel={onCancel} />
    )
    const heading = screen.getByText('Test')
    fireEvent.click(heading)
    expect(onCancel).not.toHaveBeenCalled()
  })
})
