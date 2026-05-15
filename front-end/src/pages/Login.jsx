import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      const user = await login(email, password)
      if (user) {
        const route = user.role === 'Client' ? '/app/mis-encomiendas' : user.role === 'Driver' ? '/app/mis-entregas' : '/app/dashboard'
        navigate(route)
      } else {
        setError('Credenciales inválidas. Prueba: admin@awen.com / 123456')
      }
    } catch {
      setError('Error de conexión con el servidor')
    }
  }

  return (
    <div className="login-page">
      <div className="login-page-inner">
        <div className="auth-back-row">
          <Link to="/" className="auth-back-link">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
              <path d="M19 12H5M12 19l-7-7 7-7" />
            </svg>
            Volver al inicio
          </Link>
        </div>
        <div className="login-card">
        <div className="login-logo">A</div>
        <h1 className="login-title">AWEN</h1>
        <p className="login-subtitle">Sistema de Gestión de Encomiendas</p>
        <form onSubmit={handleSubmit}>
          <div className="login-field">
            <label>Correo electrónico</label>
            <input
              type="email"
              placeholder="admin@awen.com"
              value={email}
              onChange={e => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="login-field">
            <label>Contraseña</label>
            <input
              type="password"
              placeholder="••••••"
              value={password}
              onChange={e => setPassword(e.target.value)}
              required
            />
          </div>
          {error && <p className="login-error">{error}</p>}
          <button type="submit" className="btn btn-primary login-btn">Iniciar Sesión</button>
          <a href="#" className="login-forgot">¿Olvidaste tu contraseña?</a>
        </form>
        <div className="login-hint">
          <p>Credenciales de prueba:</p>
          <code>admin@awen.com / 123456</code>
          <code>operador.carlos@awen.com / 123456</code>
          <code>conductor.pedro@awen.com / 123456</code>
          <code>juan@email.com / 123456</code>
        </div>
      </div>
      </div>
    </div>
  )
}
