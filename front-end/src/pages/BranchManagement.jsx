import { useState, useEffect, useCallback } from 'react'
import { branches as mockBranches } from '../data/mockData'
import { branchesApi } from '../services/api'
import DataTable from '../components/ui/DataTable'
import SearchBar from '../components/ui/SearchBar'
import ConfirmModal from '../components/ui/ConfirmModal'

const columns = (onEdit, onDelete) => [
  { key: 'name', label: 'Nombre', sortable: true },
  { key: 'city', label: 'Ciudad', sortable: true },
  { key: 'address', label: 'Direccion', sortable: true },
  { key: 'manager', label: 'Encargado', sortable: true },
  { key: 'phone', label: 'Telefono' },
  {
    key: 'active', label: 'Estado', sortable: true,
    render: (r) => (
      <span style={{ color: r.active ? 'var(--status-delivered)' : 'var(--text-muted)', fontWeight: 600, fontSize: '0.813rem' }}>
        {r.active ? 'Activo' : 'Inactivo'}
      </span>
    ),
  },
  {
    key: 'actions', label: 'Acciones',
    render: (r) => (
      <div style={{ display: 'flex', gap: 6 }}>
        <button className="btn-action" title="Editar" onClick={() => onEdit(r)}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
        </button>
        <button className="btn-action btn-action-danger" title="Eliminar" onClick={() => onDelete(r)}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
        </button>
      </div>
    ),
  },
]

const PAGE_SIZE = 10

export default function BranchManagement() {
  const [search, setSearch] = useState('')
  const [editBranch, setEditBranch] = useState(null)
  const [deleteTarget, setDeleteTarget] = useState(null)
  const [branchList, setBranchList] = useState(mockBranches)
  const [totalBranches, setTotalBranches] = useState(mockBranches.length)
  const [page, setPage] = useState(1)

  const fetchBranches = useCallback((p, s) => {
    branchesApi.list({ page: p, pageSize: PAGE_SIZE, search: s || undefined })
      .then(res => {
        setBranchList(res.data || res)
        setTotalBranches(res.total || res.length || 0)
      })
      .catch(() => {})
  }, [])

  useEffect(() => {
    fetchBranches(page, search)
  }, [page, fetchBranches])

  useEffect(() => {
    setPage(1)
    fetchBranches(1, search)
  }, [search, fetchBranches])

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-lg)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 'var(--space-md)' }}>
        <SearchBar search={search} onSearchChange={setSearch} />
        <button className="btn btn-primary" onClick={() => setEditBranch({})}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 4v16m8-8H4"/></svg>
          Nueva Sucursal
        </button>
      </div>

      <DataTable
        columns={columns(b => setEditBranch(b), b => setDeleteTarget(b))}
        data={branchList}
        pageSize={PAGE_SIZE}
        totalItems={totalBranches}
        currentPage={page}
        onPageChange={setPage}
      />

      {editBranch && (
        <div className="modal-overlay" onClick={() => setEditBranch(null)}>
          <div className="modal-content modal-wide" onClick={e => e.stopPropagation()}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-lg)' }}>
              <h3>{editBranch.id ? 'Editar Sucursal' : 'Nueva Sucursal'}</h3>
              <button className="btn-action" onClick={() => setEditBranch(null)}>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M6 18L18 6M6 6l12 12"/></svg>
              </button>
            </div>
            <div className="form-grid">
              <div className="form-field">
                <label>Nombre</label>
                <input name="name" type="text" placeholder="Nombre sucursal" defaultValue={editBranch.name || ''} />
              </div>
              <div className="form-field">
                <label>Ciudad</label>
                <input name="city" type="text" placeholder="Ciudad" defaultValue={editBranch.city || ''} />
              </div>
              <div className="form-field form-field-full">
                <label>Direccion</label>
                <input name="address" type="text" placeholder="Direccion completa" defaultValue={editBranch.address || ''} />
              </div>
              <div className="form-field">
                <label>Encargado</label>
                <input name="manager" type="text" placeholder="Nombre encargado" defaultValue={editBranch.manager || ''} />
              </div>
              <div className="form-field">
                <label>Telefono</label>
                <input name="phone" type="text" placeholder="+58 X XXXX XXXX" defaultValue={editBranch.phone || ''} />
              </div>
              <div className="form-field form-field-full" style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-sm)' }}>
                <input type="checkbox" id="branch-active" defaultChecked={editBranch.active !== false} />
                <label htmlFor="branch-active" style={{ margin: 0 }}>Sucursal Activa</label>
              </div>
            </div>
            <div className="modal-actions" style={{ marginTop: 'var(--space-lg)' }}>
              <button className="btn btn-outline" onClick={() => setEditBranch(null)}>Cancelar</button>
              <button className="btn btn-primary" onClick={() => {
                const f = document.querySelector('.modal-content.modal-wide .form-grid')
                if (!f) return
                const get = (n) => f.querySelector(`[name="${n}"]`)?.value || ''
                const checked = f.querySelector('#branch-active')?.checked ?? true
                const data = { name: get('name'), city: get('city'), address: get('address'), manager: get('manager'), phone: get('phone'), active: checked }
                if (editBranch?.id) {
                  branchesApi.update(editBranch.id, data)
                    .then(r => setBranchList(prev => prev.map(b => b.id === editBranch.id ? r : b)))
                    .catch(() => setBranchList(prev => prev.map(b => b.id === editBranch.id ? { ...b, ...data } : b)))
                } else {
                  branchesApi.create(data)
                    .then(r => {
                      setBranchList(prev => [r, ...prev.slice(0, PAGE_SIZE - 1)])
                      setTotalBranches(t => t + 1)
                    })
                    .catch(() => {
                      const newB = { ...data, id: Date.now() }
                      setBranchList(prev => [newB, ...prev.slice(0, PAGE_SIZE - 1)])
                      setTotalBranches(t => t + 1)
                    })
                }
                setEditBranch(null)
              }}>
                {editBranch.id ? 'Guardar Cambios' : 'Crear Sucursal'}
              </button>
            </div>
          </div>
        </div>
      )}

      <ConfirmModal
        open={!!deleteTarget}
        title="Eliminar Sucursal"
        message={`Estas seguro de eliminar ${deleteTarget?.name}? Esta accion no se puede deshacer.`}
        confirmLabel="Si, Eliminar"
        onConfirm={() => {
          const target = deleteTarget
          branchesApi.delete(target.id)
            .then(() => { setBranchList(prev => prev.filter(b => b.id !== target.id)); setTotalBranches(t => t - 1) })
            .catch(() => { setBranchList(prev => prev.filter(b => b.id !== target.id)); setTotalBranches(t => t - 1) })
          setDeleteTarget(null)
        }}
        onCancel={() => setDeleteTarget(null)}
      />
    </div>
  )
}