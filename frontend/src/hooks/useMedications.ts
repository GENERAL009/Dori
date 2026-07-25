import { useQuery } from '@tanstack/react-query'
import { getMedications } from '@/api/medications'

export function useMedications(params?: { status?: string; type?: string }) {
  return useQuery({
    queryKey: ['medications', params],
    queryFn: () => getMedications(params),
  })
}
