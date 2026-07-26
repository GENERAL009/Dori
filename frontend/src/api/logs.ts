import apiClient from './client'
import type { MedicationLog } from '@/types'

export async function getLogs(params?: { date?: string; medication_id?: string }) {
  const res = await apiClient.get<MedicationLog[]>('/v1/logs/today', { params })
  return res.data
}

export async function markMedicationTaken(medicationId: string, scheduledTime: string) {
  const today = new Date()
  const [h, m] = scheduledTime.split(':')
  const dt = new Date(today.getFullYear(), today.getMonth(), today.getDate(), parseInt(h), parseInt(m))
  const isoTime = dt.toISOString()

  const res = await apiClient.post<MedicationLog>(`/v1/logs/medication/${medicationId}/taken`, null, {
    params: { scheduled_time: isoTime }
  })
  return res.data
}

export async function markMedicationSkipped(medicationId: string, scheduledTime: string) {
  const today = new Date()
  const [h, m] = scheduledTime.split(':')
  const dt = new Date(today.getFullYear(), today.getMonth(), today.getDate(), parseInt(h), parseInt(m))
  const isoTime = dt.toISOString()

  const res = await apiClient.post<MedicationLog>(`/v1/logs/medication/${medicationId}/skip`, null, {
    params: { scheduled_time: isoTime }
  })
  return res.data
}
