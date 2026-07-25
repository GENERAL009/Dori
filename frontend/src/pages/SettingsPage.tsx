import { useState } from 'react'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { useAuthStore } from '@/stores/authStore'
import { useNavigate } from 'react-router-dom'
import { toast } from '@/components/ui/toaster'

export default function SettingsPage() {
  const [soundEnabled, setSoundEnabled] = useState(true)
  const [reminderTime, setReminderTime] = useState('5')
  const { logout, activeProfile } = useAuthStore()
  const navigate = useNavigate()

  const handleSwitchProfile = () => {
    navigate('/profile')
  }

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-bold text-gray-900">Sozlamalar</h1>

      <Card>
        <CardContent className="p-4 space-y-4">
          <h3 className="font-semibold text-gray-900">Bildirishnomalar</h3>

          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-700">Ovoz</span>
            <button
              onClick={() => {
                setSoundEnabled(!soundEnabled)
                toast({ title: soundEnabled ? 'Ovoz o\'chirildi' : 'Ovoz yoqildi' })
              }}
              className={`w-12 h-6 rounded-full transition-colors ${soundEnabled ? 'bg-primary-500' : 'bg-gray-300'}`}
            >
              <div className={`w-5 h-5 bg-white rounded-full shadow transition-transform ${soundEnabled ? 'translate-x-6' : 'translate-x-0.5'}`} />
            </button>
          </div>

          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-700">Eslatma vaqti</span>
            <select
              value={reminderTime}
              onChange={(e) => setReminderTime(e.target.value)}
              className="text-sm border rounded-lg px-3 py-1.5 bg-white"
            >
              <option value="15">15 daqiqa oldin</option>
              <option value="5">5 daqiqa oldin</option>
              <option value="0">Vaqtida</option>
            </select>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="p-4 space-y-4">
          <h3 className="font-semibold text-gray-900">Profil</h3>
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-700">Joriy profil</span>
            <span className="text-sm font-medium">
              {activeProfile === 'male' ? '👨 Erkak' : '👩 Ayol'}
            </span>
          </div>
          <Button variant="outline" className="w-full" onClick={handleSwitchProfile}>
            Profilni almashtirish
          </Button>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="p-4">
          <Button variant="destructive" className="w-full" onClick={handleLogout}>
            Chiqish
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}
