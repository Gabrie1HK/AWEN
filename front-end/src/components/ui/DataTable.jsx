import { useState, useMemo } from 'react'

export default function DataTable({ columns, data, pageSize = 10, totalItems, onPageChange, currentPage: currentPageProp = 1 }) {
  const isServerPaginated = Boolean(onPageChange)
  const [clientPage, setClientPage] = useState(1)
  const [sortKey, setSortKey] = useState(null)
  const [sortDir, setSortDir] = useState('asc')
  const safeData = Array.isArray(data) ? data : []

  const currentPage = isServerPaginated ? currentPageProp : clientPage

  const sorted = useMemo(() => {
    if (!sortKey) return safeData
    return [...safeData].sort((a, b) => {
      const av = a[sortKey], bv = b[sortKey]
      if (av == null) return 1
      if (bv == null) return -1
      const cmp = typeof av === 'string' ? av.localeCompare(bv) : av - bv
      return sortDir === 'asc' ? cmp : -cmp
    })
  }, [data, sortKey, sortDir])

  const totalPages = isServerPaginated
    ? Math.ceil(totalItems / pageSize)
    : Math.ceil(sorted.length / pageSize)

  const paged = isServerPaginated ? sorted : sorted.slice((currentPage - 1) * pageSize, currentPage * pageSize)

  const handleSort = (key) => {
    if (sortKey === key) {
      setSortDir(d => d === 'asc' ? 'desc' : 'asc')
    } else {
      setSortKey(key)
      setSortDir('asc')
    }
  }

  const goToPage = (p) => {
    if (isServerPaginated) {
      onPageChange(p)
    } else {
      setClientPage(p)
    }
  }

  const prevPage = () => goToPage(currentPage - 1)
  const nextPage = () => goToPage(currentPage + 1)

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
                    <span style={{ marginLeft: 4 }}>{sortDir === 'asc' ? '\u25B2' : '\u25BC'}</span>
                  )}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {paged.map((row, i) => (
              <tr key={row.id || i}>
                {columns.map(col => (
                  <td key={col.key} data-label={col.label}>
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
          <button disabled={currentPage <= 1} onClick={prevPage}>Anterior</button>
          <span>{currentPage} / {totalPages}</span>
          <button disabled={currentPage >= totalPages} onClick={nextPage}>Siguiente</button>
        </div>
      )}
    </div>
  )
}
