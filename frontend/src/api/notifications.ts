import apiClient from './client'
import type { Notification } from '@/types'

export async function getNotifications() {
  const res = await apiClient.get<Notification[]>('/v1/notifications')
  return res.data
}

export async function acknowledgeNotification(id: string, action: 'taken' | 'snooze' | 'skip') {
  const res = await apiClient.post(`/v1/notifications/${id}/acknowledge`, { action })
  return res.data
}

export async function markAllRead() {
  await apiClient.post('/v1/notifications/mark-all-read')
}
