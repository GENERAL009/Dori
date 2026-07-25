import { useNavigate, useLocation } from 'react-router-dom'

const navItems = [
  { path: '/dashboard', label: 'Bosh', icon: '🏠' },
  { path: '/medications', label: 'Dorilar', icon: '💊' },
  { path: '/infusions', label: 'Kapelnitsa', icon: '💉' },
  { path: '/calendar', label: 'Kalendar', icon: '📅' },
  { path: '/statistics', label: 'Statistika', icon: '📊' },
]

export default function MobileNav() {
  const navigate = useNavigate()
  const location = useLocation()

  return (
    <nav className="md:hidden fixed bottom-0 left-0 right-0 bg-white/95 backdrop-blur-md border-t border-gray-100 z-50">
      <div className="flex items-center justify-around h-16 px-1 safe-bottom">
        {navItems.map((item) => (
          <button
            key={item.path}
            onClick={() => navigate(item.path)}
            className={`flex flex-col items-center justify-center gap-0.5 min-w-[3rem] min-h-[3rem] px-2 py-1.5 rounded-xl transition-all touch-manipulation active:scale-95 ${
              location.pathname === item.path
                ? 'text-primary-600 bg-primary-50'
                : 'text-gray-400 active:bg-gray-50'
            }`}
          >
            <span className="text-xl leading-none">{item.icon}</span>
            <span className="text-[10px] font-medium leading-tight">{item.label}</span>
          </button>
        ))}
      </div>
    </nav>
  )
}
