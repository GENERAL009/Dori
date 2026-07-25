import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { User, UserRole } from '@/types'

interface AuthState {
  token: string | null
  refreshToken: string | null
  users: User[]
  activeProfile: UserRole | null
  activeUserId: string | null
  pinVerified: boolean
  setUsers: (users: User[]) => void
  setAuth: (token: string, refreshToken: string, userId: string, role: UserRole) => void
  setProfile: (role: UserRole) => void
  logout: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      token: null,
      refreshToken: null,
      users: [],
      activeProfile: null,
      activeUserId: null,
      pinVerified: false,
      setUsers: (users) => set({ users, pinVerified: true }),
      setAuth: (token, refreshToken, userId, role) =>
        set({ token, refreshToken, activeUserId: userId, activeProfile: role }),
      setProfile: (role) => {
        const user = get().users.find(u => u.role === role)
        set({ activeProfile: role, activeUserId: user?.id || null })
      },
      logout: () => set({
        token: null, refreshToken: null, users: [], activeProfile: null,
        activeUserId: null, pinVerified: false,
      }),
    }),
    { name: 'dori-auth' }
  )
)
