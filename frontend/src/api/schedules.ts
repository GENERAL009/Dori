import apiClient from './client'

export interface CalendarDay {
  date: string
  medications: Array<{ id: string; name: string; type: string; time: string; status: string }>
  infusions: Array<{ id: string; name: string; time: string; status: string }>
}

export async function getCalendarData(month: number, year: number) {
  const res = await apiClient.get<CalendarDay[]>('/v1/schedules/calendar', { params: { month, year } })
  return res.data
}
