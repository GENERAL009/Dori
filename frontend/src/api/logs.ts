import apiClient from './client'
import type { MedicationLog, LogStatus } from '@/types'

export async function getLogs(params?: { date?: string; medication_id?: string }) {
  const res = await apiClient.get<MedicationLog[]>('/v1/logs', { params })
  return res.data
}

export async function createLog(data: { medication_id: string; scheduled_time: string; status: LogStatus; notes?: string }) {
  const res = await apiClient.post<MedicationLog>('/v1/logs', data)
  return res.data
}

export async function markMedicationTaken(medicationId: string, scheduledTime: string) {
  return createLog({ medication_id: medicationId, scheduled_time: scheduledTime, status: 'taken' })
}

export async function markMedicationMissed(medicationId: string, scheduledTime: string) {
  return createLog({ medication_id: medicationId, scheduled_time: scheduledTime, status: 'missed' })
}

export async function markMedicationSkipped(medicationId: string, scheduledTime: string) {
  return createLog({ medication_id: medicationId, scheduled_time: scheduledTime, status: 'skipped' })
}
