import { useState, useEffect, useRef } from 'react'

export function useNotificationsSSE() {
  const [notifications, setNotifications] = useState([])
  const [unreadCount, setUnreadCount] = useState(0)
  const eventSourceRef = useRef(null)

  useEffect(() => {
    const token = localStorage.getItem('session_token')
    if (!token) return

    const url = `http://localhost:8000/api/v1/notifications/stream?token=${encodeURIComponent(token)}`
    const es = new EventSource(url)
    eventSourceRef.current = es

    es.onmessage = (event) => {
      try {
        const parsed = JSON.parse(event.data)
        if (parsed.type === 'ping') return
        if (parsed.type === 'notification' && parsed.data) {
          setNotifications(prev => [parsed.data, ...prev])
          setUnreadCount(prev => prev + 1)
        }
      } catch {
        // ignore malformed messages
      }
    }

    es.onerror = () => {
      // EventSource auto-reconnects
    }

    return () => {
      es.close()
      eventSourceRef.current = null
    }
  }, [])

  return { notifications, unreadCount }
}
