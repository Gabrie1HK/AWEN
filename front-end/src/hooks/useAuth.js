import { useContext } from 'react'
import { AuthContext } from '../context/constants'

export function useAuth() { return useContext(AuthContext) }
