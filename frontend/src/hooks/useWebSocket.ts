import { useEffect, useRef } from 'react'
import { useAuthStore } from '@/stores/authStore'
import { useQueryClient } from '@tanstack/react-query'
import { WS_URL } from '@/lib/constants'
import { toast } from '@/components/ui/toaster'

export function useWebSocket() {
  const ws = useRef<WebSocket | null>(null)
  const { token, activeUserId } = useAuthStore()
  const queryClient = useQueryClient()

  useEffect(() => {
    if (!token || !activeUserId) return

    const connect = () => {
      try {
        ws.current = new WebSocket(`${WS_URL}/notifications?token=${token}&user_id=${activeUserId}`)

        ws.current.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data)
            if (data.type === 'medication_reminder') {
              toast({ title: data.message, variant: 'default' })
              if (Notification.permission === 'granted') {
                new Notification('Dori eslatmasi', { body: data.message, icon: '/favicon.svg' })
              }
              queryClient.invalidateQueries({ queryKey: ['notifications'] })
              queryClient.invalidateQueries({ queryKey: ['dashboard'] })
            }
          } catch {}
        }

        ws.current.onerror = () => {}

        ws.current.onclose = () => {
          setTimeout(connect, 10000)
        }
      } catch {}
    }

    if (typeof Notification !== 'undefined' && Notification.permission === 'default') {
      Notification.requestPermission()
    }

    connect()

    return () => {
      ws.current?.close()
    }
  }, [token, activeUserId, queryClient])
}
