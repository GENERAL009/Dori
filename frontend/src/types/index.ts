export type MedicationType = 'tablet' | 'capsule' | 'syrup' | 'injection' | 'infusion' | 'vitamin' | 'drops' | 'suppository' | 'packet'
export type MedicationStatus = 'active' | 'completed' | 'cancelled'
export type LogStatus = 'taken' | 'missed' | 'skipped' | 'delayed'
export type UserRole = 'male' | 'female'

export interface User {
  id: string
  name: string
  role: UserRole
  is_active: boolean
}

export interface Medication {
  id: string
  name: string
  type: MedicationType
  dosage: string
  instruction: string
  frequency: string
  times: string[]
  start_date: string
  end_date: string
  duration_days: number
  status: MedicationStatus
  notes: string | null
  user_id: string
  created_at: string
  updated_at: string
}

export interface Infusion {
  id: string
  name: string
  solution: string
  volume: string
  frequency: string
  time: string
  clinic: string | null
  doctor: string | null
  status: string
  start_date: string
  end_date: string
  duration_days: number
  total_sessions: number
  completed_sessions: number
  notes: string | null
  user_id: string
  created_at: string
}

export interface MedicationLog {
  id: string
  medication_id: string
  user_id: string
  scheduled_time: string
  taken_time: string | null
  status: LogStatus
  notes: string | null
  created_at: string
}

export interface Prescription {
  id: string
  doctor: string
  hospital: string | null
  diagnosis: string
  date: string
  notes: string | null
  image_path: string | null
  user_id: string
}

export interface Notification {
  id: string
  type: string
  message: string
  scheduled_time: string
  status: string
  medication_id: string | null
  user_id: string
}

export interface DashboardData {
  total_medications: number
  completed_today: number
  remaining_today: number
  missed_today: number
  days_remaining: number
  overall_progress: number
  today_medications: TodayMedication[]
  today_infusions: Infusion[]
}

export interface TodayMedication {
  id: string
  medication_id: string
  name: string
  dosage: string
  type: MedicationType
  scheduled_time: string
  status: LogStatus | 'pending'
  instruction: string
}

export interface Statistics {
  completion_rate: number
  total_taken: number
  total_missed: number
  total_skipped: number
  on_time_percentage: number
  weekly_data: WeeklyData[]
}

export interface WeeklyData {
  day: string
  taken: number
  missed: number
  total: number
}
