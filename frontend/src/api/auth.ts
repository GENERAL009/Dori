import apiClient from './client'

export async function loginWithPin(pin: string) {
  const res = await apiClient.post('/v1/auth/login', { pin })
  return res.data
}

export async function selectProfile(userId: string) {
  const res = await apiClient.post('/v1/auth/select-profile', { user_id: userId })
  return res.data
}

export async function refreshToken(token: string) {
  const res = await apiClient.post('/v1/auth/refresh', { refresh_token: token })
  return res.data
}
