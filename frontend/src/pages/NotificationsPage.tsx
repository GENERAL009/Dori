import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { getNotifications, acknowledgeNotification, markAllRead } from '@/api/notifications'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { toast } from '@/components/ui/toaster'
import type { Notification } from '@/types'

export default function NotificationsPage() {
  const queryClient = useQueryClient()

  const { data: notifications = [], isLoading } = useQuery({
    queryKey: ['notifications'],
    queryFn: getNotifications,
  })

  const ackMutation = useMutation({
    mutationFn: ({ id, action }: { id: string; action: 'taken' | 'snooze' | 'skip' }) =>
      acknowledgeNotification(id, action),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notifications'] })
      queryClient.invalidateQueries({ queryKey: ['dashboard'] })
    },
  })

  const markAllMutation = useMutation({
    mutationFn: markAllRead,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notifications'] })
      toast({ title: "Hammasi o'qildi" })
    },
  })

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-2 border-primary-500 border-t-transparent rounded-full animate-spin" />
      </div>
    )
  }

  return (
    <div className="space-y-3 sm:space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-lg sm:text-xl font-bold text-gray-900">Bildirishnomalar</h1>
        {notifications.length > 0 && (
          <Button variant="ghost" size="sm" onClick={() => markAllMutation.mutate()} className="text-xs sm:text-sm touch-manipulation">
            Hammasini o'qildi
          </Button>
        )}
      </div>

      <div className="space-y-2">
        {notifications.length === 0 && (
          <Card>
            <CardContent className="p-6 text-center text-gray-500">
              Bildirishnoma yo'q
            </CardContent>
          </Card>
        )}
        {notifications.map((notif: Notification) => (
          <Card key={notif.id}>
            <CardContent className="p-3 sm:p-4">
              <div className="flex items-start justify-between gap-2 mb-2">
                <div className="min-w-0 flex-1">
                  <p className="font-medium text-gray-900 text-xs sm:text-sm truncate">{notif.message}</p>
                  <p className="text-[10px] sm:text-xs text-gray-500 mt-0.5">
                    {notif.scheduled_time?.slice(0, 5)}
                  </p>
                </div>
                <Badge className={`flex-shrink-0 text-[10px] sm:text-xs ${
                  notif.status === 'pending' ? 'bg-yellow-100 text-yellow-700' :
                  notif.status === 'sent' ? 'bg-blue-100 text-blue-700' :
                  'bg-gray-100 text-gray-700'
                }`}>
                  {notif.status === 'pending' ? 'Kutilmoqda' : notif.status === 'sent' ? 'Yuborildi' : 'O\'qildi'}
                </Badge>
              </div>

              {(notif.status === 'pending' || notif.status === 'sent') && (
                <div className="flex gap-1.5 sm:gap-2 mt-3">
                  <Button
                    size="lg"
                    variant="success"
                    className="flex-1 h-11 sm:h-12 text-sm sm:text-base font-semibold touch-manipulation active:scale-[0.97]"
                    onClick={() => ackMutation.mutate({ id: notif.id, action: 'taken' })}
                  >
                    ✅ Ichdim
                  </Button>
                  <Button
                    size="lg"
                    variant="outline"
                    className="flex-1 h-11 sm:h-12 text-sm sm:text-base font-semibold touch-manipulation active:scale-[0.97]"
                    onClick={() => ackMutation.mutate({ id: notif.id, action: 'snooze' })}
                  >
                    ⏰ 10 daq
                  </Button>
                  <Button
                    size="lg"
                    variant="ghost"
                    className="flex-1 h-11 sm:h-12 text-sm sm:text-base font-semibold touch-manipulation active:scale-[0.97]"
                    onClick={() => ackMutation.mutate({ id: notif.id, action: 'skip' })}
                  >
                    ❌ O'tkazish
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
