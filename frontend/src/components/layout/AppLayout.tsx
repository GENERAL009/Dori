import { Outlet } from 'react-router-dom'
import Header from './Header'
import MobileNav from './MobileNav'

export default function AppLayout() {
  return (
    <div className="min-h-screen min-h-[-webkit-fill-available] bg-gray-50 flex flex-col">
      <Header />
      <main className="flex-1 pb-[calc(4.5rem+env(safe-area-inset-bottom,0px))] md:pb-6 px-4 md:px-6 max-w-5xl mx-auto w-full pt-4">
        <Outlet />
      </main>
      <MobileNav />
    </div>
  )
}
