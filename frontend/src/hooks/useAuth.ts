import { useState, useEffect } from 'react'
import type { User } from '../features/user/types'
import apiClient from '../lib/axios'

export const useAuth = () => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null)

  useEffect(() => {
    apiClient.get<User>('/auth/user')
      .then(() => setIsAuthenticated(true))
      .catch(() => setIsAuthenticated(false))
  }, [])

  return { isAuthenticated }
}
