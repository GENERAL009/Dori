import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from '@/stores/authStore'
import LoginPage from '@/pages/LoginPage'
import ProfileSelectPage from '@/pages/ProfileSelectPage'
import DashboardPage from '@/pages/DashboardPage'
import MedicationsPage from '@/pages/MedicationsPage'
import InfusionsPage from '@/pages/InfusionsPage'
import CalendarPage from '@/pages/CalendarPage'
import StatisticsPage from '@/pages/StatisticsPage'
import PrescriptionsPage from '@/pages/PrescriptionsPage'
import SettingsPage from '@/pages/SettingsPage'
import NotificationsPage from '@/pages/NotificationsPage'
import AppLayout from '@/components/layout/AppLayout'
import { Toaster } from '@/components/ui/toaster'
import { useWebSocket } from '@/hooks/useWebSocket'

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { token, activeProfile } = useAuthStore()
  if (!token) return <Navigate to="/login" replace />
  if (!activeProfile) return <Navigate to="/profile" replace />
  return <>{children}</>
}

export default function App() {
  useWebSocket()

  return (
    <>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/profile" element={<ProfileSelectPage />} />
        <Route element={<ProtectedRoute><AppLayout /></ProtectedRoute>}>
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/medications" element={<MedicationsPage />} />
          <Route path="/infusions" element={<InfusionsPage />} />
          <Route path="/calendar" element={<CalendarPage />} />
          <Route path="/statistics" element={<StatisticsPage />} />
          <Route path="/prescriptions" element={<PrescriptionsPage />} />
          <Route path="/notifications" element={<NotificationsPage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Route>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
      <Toaster />
    </>
  )
}
