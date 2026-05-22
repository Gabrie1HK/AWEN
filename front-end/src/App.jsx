import { lazy, Suspense } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import { useAuth } from './hooks/useAuth'
import ErrorBoundary from './components/ui/ErrorBoundary'
import AppLayout from './components/layout/AppLayout'
import './components/ui/components.css'
import './pages/pages.css'

const Landing = lazy(() => import('./pages/Landing'))
const Login = lazy(() => import('./pages/Login'))
const Dashboard = lazy(() => import('./pages/Dashboard'))
const ParcelManagement = lazy(() => import('./pages/ParcelManagement'))
const Tracking = lazy(() => import('./pages/Tracking'))
const Logistics = lazy(() => import('./pages/Logistics'))
const ProofOfDelivery = lazy(() => import('./pages/ProofOfDelivery'))
const Reports = lazy(() => import('./pages/Reports'))
const UserManagement = lazy(() => import('./pages/UserManagement'))
const BranchManagement = lazy(() => import('./pages/BranchManagement'))
const ClientProfile = lazy(() => import('./pages/ClientProfile'))
const DriverDashboard = lazy(() => import('./pages/DriverDashboard'))

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
        <ErrorBoundary>
        <Suspense fallback={
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '100vh', padding: 32, color: 'var(--text-muted)', fontSize: '0.875rem' }}>
            <div className="spinner" />
          </div>
        }>
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
            <Route path="mis-entregas" element={<ProtectedRoute path="/app/mis-entregas"><DriverDashboard /></ProtectedRoute>} />
            <Route path="perfil" element={<ProtectedRoute path="/app/perfil"><ClientProfile /></ProtectedRoute>} />
          </Route>

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
        </Suspense>
        </ErrorBoundary>
      </AuthProvider>
    </BrowserRouter>
  )
}
