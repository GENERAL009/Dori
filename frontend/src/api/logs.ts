import apiClient from './client'
import type { MedicationLog } from '@/types'

export async function getLogs(params?: { date?: string; medication_id?: string }) {
  const res = await apiClient.get<MedicationLog[]>('/v1/logs/today', { params })
  return res.data
}

function buildScheduledTime(timeStr: string): string {
  const today = new Date()
  const [h, m] = timeStr.split(':')
  const year = today.getFullYear()
  const month = String(today.getMonth() + 1).padStart(2, '0')
  const day = String(today.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}T${h.padStart(2, '0')}:${m.padStart(2, '0')}:00+05:00`
}

export async function markMedicationTaken(medicationId: string, scheduledTime: string) {
  const isoTime = buildScheduledTime(scheduledTime)

  const res = await apiClient.post<MedicationLog>(`/v1/logs/medication/${medicationId}/taken`, null, {
    params: { scheduled_time: isoTime }
  })
  return res.data
}

export async function markMedicationSkipped(medicationId: string, scheduledTime: string) {
  const isoTime = buildScheduledTime(scheduledTime)

  const res = await apiClient.post<MedicationLog>(`/v1/logs/medication/${medicationId}/skip`, null, {
    params: { scheduled_time: isoTime }
  })
  return res.data
}
