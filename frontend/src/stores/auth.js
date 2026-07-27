import { reactive } from 'vue'

import { apiRequest } from '../services/api'

function readStoredUser() {
  try {
    const value = localStorage.getItem('ai_naming_user')
    return value ? JSON.parse(value) : null
  } catch {
    localStorage.removeItem('ai_naming_user')
    return null
  }
}

export const authState = reactive({
  token: localStorage.getItem('ai_naming_token') || '',
  user: readStoredUser(),
})

export function saveSession(payload) {
  authState.token = payload.access_token
  authState.user = payload.user
  localStorage.setItem('ai_naming_token', payload.access_token)
  localStorage.setItem('ai_naming_user', JSON.stringify(payload.user))
}

export function clearSession() {
  authState.token = ''
  authState.user = null
  localStorage.removeItem('ai_naming_token')
  localStorage.removeItem('ai_naming_user')
}

export async function refreshCurrentUser() {
  const user = await apiRequest('/auth/me')
  authState.user = user
  localStorage.setItem('ai_naming_user', JSON.stringify(user))
  return user
}
