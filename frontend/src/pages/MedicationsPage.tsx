import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { getMedications } from '@/api/medications'
import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs'
import { MEDICATION_TYPES, MEDICATION_STATUSES } from '@/lib/constants'
import { progressPercentage, daysRemaining } from '@/lib/utils'
import type { Medication } from '@/types'

export default function MedicationsPage() {
  const [filter, setFilter] = useState('all')

  const { data: medications = [], isLoading } = useQuery({
    queryKey: ['medications', filter],
    queryFn: () => getMedications(filter !== 'all' ? { type: filter } : undefined),
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
        <h1 className="text-lg sm:text-xl font-bold text-gray-900">Dorilar</h1>
        <Badge>{medications.length} ta</Badge>
      </div>

      <Tabs value={filter} onValueChange={setFilter}>
        <TabsList className="w-full overflow-x-auto no-scrollbar flex-nowrap">
          <TabsTrigger value="all" className="text-xs sm:text-sm touch-manipulation">Hammasi</TabsTrigger>
          <TabsTrigger value="tablet" className="text-xs sm:text-sm touch-manipulation">Tabletka</TabsTrigger>
          <TabsTrigger value="capsule" className="text-xs sm:text-sm touch-manipulation">Kapsula</TabsTrigger>
          <TabsTrigger value="vitamin" className="text-xs sm:text-sm touch-manipulation">Vitamin</TabsTrigger>
          <TabsTrigger value="packet" className="text-xs sm:text-sm touch-manipulation">Paketik</TabsTrigger>
          <TabsTrigger value="suppository" className="text-xs sm:text-sm touch-manipulation">Svecha</TabsTrigger>
        </TabsList>

        <TabsContent value={filter}>
          <div className="space-y-2 sm:space-y-3 mt-2 sm:mt-3">
            {medications.length === 0 && (
              <Card>
                <CardContent className="p-6 text-center text-gray-500">
                  Bu kategoriyada dori yo'q
                </CardContent>
              </Card>
            )}
            {medications.map((med: Medication) => (
              <MedicationCard key={med.id} medication={med} />
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}

function MedicationCard({ medication }: { medication: Medication }) {
  const progress = progressPercentage(medication.start_date, medication.end_date)
  const days = daysRemaining(medication.end_date)
  const typeInfo = MEDICATION_TYPES[medication.type]
  const statusInfo = MEDICATION_STATUSES[medication.status]

  return (
    <Card className="active:shadow-md transition-shadow">
      <CardContent className="p-3 sm:p-4">
        <div className="flex items-start justify-between gap-2 mb-2 sm:mb-3">
          <div className="min-w-0 flex-1">
            <h3 className="font-semibold text-gray-900 text-sm sm:text-base truncate">{medication.name}</h3>
            <p className="text-xs sm:text-sm text-gray-500 mt-0.5 truncate">{medication.dosage} • {medication.frequency}</p>
          </div>
          <div className="flex gap-1 flex-shrink-0">
            <Badge className={`text-[10px] sm:text-xs px-1.5 sm:px-2.5 ${typeInfo?.color}`}>{typeInfo?.label}</Badge>
            <Badge className={`text-[10px] sm:text-xs px-1.5 sm:px-2.5 ${statusInfo?.color}`}>{statusInfo?.label}</Badge>
          </div>
        </div>

        {medication.instruction && (
          <p className="text-[11px] sm:text-xs text-gray-600 mb-2 sm:mb-3 bg-gray-50 px-2 py-1 rounded truncate">{medication.instruction}</p>
        )}

        <div className="flex items-center gap-1.5 sm:gap-2 mb-2 sm:mb-3 flex-wrap">
          {medication.times.map((t, i) => (
            <span key={i} className="text-[10px] sm:text-xs bg-blue-50 text-blue-600 px-2 py-0.5 sm:py-1 rounded-full font-medium">
              {t.slice(0, 5)}
            </span>
          ))}
        </div>

        <div className="flex items-center justify-between">
          <div className="flex-1 mr-3 sm:mr-4">
            <Progress value={progress} className="h-1.5 sm:h-2" />
          </div>
          <span className="text-[10px] sm:text-xs text-gray-500 whitespace-nowrap">
            {days > 0 ? `${days} kun qoldi` : 'Tugagan'}
          </span>
        </div>

        {medication.notes && (
          <p className="text-[10px] sm:text-xs text-gray-400 mt-2 italic truncate">{medication.notes}</p>
        )}
      </CardContent>
    </Card>
  )
}
