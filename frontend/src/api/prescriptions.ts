import apiClient from './client'
import type { Prescription } from '@/types'

export async function getPrescriptions() {
  const res = await apiClient.get<Prescription[]>('/v1/prescriptions')
  return res.data
}

export async function getPrescription(id: string) {
  const res = await apiClient.get<Prescription>(`/v1/prescriptions/${id}`)
  return res.data
}

export async function createPrescription(data: FormData) {
  const res = await apiClient.post<Prescription>('/v1/prescriptions', data, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return res.data
}

export async function deletePrescription(id: string) {
  await apiClient.delete(`/v1/prescriptions/${id}`)
}
