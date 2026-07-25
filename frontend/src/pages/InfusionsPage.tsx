import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { getInfusions, completeInfusionSession } from '@/api/infusions'
import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { toast } from '@/components/ui/toaster'
import { formatDate } from '@/lib/utils'
import type { Infusion } from '@/types'

export default function InfusionsPage() {
  const queryClient = useQueryClient()

  const { data: infusions = [], isLoading } = useQuery({
    queryKey: ['infusions'],
    queryFn: () => getInfusions(),
  })

  const completeMutation = useMutation({
    mutationFn: completeInfusionSession,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['infusions'] })
      queryClient.invalidateQueries({ queryKey: ['dashboard'] })
      toast({ title: 'Seans bajarildi', variant: 'success' })
    },
  })

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-2 border-primary-500 border-t-transparent rounded-full animate-spin" />
      </div>
    )
  }

  return (
    <div className="space-y-3 sm:space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-lg sm:text-xl font-bold text-gray-900">Kapelnitsalar</h1>
        <Badge variant="warning">{infusions.length} ta</Badge>
      </div>

      <div className="space-y-2 sm:space-y-3">
        {infusions.length === 0 && (
          <Card>
            <CardContent className="p-6 text-center text-gray-500">
              Kapelnitsa yo'q
            </CardContent>
          </Card>
        )}
        {infusions.map((inf: Infusion) => (
          <InfusionCard
            key={inf.id}
            infusion={inf}
            onComplete={() => completeMutation.mutate(inf.id)}
            loading={completeMutation.isPending}
          />
        ))}
      </div>
    </div>
  )
}

function InfusionCard({ infusion, onComplete, loading }: { infusion: Infusion; onComplete: () => void; loading: boolean }) {
  const progress = infusion.total_sessions > 0
    ? Math.round((infusion.completed_sessions / infusion.total_sessions) * 100)
    : 0

  return (
    <Card className="active:shadow-md transition-shadow">
      <CardContent className="p-3 sm:p-4">
        <div className="flex items-start justify-between gap-2 mb-2 sm:mb-3">
          <div className="min-w-0 flex-1">
            <h3 className="font-semibold text-gray-900 text-sm sm:text-base truncate">{infusion.name}</h3>
            <p className="text-xs sm:text-sm text-gray-500 truncate">{infusion.solution} • {infusion.volume}</p>
          </div>
          <Badge className={`flex-shrink-0 text-[10px] sm:text-xs ${infusion.status === 'active' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'}`}>
            {infusion.status === 'active' ? 'Faol' : 'Tugagan'}
          </Badge>
        </div>

        <div className="grid grid-cols-2 gap-1.5 sm:gap-2 text-[10px] sm:text-xs text-gray-500 mb-2 sm:mb-3">
          <div>Chastota: {infusion.frequency}</div>
          <div>Boshlanish: {formatDate(infusion.start_date)}</div>
          {infusion.clinic && <div className="truncate">Klinika: {infusion.clinic}</div>}
          {infusion.doctor && <div className="truncate">Doktor: {infusion.doctor}</div>}
        </div>

        <div className="flex items-center justify-between mb-1.5 sm:mb-2">
          <span className="text-[10px] sm:text-xs text-gray-600">
            {infusion.completed_sessions} / {infusion.total_sessions} seans
          </span>
          <span className="text-[10px] sm:text-xs font-medium text-primary-600">{progress}%</span>
        </div>
        <Progress value={progress} className="h-1.5 sm:h-2 mb-2 sm:mb-3" />

        {infusion.status === 'active' && infusion.completed_sessions < infusion.total_sessions && (
          <Button
            size="lg"
            variant="success"
            className="w-full h-11 sm:h-12 text-sm sm:text-base font-semibold touch-manipulation active:scale-[0.97]"
            onClick={onComplete}
            disabled={loading}
          >
            ✅ Seansni bajarildi deb belgilash
          </Button>
        )}

        {infusion.notes && (
          <p className="text-[10px] sm:text-xs text-gray-400 mt-2 italic truncate">{infusion.notes}</p>
        )}
      </CardContent>
    </Card>
  )
}
