import { Component } from 'react'

export default class ErrorBoundary extends Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback
      }
      return (
        <div style={{
          display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
          minHeight: '60vh', padding: 32, textAlign: 'center', color: 'var(--text-muted, #6b7280)'
        }}>
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ marginBottom: 16 }}>
            <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
          <h3 style={{ marginBottom: 8, color: 'var(--text-primary, #111827)' }}>Algo salio mal</h3>
          <p style={{ marginBottom: 16, maxWidth: 400 }}>Ocurrio un error inesperado al cargar esta seccion. Intenta recargar la pagina.</p>
          <button className="btn btn-primary" onClick={() => { this.setState({ hasError: false, error: null }); window.location.reload() }}>
            Recargar Pagina
          </button>
        </div>
      )
    }
    return this.props.children
  }
}
