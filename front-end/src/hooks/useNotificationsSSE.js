import { useState, useEffect, useRef } from 'react'
import { getAuthToken } from '../services/api'

const MAX_RETRIES = 10
const BASE_DELAY = 1000

export function useNotificationsSSE() {
  const [notifications, setNotifications] = useState([])
  const [unreadCount, setUnreadCount] = useState(0)
  const eventSourceRef = useRef(null)
  const retryCountRef = useRef(0)
  const retryTimerRef = useRef(null)

  useEffect(() => {
    const token = getAuthToken()
    if (!token) return

    function connect() {
      const url = `/api/v1/notifications/stream?token=${encodeURIComponent(token)}`
      const es = new EventSource(url)
      eventSourceRef.current = es
      retryCountRef.current = 0

      es.onmessage = (event) => {
        try {
          const parsed = JSON.parse(event.data)
          if (parsed.type === 'ping') return
          if (parsed.type === 'notification' && parsed.data) {
            const n = parsed.data
            setNotifications(prev => [{
              id: n.id || String(Date.now()),
              text: n.message || n.text || '',
              time: n.created_at || n.time || 'Ahora',
              read: false,
            }, ...prev])
            setUnreadCount(prev => prev + 1)
          }
        } catch {
          // ignore malformed messages
        }
      }

      es.onerror = () => {
        es.close()
        eventSourceRef.current = null
        retryCountRef.current += 1
        if (retryCountRef.current <= MAX_RETRIES) {
          const delay = BASE_DELAY * Math.pow(2, retryCountRef.current - 1)
          retryTimerRef.current = setTimeout(connect, delay)
        }
      }
    }

    connect()

    return () => {
      if (retryTimerRef.current) clearTimeout(retryTimerRef.current)
      if (eventSourceRef.current) eventSourceRef.current.close()
      eventSourceRef.current = null
    }
  }, [])

  const markRead = (id) => {
    setNotifications(prev => prev.map(n => n.id === id ? { ...n, read: true } : n))
    setUnreadCount(prev => Math.max(0, prev - 1))
  }

  const markAllRead = () => {
    setNotifications(prev => prev.map(n => ({ ...n, read: true })))
    setUnreadCount(0)
  }

  return { notifications, unreadCount, markRead, markAllRead }
}
