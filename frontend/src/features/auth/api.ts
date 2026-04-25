import apiClient from '../../lib/axios'
import type { LoginRequest, LoginResponse } from './types'

export const login = async (data: LoginRequest): Promise<LoginResponse> => {
  const response = await apiClient.post<LoginResponse>('/auth/login', data)
  return response.data
}

export const logout = async (): Promise<void> => {
  await apiClient.post('/auth/logout')
}
