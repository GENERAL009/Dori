import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { getStatistics } from '@/api/statistics'
import { Card, CardContent } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs'

export default function StatisticsPage() {
  const [period, setPeriod] = useState<'today' | 'week' | 'month'>('week')

  const { data: stats, isLoading } = useQuery({
    queryKey: ['statistics', period],
    queryFn: () => getStatistics(period),
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
      <h1 className="text-xl font-bold text-gray-900">Statistika</h1>

      <Tabs value={period} onValueChange={(v) => setPeriod(v as 'today' | 'week' | 'month')}>
        <TabsList>
          <TabsTrigger value="today">Bugun</TabsTrigger>
          <TabsTrigger value="week">Hafta</TabsTrigger>
          <TabsTrigger value="month">Oy</TabsTrigger>
        </TabsList>
      </Tabs>

      <Card>
        <CardContent className="p-6">
          <div className="flex items-center justify-center mb-4">
            <div className="relative w-32 h-32">
              <svg className="w-full h-full -rotate-90" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="40" fill="none" stroke="#f1f5f9" strokeWidth="8" />
                <circle
                  cx="50" cy="50" r="40" fill="none"
                  stroke="#3b82f6" strokeWidth="8"
                  strokeLinecap="round"
                  strokeDasharray={`${(stats?.completion_rate || 0) * 2.51} 251`}
                />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <span className="text-2xl font-bold text-gray-900">{stats?.completion_rate || 0}%</span>
              </div>
            </div>
          </div>
          <p className="text-center text-sm text-gray-500">Bajarilish darajasi</p>
        </CardContent>
      </Card>

      <div className="grid grid-cols-2 gap-3">
        <Card>
          <CardContent className="p-4">
            <p className="text-2xl font-bold text-green-600">{stats?.total_taken || 0}</p>
            <p className="text-xs text-gray-500 mt-1">Qabul qilindi</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <p className="text-2xl font-bold text-red-600">{stats?.total_missed || 0}</p>
            <p className="text-xs text-gray-500 mt-1">O'tkazildi</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <p className="text-2xl font-bold text-blue-600">{stats?.on_time_percentage || 0}%</p>
            <p className="text-xs text-gray-500 mt-1">Vaqtida</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <p className="text-2xl font-bold text-yellow-600">{stats?.total_skipped || 0}</p>
            <p className="text-xs text-gray-500 mt-1">O'tkazib yuborildi</p>
          </CardContent>
        </Card>
      </div>

      {stats?.weekly_data && stats.weekly_data.length > 0 && (
        <Card>
          <CardContent className="p-4">
            <h3 className="font-semibold text-gray-900 mb-4">Haftalik ko'rinish</h3>
            <div className="flex items-end justify-between gap-2 h-32">
              {stats.weekly_data.map((day, i) => {
                const maxVal = Math.max(...stats.weekly_data.map(d => d.total), 1)
                const takenHeight = (day.taken / maxVal) * 100
                const missedHeight = (day.missed / maxVal) * 100

                return (
                  <div key={i} className="flex-1 flex flex-col items-center gap-1">
                    <div className="w-full flex flex-col-reverse h-24 gap-0.5">
                      <div
                        className="w-full bg-green-400 rounded-t"
                        style={{ height: `${takenHeight}%` }}
                      />
                      <div
                        className="w-full bg-red-300 rounded-t"
                        style={{ height: `${missedHeight}%` }}
                      />
                    </div>
                    <span className="text-[10px] text-gray-400">{day.day}</span>
                  </div>
                )
              })}
            </div>
            <div className="flex items-center gap-4 mt-3 justify-center">
              <div className="flex items-center gap-1">
                <div className="w-3 h-3 rounded bg-green-400" />
                <span className="text-xs text-gray-500">Qabul qilindi</span>
              </div>
              <div className="flex items-center gap-1">
                <div className="w-3 h-3 rounded bg-red-300" />
                <span className="text-xs text-gray-500">O'tkazildi</span>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
