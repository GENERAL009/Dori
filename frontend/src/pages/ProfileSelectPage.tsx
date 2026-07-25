import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '@/stores/authStore'
import { selectProfile } from '@/api/auth'
import { toast } from '@/components/ui/toaster'

export default function ProfileSelectPage() {
  const { users, pinVerified, setAuth } = useAuthStore()
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)

  if (!pinVerified || users.length === 0) {
    navigate('/login')
    return null
  }

  const handleSelect = async (role: 'male' | 'female') => {
    const user = users.find(u => u.role === role)
    if (!user) return

    setLoading(true)
    try {
      const data = await selectProfile(user.id)
      setAuth(data.access_token, data.refresh_token, data.user_id, role)
      navigate('/dashboard')
    } catch {
      toast({ title: 'Xatolik yuz berdi', variant: 'destructive' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-10">
          <h1 className="text-2xl font-bold text-gray-900">Kim kiryapti?</h1>
          <p className="text-gray-500 mt-2">Profilni tanlang</p>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <button
            onClick={() => handleSelect('male')}
            disabled={loading}
            className="flex flex-col items-center gap-4 p-8 rounded-2xl border-2 border-blue-200 hover:border-blue-400 hover:bg-blue-50 transition-all active:scale-95 disabled:opacity-50"
          >
            <div className="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center">
              <span className="text-4xl">👨</span>
            </div>
            <span className="text-lg font-semibold text-gray-800">Men</span>
          </button>

          <button
            onClick={() => handleSelect('female')}
            disabled={loading}
            className="flex flex-col items-center gap-4 p-8 rounded-2xl border-2 border-rose-200 hover:border-rose-400 hover:bg-rose-50 transition-all active:scale-95 disabled:opacity-50"
          >
            <div className="w-20 h-20 bg-rose-100 rounded-full flex items-center justify-center">
              <span className="text-4xl">👩</span>
            </div>
            <span className="text-lg font-semibold text-gray-800">Ayolim</span>
          </button>
        </div>

        {loading && (
          <p className="text-center text-sm text-gray-500 mt-6">Yuklanmoqda...</p>
        )}
      </div>
    </div>
  )
}
