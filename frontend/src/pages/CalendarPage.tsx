import { useState, useMemo } from 'react'
import { useQuery } from '@tanstack/react-query'
import { getMedications } from '@/api/medications'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { MEDICATION_TYPES } from '@/lib/constants'
import type { Medication } from '@/types'

const MONTH_NAMES = ['Yanvar', 'Fevral', 'Mart', 'Aprel', 'May', 'Iyun', 'Iyul', 'Avgust', 'Sentyabr', 'Oktyabr', 'Noyabr', 'Dekabr']
const DAY_NAMES = ['Du', 'Se', 'Cho', 'Pa', 'Ju', 'Sha', 'Ya']

function getTodayStr() {
  const d = new Date()
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

export default function CalendarPage() {
  const today = new Date()
  const [currentDate, setCurrentDate] = useState(today)
  const [selectedDate, setSelectedDate] = useState<string>(getTodayStr())

  const month = currentDate.getMonth() + 1
  const year = currentDate.getFullYear()

  const { data: medications = [] } = useQuery({
    queryKey: ['medications'],
    queryFn: () => getMedications(),
  })

  const daysInMonth = new Date(year, month, 0).getDate()
  const firstDayOfMonth = new Date(year, month - 1, 1).getDay()
  const startDay = firstDayOfMonth === 0 ? 6 : firstDayOfMonth - 1

  const calendarMap = useMemo(() => {
    const map: Record<string, { name: string; type: string; times: string[]; dosage: string; instruction: string | null }[]> = {}

    medications.forEach((med: Medication) => {
      if (med.status !== 'active') return
      const start = new Date(med.start_date)
      const end = med.end_date ? new Date(med.end_date) : new Date(start.getTime() + 90 * 86400000)

      for (let d = new Date(start); d <= end; d.setDate(d.getDate() + 1)) {
        if (d.getMonth() + 1 === month && d.getFullYear() === year) {
          const key = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
          if (!map[key]) map[key] = []
          map[key].push({
            name: med.name,
            type: med.type,
            times: med.times,
            dosage: med.dosage,
            instruction: med.instruction,
          })
        }
      }
    })
    return map
  }, [medications, month, year])

  const prevMonth = () => {
    setCurrentDate(new Date(year, month - 2, 1))
  }

  const nextMonth = () => {
    setCurrentDate(new Date(year, month, 1))
  }

  const goToToday = () => {
    setCurrentDate(new Date())
    setSelectedDate(getTodayStr())
  }

  const selectedDayMeds = selectedDate ? calendarMap[selectedDate] || [] : []
  const todayStr = getTodayStr()

  return (
    <div className="space-y-3 sm:space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-lg sm:text-xl font-bold text-gray-900">Kalendar</h1>
        <Button variant="outline" size="sm" onClick={goToToday} className="touch-manipulation">Bugun</Button>
      </div>

      <Card>
        <CardContent className="p-3 sm:p-4">
          <div className="flex items-center justify-between mb-4">
            <Button variant="ghost" size="sm" className="h-9 w-9 sm:h-10 sm:w-10 text-lg touch-manipulation active:scale-90" onClick={prevMonth}>←</Button>
            <h2 className="font-bold text-base sm:text-lg text-gray-900">{MONTH_NAMES[month - 1]} {year}</h2>
            <Button variant="ghost" size="sm" className="h-9 w-9 sm:h-10 sm:w-10 text-lg touch-manipulation active:scale-90" onClick={nextMonth}>→</Button>
          </div>

          <div className="grid grid-cols-7 gap-0.5 sm:gap-1 mb-2">
            {DAY_NAMES.map(d => (
              <div key={d} className="text-center text-[10px] sm:text-xs text-gray-400 font-semibold py-1">{d}</div>
            ))}
          </div>

          <div className="grid grid-cols-7 gap-0.5 sm:gap-1">
            {Array.from({ length: startDay }).map((_, i) => (
              <div key={`empty-${i}`} className="aspect-square" />
            ))}
            {Array.from({ length: daysInMonth }).map((_, i) => {
              const day = i + 1
              const dateStr = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`
              const isToday = todayStr === dateStr
              const isSelected = selectedDate === dateStr
              const dayMeds = calendarMap[dateStr] || []
              const hasMeds = dayMeds.length > 0
              const totalDoses = dayMeds.reduce((sum, m) => sum + m.times.length, 0)

              return (
                <button
                  key={day}
                  onClick={() => setSelectedDate(dateStr)}
                  className={`relative aspect-square flex flex-col items-center justify-center rounded-lg sm:rounded-xl text-xs sm:text-sm font-medium transition-all touch-manipulation active:scale-95 ${
                    isSelected
                      ? 'bg-primary-500 text-white shadow-md'
                      : isToday
                      ? 'bg-primary-100 text-primary-700 font-bold ring-2 ring-primary-300'
                      : hasMeds
                      ? 'bg-blue-50 text-gray-800 active:bg-blue-100'
                      : 'active:bg-gray-50 text-gray-600'
                  }`}
                >
                  <span>{day}</span>
                  {hasMeds && !isSelected && (
                    <div className="absolute bottom-0.5 sm:bottom-1 flex gap-0.5">
                      {totalDoses <= 3 && Array.from({ length: Math.min(totalDoses, 3) }).map((_, di) => (
                        <div key={di} className="w-1 h-1 sm:w-1.5 sm:h-1.5 rounded-full bg-primary-400" />
                      ))}
                      {totalDoses > 3 && (
                        <span className="text-[7px] sm:text-[8px] text-primary-500 font-bold">{totalDoses}</span>
                      )}
                    </div>
                  )}
                  {hasMeds && isSelected && (
                    <span className="text-[8px] sm:text-[9px] text-white/80 font-semibold">{totalDoses} ta</span>
                  )}
                </button>
              )
            })}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="p-3 sm:p-4">
          <div className="flex items-center justify-between mb-2 sm:mb-3">
            <h3 className="font-bold text-sm sm:text-base text-gray-900">
              {selectedDate ? `${new Date(selectedDate + 'T00:00').getDate()} ${MONTH_NAMES[new Date(selectedDate + 'T00:00').getMonth()]}` : 'Kunni tanlang'}
            </h3>
            {selectedDate === todayStr && (
              <Badge variant="success">Bugun</Badge>
            )}
          </div>

          {selectedDayMeds.length === 0 ? (
            <p className="text-sm text-gray-500 text-center py-4">Bu kunda dori yo'q</p>
          ) : (
            <div className="space-y-0.5 sm:space-y-1">
              {selectedDayMeds.flatMap((med) =>
                med.times.map((t, ti) => (
                  <div
                    key={`${med.name}-${ti}`}
                    className="flex items-center justify-between py-2 sm:py-2.5 px-2 sm:px-3 rounded-lg hover:bg-gray-50 active:bg-gray-50 transition-colors"
                  >
                    <div className="flex items-center gap-2 sm:gap-3 min-w-0 flex-1">
                      <span className="text-[10px] sm:text-xs bg-primary-50 text-primary-600 px-2 py-0.5 sm:py-1 rounded-full font-semibold min-w-[42px] sm:min-w-[50px] text-center flex-shrink-0">
                        {t.slice(0, 5)}
                      </span>
                      <div className="min-w-0 flex-1">
                        <span className="text-xs sm:text-sm font-medium text-gray-800 block truncate">{med.name}</span>
                        <span className="text-[10px] sm:text-xs text-gray-400">{med.dosage}</span>
                      </div>
                    </div>
                    <Badge className={`text-[9px] sm:text-xs ml-1 flex-shrink-0 ${MEDICATION_TYPES[med.type as keyof typeof MEDICATION_TYPES]?.color || 'bg-gray-100 text-gray-700'}`}>
                      {MEDICATION_TYPES[med.type as keyof typeof MEDICATION_TYPES]?.label || med.type}
                    </Badge>
                  </div>
                ))
              )}
            </div>
          )}

          {selectedDayMeds.length > 0 && (
            <div className="mt-2 sm:mt-3 pt-2 sm:pt-3 border-t border-gray-100 flex items-center justify-between">
              <span className="text-[11px] sm:text-xs text-gray-400">Jami</span>
              <span className="text-xs sm:text-sm font-bold text-primary-600">
                {selectedDayMeds.reduce((sum, m) => sum + m.times.length, 0)} ta dori
              </span>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
