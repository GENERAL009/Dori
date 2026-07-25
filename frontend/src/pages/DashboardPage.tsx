import { useMutation, useQueryClient, useQuery } from '@tanstack/react-query'
import { getDashboard } from '@/api/dashboard'
import { markMedicationTaken, markMedicationSkipped } from '@/api/logs'
import { useAuthStore } from '@/stores/authStore'
import { Card, CardContent } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { toast } from '@/components/ui/toaster'
import { MEDICATION_TYPES } from '@/lib/constants'
import type { MedicationType } from '@/types'

interface MedicationSummaryItem {
  id: string
  name: string
  type: MedicationType
  dosage: string
  time: string
  status: string
  instruction: string | null
}

interface InfusionSummaryItem {
  id: string
  name: string
  volume: string
  session_number: number
  total_sessions: number
  status: string
}

interface DashboardResponse {
  date: string
  user_name: string
  user_role: string
  total_medications_today: number
  completed_medications: number
  remaining_medications: number
  missed_medications: number
  total_infusions_today: number
  completed_infusions: number
  remaining_infusions: number
  vitamins_count: number
  injections_count: number
  days_until_treatment_ends: number | null
  treatment_progress_percentage: number
  upcoming_medications: MedicationSummaryItem[]
  upcoming_infusions: InfusionSummaryItem[]
}

export default function DashboardPage() {
  const { activeProfile } = useAuthStore()
  const queryClient = useQueryClient()

  const { data, isLoading } = useQuery<DashboardResponse>({
    queryKey: ['dashboard', activeProfile],
    queryFn: getDashboard,
    refetchInterval: 60000,
  })

  const takeMutation = useMutation({
    mutationFn: (med: MedicationSummaryItem) => markMedicationTaken(med.id, med.time),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['dashboard'] })
      toast({ title: 'Dori qabul qilindi', variant: 'success' })
    },
  })

  const skipMutation = useMutation({
    mutationFn: (med: MedicationSummaryItem) => markMedicationSkipped(med.id, med.time),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['dashboard'] })
      toast({ title: "O'tkazib yuborildi" })
    },
  })

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-2 border-primary-500 border-t-transparent rounded-full animate-spin" />
      </div>
    )
  }

  const today = new Date()
  const months = ['Yanvar', 'Fevral', 'Mart', 'Aprel', 'May', 'Iyun', 'Iyul', 'Avgust', 'Sentyabr', 'Oktyabr', 'Noyabr', 'Dekabr']

  return (
    <div className="space-y-4 sm:space-y-6">
      <div>
        <h1 className="text-lg sm:text-xl font-bold text-gray-900">
          Bugun, {today.getDate()} {months[today.getMonth()]}
        </h1>
        <p className="text-gray-500 text-sm mt-0.5">
          {data?.user_name || (activeProfile === 'male' ? 'Erkak' : 'Ayol')} profili
        </p>
      </div>

      <div className="grid grid-cols-2 gap-2 sm:gap-3 sm:grid-cols-4">
        <Card>
          <CardContent className="p-3 sm:p-4">
            <p className="text-xl sm:text-2xl font-bold text-primary-600">{data?.total_medications_today || 0}</p>
            <p className="text-[11px] sm:text-xs text-gray-500 mt-0.5">Bugungi dorilar</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-3 sm:p-4">
            <p className="text-xl sm:text-2xl font-bold text-green-600">{data?.completed_medications || 0}</p>
            <p className="text-[11px] sm:text-xs text-gray-500 mt-0.5">Bajarilgan</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-3 sm:p-4">
            <p className="text-xl sm:text-2xl font-bold text-yellow-600">{data?.remaining_medications || 0}</p>
            <p className="text-[11px] sm:text-xs text-gray-500 mt-0.5">Qolgan</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-3 sm:p-4">
            <p className="text-xl sm:text-2xl font-bold text-blue-600">{data?.days_until_treatment_ends ?? 0}</p>
            <p className="text-[11px] sm:text-xs text-gray-500 mt-0.5">Kun qoldi</p>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardContent className="p-3 sm:p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-700">Davolash progressi</span>
            <span className="text-sm font-bold text-primary-600">{data?.treatment_progress_percentage || 0}%</span>
          </div>
          <Progress value={data?.treatment_progress_percentage || 0} />
        </CardContent>
      </Card>

      <div>
        <h2 className="text-base sm:text-lg font-semibold text-gray-900 mb-2 sm:mb-3">Bugungi dorilar</h2>
        <div className="space-y-2">
          {(!data?.upcoming_medications || data.upcoming_medications.length === 0) && (
            <Card>
              <CardContent className="p-6 text-center text-gray-500">
                Bugun dori yo'q
              </CardContent>
            </Card>
          )}
          {data?.upcoming_medications?.map((med, idx) => (
            <Card key={`${med.id}-${med.time}-${idx}`} className={med.status === 'completed' ? 'opacity-60' : ''}>
              <CardContent className="p-3 sm:p-4">
                <div className="flex items-start justify-between gap-2">
                  <div className="flex items-start gap-2 sm:gap-3 flex-1 min-w-0">
                    <div className={`w-2.5 h-2.5 sm:w-3 sm:h-3 rounded-full flex-shrink-0 mt-1.5 ${
                      med.status === 'completed' ? 'bg-green-500' :
                      med.status === 'missed' ? 'bg-red-500' :
                      'bg-yellow-500'
                    }`} />
                    <div className="flex-1 min-w-0">
                      <p className="font-medium text-gray-900 text-sm sm:text-base truncate">{med.name}</p>
                      <div className="flex items-center gap-1.5 sm:gap-2 mt-0.5 flex-wrap">
                        <span className="text-xs text-gray-500">{med.dosage}</span>
                        <Badge className={`text-[10px] px-1.5 py-0 ${MEDICATION_TYPES[med.type]?.color || 'bg-gray-100 text-gray-700'}`}>
                          {MEDICATION_TYPES[med.type]?.label || med.type}
                        </Badge>
                      </div>
                      {med.instruction && (
                        <p className="text-[11px] sm:text-xs text-gray-400 mt-0.5 truncate">{med.instruction}</p>
                      )}
                    </div>
                  </div>
                  <span className="text-xs sm:text-sm font-medium text-gray-600 bg-gray-50 px-2 py-1 rounded flex-shrink-0">
                    {med.time?.slice(0, 5)}
                  </span>
                </div>

                {med.status === 'pending' && (
                  <div className="flex gap-2 mt-3">
                    <Button
                      size="lg"
                      variant="success"
                      className="flex-1 h-12 sm:h-12 text-sm sm:text-base font-semibold touch-manipulation active:scale-[0.97]"
                      onClick={() => takeMutation.mutate(med)}
                      disabled={takeMutation.isPending}
                    >
                      ✅ Ichdim
                    </Button>
                    <Button
                      size="lg"
                      variant="outline"
                      className="h-12 px-4 sm:px-5 text-sm sm:text-base touch-manipulation active:scale-[0.97]"
                      onClick={() => skipMutation.mutate(med)}
                      disabled={skipMutation.isPending}
                    >
                      O'tkazish
                    </Button>
                  </div>
                )}
                {med.status === 'completed' && (
                  <div className="mt-2 flex items-center gap-1 text-green-600">
                    <span className="text-base sm:text-lg">✅</span>
                    <span className="text-xs sm:text-sm font-medium">Qabul qilindi</span>
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {data?.upcoming_infusions && data.upcoming_infusions.length > 0 && (
        <div>
          <h2 className="text-base sm:text-lg font-semibold text-gray-900 mb-2 sm:mb-3">Bugungi kapelnitsalar</h2>
          <div className="space-y-2">
            {data.upcoming_infusions.map((inf) => (
              <Card key={inf.id}>
                <CardContent className="p-3 sm:p-4">
                  <div className="flex items-center justify-between">
                    <div className="min-w-0 flex-1">
                      <p className="font-medium text-gray-900 text-sm sm:text-base truncate">{inf.name}</p>
                      <p className="text-xs text-gray-500">{inf.volume} • Seans {inf.session_number}/{inf.total_sessions}</p>
                    </div>
                    <Badge variant={inf.status === 'completed' ? 'success' : 'warning'}>
                      {inf.status === 'completed' ? 'Bajarildi' : 'Kutilmoqda'}
                    </Badge>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
