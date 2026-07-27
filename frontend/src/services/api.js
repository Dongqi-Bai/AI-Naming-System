const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

function getErrorMessage(data, fallback) {
  if (typeof data?.detail === 'string') return data.detail
  if (Array.isArray(data?.detail)) {
    return data.detail.map((item) => item.msg).join('；')
  }
  return fallback
}

export async function apiRequest(path, options = {}) {
  const headers = new Headers(options.headers)
  const token = localStorage.getItem('ai_naming_token')

  if (options.body && !(options.body instanceof FormData)) {
    headers.set('Content-Type', 'application/json')
  }
  if (token) headers.set('Authorization', `Bearer ${token}`)

  let response
  try {
    response = await fetch(`${API_BASE_URL}${path}`, { ...options, headers })
  } catch {
    throw new Error('无法连接服务器，请确认后端服务已启动')
  }

  const data = await response.json().catch(() => ({}))
  if (!response.ok) {
    const error = new Error(getErrorMessage(data, '请求失败，请稍后重试'))
    error.status = response.status
    throw error
  }
  return data
}
