import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import { useAuth } from './hooks/useAuth'
import AppLayout from './components/layout/AppLayout'
import Landing from './pages/Landing'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import ParcelManagement from './pages/ParcelManagement'
import Tracking from './pages/Tracking'
import Logistics from './pages/Logistics'
import ProofOfDelivery from './pages/ProofOfDelivery'
import Reports from './pages/Reports'
import UserManagement from './pages/UserManagement'
import BranchManagement from './pages/BranchManagement'
import ClientProfile from './pages/ClientProfile'
import './components/ui/components.css'
import './pages/pages.css'

function ProtectedRoute({ children, path }) {
  const { user, canAccess } = useAuth()
  if (!user) return <Navigate to="/login" replace />
  if (!canAccess(path)) return <Navigate to="/app/dashboard" replace />
  return children
}

function PublicTrackingRoute({ children }) {
  const { user } = useAuth()
  if (user && user.role !== 'Client') return <>{children}</>
  return children
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/tracking" element={<PublicTrackingRoute><Tracking /></PublicTrackingRoute>} />

          <Route path="/app" element={<AppLayout />}>
            <Route index element={<Navigate to="/app/dashboard" replace />} />
            <Route path="dashboard" element={<ProtectedRoute path="/app/dashboard"><Dashboard /></ProtectedRoute>} />
            <Route path="encomiendas" element={<ProtectedRoute path="/app/encomiendas"><ParcelManagement /></ProtectedRoute>} />
            <Route path="logistica" element={<ProtectedRoute path="/app/logistica"><Logistics /></ProtectedRoute>} />
            <Route path="comprobantes" element={<ProtectedRoute path="/app/comprobantes"><ProofOfDelivery /></ProtectedRoute>} />
            <Route path="reportes" element={<ProtectedRoute path="/app/reportes"><Reports /></ProtectedRoute>} />
            <Route path="usuarios" element={<ProtectedRoute path="/app/usuarios"><UserManagement /></ProtectedRoute>} />
            <Route path="sucursales" element={<ProtectedRoute path="/app/sucursales"><BranchManagement /></ProtectedRoute>} />
            <Route path="mis-encomiendas" element={<ProtectedRoute path="/app/mis-encomiendas"><ClientProfile /></ProtectedRoute>} />
            <Route path="perfil" element={<ProtectedRoute path="/app/perfil"><ClientProfile /></ProtectedRoute>} />
          </Route>

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}
