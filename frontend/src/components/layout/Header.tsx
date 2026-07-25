import { useAuthStore } from '@/stores/authStore'
import { useNavigate, useLocation } from 'react-router-dom'
import { Button } from '@/components/ui/button'

const navItems = [
  { path: '/dashboard', label: 'Bosh sahifa' },
  { path: '/medications', label: 'Dorilar' },
  { path: '/infusions', label: 'Kapelnitsa' },
  { path: '/calendar', label: 'Kalendar' },
  { path: '/statistics', label: 'Statistika' },
  { path: '/prescriptions', label: 'Retseptlar' },
]

export default function Header() {
  const { activeProfile, logout } = useAuthStore()
  const navigate = useNavigate()
  const location = useLocation()

  return (
    <header className="bg-white border-b border-gray-100 sticky top-0 z-40 safe-top">
      <div className="max-w-5xl mx-auto px-4 md:px-6 h-14 md:h-16 flex items-center justify-between">
        <div className="flex items-center gap-2 md:gap-3">
          <div className="w-8 h-8 bg-primary-500 rounded-lg flex items-center justify-center">
            <span className="text-white text-sm font-bold">D</span>
          </div>
          <span className="font-semibold text-lg text-gray-900">Dori</span>
        </div>

        <nav className="hidden md:flex items-center gap-1">
          {navItems.map((item) => (
            <button
              key={item.path}
              onClick={() => navigate(item.path)}
              className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                location.pathname === item.path
                  ? 'bg-primary-50 text-primary-700'
                  : 'text-gray-600 hover:bg-gray-50'
              }`}
            >
              {item.label}
            </button>
          ))}
        </nav>

        <div className="flex items-center gap-2 md:gap-3">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center">
              <span className="text-sm">{activeProfile === 'male' ? '👨' : '👩'}</span>
            </div>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => { logout(); navigate('/login') }}
            className="text-gray-500 text-xs md:text-sm"
          >
            Chiqish
          </Button>
        </div>
      </div>
    </header>
  )
}
