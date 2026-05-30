import { useState, useEffect, useCallback } from 'react'
import { usersApi, branchesApi } from '../services/api'
import RoleBadge from '../components/ui/RoleBadge'
import DataTable from '../components/ui/DataTable'
import SearchBar from '../components/ui/SearchBar'
import ConfirmModal from '../components/ui/ConfirmModal'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import ErrorBanner from '../components/ui/ErrorBanner'
import { useApi } from '../hooks/useApi'

const roleOptions = [
  { value: 'Admin', label: 'Admin' },
  { value: 'Warehouse Operator', label: 'Operador' },
  { value: 'Driver', label: 'Conductor' },
  { value: 'Client', label: 'Cliente' },
]

const columns = (onEdit, onDelete, onResetPassword) => [
  { key: 'name', label: 'Nombre', sortable: true },
  { key: 'email', label: 'Email', sortable: true },
  { key: 'role', label: 'Rol', render: (r) => <RoleBadge role={r.role} /> },
  { key: 'branch', label: 'Sucursal', sortable: true },
  { key: 'active', label: 'Estado', sortable: true, render: (r) => (
    <span style={{ color: r.active ? 'var(--status-delivered)' : 'var(--text-muted)', fontWeight: 600, fontSize: '0.813rem' }}>
      {r.active ? 'Activo' : 'Inactivo'}
    </span>
  )},
  { key: 'lastLogin', label: 'Ultimo Acceso', sortable: true },
  {
    key: 'actions', label: 'Acciones',
    render: (r) => (
      <div style={{ display: 'flex', gap: 6 }}>
        <button className="btn-action" title="Editar" onClick={() => onEdit(r)}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
        </button>
        <button className="btn-action" title="Cambiar clave" onClick={() => onResetPassword(r)}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0110 0v4"/></svg>
        </button>
        <button className="btn-action btn-action-danger" title="Eliminar" onClick={() => onDelete(r)}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
        </button>
      </div>
    ),
  },
]

const PAGE_SIZE = 10
export default function UserManagement() {
  const [search, setSearch] = useState('')
  const [roleFilter, setRoleFilter] = useState('')
  const [editUser, setEditUser] = useState(null)
  const [deleteTarget, setDeleteTarget] = useState(null)
  const [passwordTarget, setPasswordTarget] = useState(null)

  const [userList, setUserList] = useState([])
  const [branchList, setBranchList] = useState([])
  const [totalUsers, setTotalUsers] = useState(0)
  const [page, setPage] = useState(1)
  const { loading, error, setError, execute } = useApi()

  const fetchUsers = useCallback((p, s, r) => {
    execute(() => usersApi.list({ page: p, pageSize: PAGE_SIZE, search: s || undefined, role: r || undefined }))
      .then(res => {
        if (res) {
          setUserList(res.data || res)
          setTotalUsers(res.total || res.length || 0)
        }
      })
  }, [execute])

  useEffect(() => {
    fetchUsers(page, search, roleFilter)
  }, [page, fetchUsers])

  useEffect(() => {
    setPage(1)
    fetchUsers(1, search, roleFilter)
  }, [search, roleFilter, fetchUsers])

  useEffect(() => {
    execute(() => branchesApi.list({ pageSize: 50 }))
      .then(res => { if (res) setBranchList(res.data || res) })
  }, [])

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-lg)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 'var(--space-md)' }}>
        <SearchBar
          search={search} onSearchChange={setSearch}
          filters={[{ key: 'role', value: roleFilter, placeholder: 'Filtrar por rol', options: roleOptions }]}
          onFilterChange={(k, v) => setRoleFilter(v)}
        />
        <button className="btn btn-primary" onClick={() => setEditUser({})}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 4v16m8-8H4"/></svg>
          Nuevo Usuario
        </button>
      </div>

      <ErrorBanner message={error} onDismiss={() => setError(null)} />
      {loading ? <LoadingSpinner /> : (
      <DataTable
        columns={columns(u => setEditUser(u), u => setDeleteTarget(u), u => setPasswordTarget(u))}
        data={userList}
        pageSize={PAGE_SIZE}
        totalItems={totalUsers}
        currentPage={page}
        onPageChange={setPage}
      />
      )}

      {editUser && (
        <div className="modal-overlay" onClick={() => setEditUser(null)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-lg)' }}>
              <h3>{editUser.id ? 'Editar Usuario' : 'Nuevo Usuario'}</h3>
              <button className="btn-action" onClick={() => setEditUser(null)}>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M6 18L18 6M6 6l12 12"/></svg>
              </button>
            </div>
            <div className="form-grid">
              <div className="form-field">
                <label>Nombre</label>
                <input name="name" type="text" placeholder="Nombre completo" defaultValue={editUser.name || ''} />
              </div>
              <div className="form-field">
                <label>Email</label>
                <input name="email" type="email" placeholder="correo@awen.com" defaultValue={editUser.email || ''} />
              </div>
              <div className="form-field">
                <label>Rol</label>
                <select name="role" defaultValue={editUser.role || ''}>
                  <option value="">Seleccionar...</option>
                  {roleOptions.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
                </select>
              </div>
              <div className="form-field">
                <label>Sucursal</label>
                <select name="branch" defaultValue={editUser.branch || ''}>
                  <option value="">Sin sucursal</option>
                  {branchList.filter(b => b.active).map(b => <option key={b.id} value={b.name}>{b.name}</option>)}
                </select>
              </div>
              <div className="form-field form-field-full" style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-sm)' }}>
                <input type="checkbox" id="active-toggle" defaultChecked={editUser.active !== false} />
                <label htmlFor="active-toggle" style={{ margin: 0 }}>Usuario Activo</label>
              </div>
            </div>
            <div className="modal-actions" style={{ marginTop: 'var(--space-lg)' }}>
              <button className="btn btn-outline" onClick={() => setEditUser(null)}>Cancelar</button>
              <button className="btn btn-primary" onClick={() => {
                const f = document.querySelector('.modal-content .form-grid')
                if (!f) return
                const get = (n) => f.querySelector(`[name="${n}"]`)?.value || ''
                const checked = f.querySelector('#active-toggle')?.checked ?? true
                const data = { name: get('name'), email: get('email'), role: get('role'), branch: get('branch'), active: checked }
                if (editUser?.id) {
                  usersApi.update(editUser.id, data)
                    .then(r => setUserList(prev => prev.map(u => u.id === editUser.id ? r : u)))
                    .catch(() => setError('No se pudo actualizar el usuario'))
                } else {
                  usersApi.create(data)
                    .then(r => {
                      setUserList(prev => [r, ...prev.slice(0, PAGE_SIZE - 1)])
                      setTotalUsers(t => t + 1)
                    })
                    .catch(() => setError('No se pudo crear el usuario'))
                }
                setEditUser(null)
              }}>
                {editUser.id ? 'Guardar Cambios' : 'Crear Usuario'}
              </button>
            </div>
          </div>
        </div>
      )}

      {passwordTarget && (
        <div className="modal-overlay" onClick={() => setPasswordTarget(null)}>
          <div className="modal-content" onClick={e => e.stopPropagation()} style={{ maxWidth: 420 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-lg)' }}>
              <h3>Cambiar Clave</h3>
              <button className="btn-action" onClick={() => setPasswordTarget(null)}>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M6 18L18 6M6 6l12 12"/></svg>
              </button>
            </div>
            <p style={{ marginBottom: 'var(--space-md)', fontSize: '0.875rem', color: 'var(--text-muted)' }}>
              Nueva clave para <strong>{passwordTarget.name}</strong>
            </p>
            <div className="form-grid">
              <div className="form-field form-field-full">
                <label>Nueva clave</label>
                <input id="pw-new" type="password" placeholder="Min. 6 caracteres" />
              </div>
              <div className="form-field form-field-full">
                <label>Confirmar clave</label>
                <input id="pw-confirm" type="password" placeholder="Repite la clave" />
              </div>
            </div>
            <div className="modal-actions" style={{ marginTop: 'var(--space-lg)' }}>
              <button className="btn btn-outline" onClick={() => setPasswordTarget(null)}>Cancelar</button>
              <button className="btn btn-primary" onClick={() => {
                const pw = document.getElementById('pw-new')?.value
                const confirm = document.getElementById('pw-confirm')?.value
                if (!pw || pw.length < 6) { setError('La clave debe tener al menos 6 caracteres'); return }
                if (pw !== confirm) { setError('Las claves no coinciden'); return }
                usersApi.resetPassword(passwordTarget.id, pw)
                  .then(() => setPasswordTarget(null))
                  .catch(() => setError('No se pudo cambiar la clave'))
              }}>
                Guardar Clave
              </button>
            </div>
          </div>
        </div>
      )}

      <ConfirmModal
        open={!!deleteTarget}
        title="Eliminar Usuario"
        message={`Estas seguro de eliminar a ${deleteTarget?.name}? Esta accion no se puede deshacer.`}
        confirmLabel="Si, Eliminar"
        onConfirm={() => {
          const target = deleteTarget
          usersApi.delete(target.id)
            .then(() => { setUserList(prev => prev.filter(u => u.id !== target.id)); setTotalUsers(t => t - 1) })
            .catch(() => setError('No se pudo eliminar el usuario'))
          setDeleteTarget(null)
        }}
        onCancel={() => setDeleteTarget(null)}
      />
    </div>
  )
}
