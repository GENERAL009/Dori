import apiClient from './client'
import type { Statistics } from '@/types'

export async function getStatistics(period?: 'today' | 'week' | 'month') {
  const res = await apiClient.get<Statistics>('/v1/statistics', { params: { period } })
  return res.data
}
