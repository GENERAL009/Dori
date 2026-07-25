import apiClient from './client'
import type { DashboardData } from '@/types'

export async function getDashboard() {
  const res = await apiClient.get<DashboardData>('/v1/dashboard')
  return res.data
}
