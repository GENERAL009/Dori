import { useQuery } from '@tanstack/react-query'
import { getInfusions } from '@/api/infusions'

export function useInfusions(params?: { status?: string }) {
  return useQuery({
    queryKey: ['infusions', params],
    queryFn: () => getInfusions(params),
  })
}
