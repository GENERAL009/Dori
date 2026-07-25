import apiClient from './client'
import type { Medication } from '@/types'

interface MedicationListResponse {
  items: Medication[]
  total: number
  page: number
  page_size: number
}

export async function getMedications(params?: { status?: string; type?: string; search?: string }) {
  const res = await apiClient.get<MedicationListResponse>('/v1/medications', { params })
  return res.data.items
}

export async function getMedication(id: string) {
  const res = await apiClient.get<Medication>(`/v1/medications/${id}`)
  return res.data
}

export async function createMedication(data: Partial<Medication>) {
  const res = await apiClient.post<Medication>('/v1/medications', data)
  return res.data
}

export async function updateMedication(id: string, data: Partial<Medication>) {
  const res = await apiClient.put<Medication>(`/v1/medications/${id}`, data)
  return res.data
}

export async function deleteMedication(id: string) {
  await apiClient.delete(`/v1/medications/${id}`)
}
