import { Navigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'

function PrivateRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuth()

  if (isAuthenticated === null) return <div>Loading...</div>
  if (!isAuthenticated) return <Navigate to="/login" />

  return <>{children}</>
}

export default PrivateRoute
