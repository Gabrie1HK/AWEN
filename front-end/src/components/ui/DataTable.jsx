import { useState, useMemo } from 'react'

export default function DataTable({ columns, data, pageSize = 10 }) {
  const [page, setPage] = useState(0)
  const [sortKey, setSortKey] = useState(null)
  const [sortDir, setSortDir] = useState('asc')

  const sorted = useMemo(() => {
    if (!sortKey) return data
    return [...data].sort((a, b) => {
      const av = a[sortKey], bv = b[sortKey]
      if (av == null) return 1
      if (bv == null) return -1
      const cmp = typeof av === 'string' ? av.localeCompare(bv) : av - bv
      return sortDir === 'asc' ? cmp : -cmp
    })
  }, [data, sortKey, sortDir])

  const totalPages = Math.ceil(sorted.length / pageSize)
  const paged = sorted.slice(page * pageSize, (page + 1) * pageSize)

  const handleSort = (key) => {
    if (sortKey === key) {
      setSortDir(d => d === 'asc' ? 'desc' : 'asc')
    } else {
      setSortKey(key)
      setSortDir('asc')
    }
  }

  return (
    <div className="data-table-wrapper">
      <div className="data-table-scroll">
        <table className="data-table">
          <thead>
            <tr>
              {columns.map(col => (
                <th
                  key={col.key}
                  onClick={col.sortable ? () => handleSort(col.key) : undefined}
                  style={{ cursor: col.sortable ? 'pointer' : 'default', userSelect: 'none' }}
                >
                  {col.label}
                  {sortKey === col.key && (
                    <span style={{ marginLeft: 4 }}>{sortDir === 'asc' ? '▲' : '▼'}</span>
                  )}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {paged.map((row, i) => (
              <tr key={row.id || i}>
                {columns.map(col => (
                  <td key={col.key}>
                    {col.render ? col.render(row) : row[col.key]}
                  </td>
                ))}
              </tr>
            ))}
            {paged.length === 0 && (
              <tr>
                <td colSpan={columns.length} style={{ textAlign: 'center', padding: '32px', color: 'var(--text-muted)' }}>
                  No hay datos disponibles
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      {totalPages > 1 && (
        <div className="data-table-pagination">
          <button disabled={page === 0} onClick={() => setPage(p => p - 1)}>Anterior</button>
          <span>{page + 1} / {totalPages}</span>
          <button disabled={page >= totalPages - 1} onClick={() => setPage(p => p + 1)}>Siguiente</button>
        </div>
      )}
    </div>
  )
}
