import { useQuery } from '@tanstack/react-query'
import { getPrescriptions } from '@/api/prescriptions'
import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { formatFullDate } from '@/lib/utils'
import type { Prescription } from '@/types'

export default function PrescriptionsPage() {
  const { data: prescriptions = [], isLoading } = useQuery({
    queryKey: ['prescriptions'],
    queryFn: getPrescriptions,
  })

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-2 border-primary-500 border-t-transparent rounded-full animate-spin" />
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-bold text-gray-900">Retseptlar</h1>
        <Badge>{prescriptions.length} ta</Badge>
      </div>

      <div className="space-y-3">
        {prescriptions.length === 0 && (
          <Card>
            <CardContent className="p-6 text-center text-gray-500">
              Retsept yo'q
            </CardContent>
          </Card>
        )}
        {prescriptions.map((rx: Prescription) => (
          <Card key={rx.id} className="hover:shadow-md transition-shadow">
            <CardContent className="p-4">
              <div className="flex items-start justify-between mb-2">
                <div>
                  <h3 className="font-semibold text-gray-900">{rx.doctor}</h3>
                  {rx.hospital && <p className="text-xs text-gray-500">{rx.hospital}</p>}
                </div>
                <span className="text-xs text-gray-400">{formatFullDate(rx.date)}</span>
              </div>
              <p className="text-sm text-gray-600 mb-2">{rx.diagnosis}</p>
              {rx.notes && <p className="text-xs text-gray-400 italic">{rx.notes}</p>}
              {rx.image_path && (
                <div className="mt-3">
                  <Badge variant="secondary">Rasm biriktirilgan</Badge>
                </div>
              )}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
