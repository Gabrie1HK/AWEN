import { useState, useCallback } from 'react'

export function useApi(initialData = null) {
  const [data, setData] = useState(initialData)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const execute = useCallback(async (apiCall) => {
    setLoading(true)
    setError(null)
    try {
      const result = await apiCall()
      setData(result)
      return result
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Error de red'
      setError(message)
      return null
    } finally {
      setLoading(false)
    }
  }, [])

  return { data, setData, loading, error, setError, execute }
}
