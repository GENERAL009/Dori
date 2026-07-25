import * as React from 'react'
import * as ToastPrimitive from '@radix-ui/react-toast'
import { cn } from '@/lib/utils'
import { create } from 'zustand'

interface Toast {
  id: string
  title: string
  description?: string
  variant?: 'default' | 'success' | 'destructive'
}

interface ToastStore {
  toasts: Toast[]
  addToast: (toast: Omit<Toast, 'id'>) => void
  removeToast: (id: string) => void
}

export const useToastStore = create<ToastStore>((set) => ({
  toasts: [],
  addToast: (toast) =>
    set((state) => ({
      toasts: [...state.toasts, { ...toast, id: Math.random().toString(36).slice(2) }],
    })),
  removeToast: (id) =>
    set((state) => ({ toasts: state.toasts.filter((t) => t.id !== id) })),
}))

export function toast(props: Omit<Toast, 'id'>) {
  useToastStore.getState().addToast(props)
  setTimeout(() => {
    const toasts = useToastStore.getState().toasts
    if (toasts.length > 0) {
      useToastStore.getState().removeToast(toasts[0].id)
    }
  }, 4000)
}

export function Toaster() {
  const { toasts, removeToast } = useToastStore()

  return (
    <ToastPrimitive.Provider swipeDirection="right">
      {toasts.map((t) => (
        <ToastPrimitive.Root
          key={t.id}
          className={cn(
            'fixed bottom-4 right-4 z-[100] flex w-full max-w-sm items-center justify-between space-x-4 rounded-xl border p-4 shadow-lg transition-all',
            t.variant === 'destructive' ? 'border-red-200 bg-red-50' : t.variant === 'success' ? 'border-green-200 bg-green-50' : 'border-gray-200 bg-white'
          )}
          onOpenChange={(open) => { if (!open) removeToast(t.id) }}
        >
          <div className="flex flex-col gap-1">
            <ToastPrimitive.Title className="text-sm font-semibold">{t.title}</ToastPrimitive.Title>
            {t.description && <ToastPrimitive.Description className="text-sm text-muted-foreground">{t.description}</ToastPrimitive.Description>}
          </div>
          <ToastPrimitive.Close className="rounded-md p-1 hover:bg-gray-100">✕</ToastPrimitive.Close>
        </ToastPrimitive.Root>
      ))}
      <ToastPrimitive.Viewport />
    </ToastPrimitive.Provider>
  )
}
