import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '@/stores/authStore'
import { loginWithPin } from '@/api/auth'
import { toast } from '@/components/ui/toaster'

export default function LoginPage() {
  const [pin, setPin] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const { setUsers } = useAuthStore()

  const handleDigit = (digit: string) => {
    if (pin.length < 4) {
      const newPin = pin + digit
      setPin(newPin)
      if (newPin.length === 4) {
        handleLogin(newPin)
      }
    }
  }

  const handleDelete = () => {
    setPin(pin.slice(0, -1))
  }

  const handleLogin = async (code: string) => {
    setLoading(true)
    try {
      const data = await loginWithPin(code)
      setUsers(data.users)
      navigate('/profile')
    } catch {
      toast({ title: 'Xato PIN kod', variant: 'destructive' })
      setPin('')
    } finally {
      setLoading(false)
    }
  }

  const digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '', '0', '⌫']

  return (
    <div className="min-h-screen min-h-[-webkit-fill-available] bg-white flex flex-col items-center justify-center px-4 safe-top safe-bottom">
      <div className="w-full max-w-sm">
        <div className="text-center mb-8 sm:mb-10">
          <div className="w-14 h-14 sm:w-16 sm:h-16 bg-primary-500 rounded-2xl flex items-center justify-center mx-auto mb-3 sm:mb-4">
            <span className="text-white text-xl sm:text-2xl font-bold">D</span>
          </div>
          <h1 className="text-xl sm:text-2xl font-bold text-gray-900">Dori</h1>
          <p className="text-gray-500 text-sm mt-1">Family Medicine Tracker</p>
        </div>

        <div className="flex justify-center gap-3 mb-8 sm:mb-10">
          {[0, 1, 2, 3].map((i) => (
            <div
              key={i}
              className={`w-3.5 h-3.5 sm:w-4 sm:h-4 rounded-full transition-all duration-200 ${
                i < pin.length ? 'bg-primary-500 scale-110' : 'bg-gray-200'
              }`}
            />
          ))}
        </div>

        <div className="grid grid-cols-3 gap-2.5 sm:gap-3 max-w-[260px] sm:max-w-[280px] mx-auto">
          {digits.map((digit, i) => (
            <button
              key={i}
              disabled={loading || digit === ''}
              onClick={() => digit === '⌫' ? handleDelete() : handleDigit(digit)}
              className={`h-14 sm:h-16 rounded-xl text-lg sm:text-xl font-medium transition-all touch-manipulation active:scale-95 select-none ${
                digit === ''
                  ? 'invisible'
                  : digit === '⌫'
                  ? 'text-gray-500 active:bg-gray-100'
                  : 'bg-gray-50 active:bg-gray-200 text-gray-900'
              } ${loading ? 'opacity-50' : ''}`}
            >
              {digit}
            </button>
          ))}
        </div>

        {loading && (
          <p className="text-center text-sm text-gray-500 mt-6">Tekshirilmoqda...</p>
        )}
      </div>
    </div>
  )
}
