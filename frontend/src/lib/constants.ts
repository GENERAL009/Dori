export const API_BASE_URL = import.meta.env.VITE_API_URL || '/api'
export const WS_URL = import.meta.env.VITE_WS_URL || `${window.location.protocol === 'https:' ? 'wss' : 'ws'}://${window.location.host}/ws`

export const MEDICATION_TYPES = {
  tablet: { label: 'Tabletka', color: 'bg-blue-100 text-blue-700' },
  capsule: { label: 'Kapsula', color: 'bg-indigo-100 text-indigo-700' },
  syrup: { label: 'Sirop', color: 'bg-amber-100 text-amber-700' },
  injection: { label: 'Ukol', color: 'bg-red-100 text-red-700' },
  infusion: { label: 'Kapelnitsa', color: 'bg-purple-100 text-purple-700' },
  vitamin: { label: 'Vitamin', color: 'bg-green-100 text-green-700' },
  drops: { label: 'Tomchi', color: 'bg-cyan-100 text-cyan-700' },
  suppository: { label: 'Svecha', color: 'bg-pink-100 text-pink-700' },
  packet: { label: 'Paketik', color: 'bg-orange-100 text-orange-700' },
} as const

export const MEDICATION_STATUSES = {
  active: { label: 'Faol', color: 'bg-green-100 text-green-700' },
  completed: { label: 'Tugagan', color: 'bg-gray-100 text-gray-700' },
  cancelled: { label: 'Bekor qilingan', color: 'bg-red-100 text-red-700' },
} as const

export const LOG_STATUSES = {
  taken: { label: 'Qabul qilindi', color: 'text-green-600', icon: '✅' },
  missed: { label: "O'tkazildi", color: 'text-red-600', icon: '❌' },
  skipped: { label: "Bugun yo'q", color: 'text-gray-600', icon: '⏭️' },
  delayed: { label: 'Kechikdi', color: 'text-yellow-600', icon: '⏰' },
} as const
