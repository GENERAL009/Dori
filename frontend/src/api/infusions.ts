import apiClient from './client'
import type { Infusion } from '@/types'

interface InfusionListResponse {
  items: Infusion[]
  total: number
  page: number
  page_size: number
}

export async function getInfusions(params?: { status?: string }) {
  const res = await apiClient.get<InfusionListResponse>('/v1/infusions', { params })
  return res.data.items
}

export async function getInfusion(id: string) {
  const res = await apiClient.get<Infusion>(`/v1/infusions/${id}`)
  return res.data
}

export async function createInfusion(data: Partial<Infusion>) {
  const res = await apiClient.post<Infusion>('/v1/infusions', data)
  return res.data
}

export async function updateInfusion(id: string, data: Partial<Infusion>) {
  const res = await apiClient.put<Infusion>(`/v1/infusions/${id}`, data)
  return res.data
}

export async function completeInfusionSession(id: string) {
  const res = await apiClient.post(`/v1/infusions/${id}/complete-session`)
  return res.data
}
