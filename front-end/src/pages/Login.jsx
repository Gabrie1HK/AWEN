import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = (e) => {
    e.preventDefault()
    setError('')
    const user = login(email, password)
    if (user) {
      navigate(user.role === 'Client' ? '/tracking' : '/app/dashboard')
    } else {
      setError('Credenciales inválidas. Prueba: admin@awen.cl / 123456')
    }
  }

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="login-logo">A</div>
        <h1 className="login-title">AWEN</h1>
        <p className="login-subtitle">Sistema de Gestión de Encomiendas</p>
        <form onSubmit={handleSubmit}>
          <div className="login-field">
            <label>Correo electrónico</label>
            <input
              type="email"
              placeholder="admin@awen.cl"
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
          <code>admin@awen.cl / 123456</code>
          <code>operador.carlos@awen.cl / 123456</code>
          <code>conductor.pedro@awen.cl / 123456</code>
          <code>juan@email.com / 123456</code>
        </div>
      </div>
    </div>
  )
}
