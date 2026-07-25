import axios from 'axios'
import { useAuthStore } from '@/stores/authStore'
import { API_BASE_URL } from '@/lib/constants'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
})

apiClient.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  const activeUserId = useAuthStore.getState().activeUserId
  if (activeUserId) {
    config.headers['X-User-Id'] = activeUserId
  }
  return config
})

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      const refreshToken = useAuthStore.getState().refreshToken
      if (refreshToken) {
        try {
          const res = await axios.post(`${API_BASE_URL}/v1/auth/refresh`, { refresh_token: refreshToken })
          useAuthStore.getState().setAuth(res.data.access_token, res.data.refresh_token, useAuthStore.getState().users)
          error.config.headers.Authorization = `Bearer ${res.data.access_token}`
          return apiClient(error.config)
        } catch {
          useAuthStore.getState().logout()
        }
      } else {
        useAuthStore.getState().logout()
      }
    }
    return Promise.reject(error)
  }
)

export default apiClient
