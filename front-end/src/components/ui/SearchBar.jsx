export default function SearchBar({ search, onSearchChange, filters = [], onFilterChange }) {
  return (
    <div className="search-bar">
      <div className="search-bar-input">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>
        </svg>
        <input
          type="text"
          placeholder="Buscar..."
          value={search}
          onChange={e => onSearchChange(e.target.value)}
        />
      </div>
      {filters.map(f => (
        <select
          key={f.key}
          value={f.value}
          onChange={e => onFilterChange(f.key, e.target.value)}
          className="search-bar-select"
        >
          <option value="">{f.placeholder}</option>
          {f.options.map(o => (
            <option key={o.value} value={o.value}>{o.label}</option>
          ))}
        </select>
      ))}
    </div>
  )
}
