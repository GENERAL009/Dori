import { useMutation } from '@tanstack/react-query'
import { loginWithPin } from '@/api/auth'
import { useAuthStore } from '@/stores/authStore'
import { useNavigate } from 'react-router-dom'
import { toast } from '@/components/ui/toaster'

export function useLogin() {
  const { setAuth } = useAuthStore()
  const navigate = useNavigate()

  return useMutation({
    mutationFn: loginWithPin,
    onSuccess: (data) => {
      setAuth(data.access_token, data.refresh_token, data.users)
      navigate('/profile')
    },
    onError: () => {
      toast({ title: 'Xato PIN kod', variant: 'destructive' })
    },
  })
}
